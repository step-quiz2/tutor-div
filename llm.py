"""
llm.py · Interfície Gemini per al Tutor de Divisibilitat (arquitectura v2).

Una sola funció pública:

    tutor_turn(capitol, current_position, transcript) -> dict

Fa UNA crida a Gemini per torn de conversa. El model rep la conversa
sencera del capítol com a `contents` multi-torn i retorna:
  - text natural per a l'alumne,
  - un separador literal `---CONTROL---`,
  - un bloc JSON {"action": "stay"|"advance"}.

El control flow (quin pas, quin capítol, quan s'acaba) viu a Python
(tutor.py); el model només decideix si cal quedar-se al pas o avançar.

Aquest disseny substitueix l'avaluació torn-a-torn aïllada de la v1
(que jutjava cada missatge sol i podia rebutjar respostes correctes
dites amb el vocabulari que la conversa havia construït).

Variables d'entorn:
  GEMINI_API_KEY  — obligatòria per al mode IA
  GEMINI_MODEL    — opcional, default "gemini-2.5-flash"

Si no hi ha clau, l'app funciona en un mode de reserva (heurístic
senzill) perquè es pugui provar el flux sense IA.
"""

from __future__ import annotations

import json
import os
import re
import time
import unicodedata
from pathlib import Path

try:
    from google import genai
    from google.genai import types as genai_types
    _GENAI_OK = True
except Exception:  # la SDK pot no estar instal·lada (tests amb mocks)
    genai = None
    genai_types = None
    _GENAI_OK = False


# ───────────────────────────── configuració ───────────────────────────── #

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

PROMPTS_DIR = Path(__file__).parent / "prompts"
PROMPT_VERSION = "v2"

# IMPORTANT: Gemini 2.5 Flash compta els tokens de raonament intern dins
# d'aquest pressupost. Un sostre baix (p. ex. 500) trunca la resposta
# abans del separador ---CONTROL---. 8000 deixa marge de sobres.
MAX_OUTPUT_TOKENS = 8000

TEMPERATURE = 0.4

CONTROL_SEPARATOR = "---CONTROL---"
VALID_ACTIONS = ("stay", "advance")

MAX_ATTEMPTS = 3
RETRY_PATTERNS = ("503", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
                  "DEADLINE_EXCEEDED", "500", "INTERNAL", "timeout", "Timeout")


# ───────────────────────────── client (lazy) ──────────────────────────── #

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY no està definida a l'entorn.")
        _client = genai.Client(api_key=api_key)
    return _client


def ia_disponible() -> bool:
    """True si hi ha SDK + clau d'API; False → mode de reserva."""
    return _GENAI_OK and bool(os.environ.get("GEMINI_API_KEY"))


# ─────────────────────── system prompt (cache per capítol) ─────────────── #

_prompt_cache: dict[int, str] = {}


def _render_steps(capitol: dict) -> str:
    blocs = []
    for p in capitol["passos"]:
        pistes = " · ".join(p.get("pistes", [])) or "(cap)"
        blocs.append(
            f"**PAS {p['id']}.** {p['pregunta']}\n"
            f"- Comprensió esperada (INTERNA, no la dictis): {p['resposta_ref']}\n"
            f"- Conceptes clau: {', '.join(p.get('conceptes_clau', []))}\n"
            f"- Pistes que pots reformular: {pistes}"
        )
    return "\n\n".join(blocs)


def _load_system_prompt(capitol: dict, cap_total: int) -> str:
    cid = capitol["id"]
    if cid in _prompt_cache:
        return _prompt_cache[cid]

    template = (PROMPTS_DIR / f"tutor_system_{PROMPT_VERSION}.md").read_text(
        encoding="utf-8"
    )
    replacements = {
        "{{CAP_NUM}}": str(capitol["id"]),
        "{{CAP_TOTAL}}": str(cap_total),
        "{{CAP_TITOL}}": capitol["titol"],
        "{{CAP_INTRO}}": capitol["introduccio"],
        "{{N_PASSOS}}": str(len(capitol["passos"])),
        "{{STEPS}}": _render_steps(capitol),
    }
    for k, v in replacements.items():
        template = template.replace(k, v)

    unresolved = re.findall(r"\{\{[A-Z_0-9]+\}\}", template)
    if unresolved:
        raise RuntimeError(f"Placeholders sense resoldre: {unresolved}")

    _prompt_cache[cid] = template
    return template


# ───────────────────────────── crida amb retry ────────────────────────── #

def _is_retriable(err: Exception) -> bool:
    s = str(err)
    return any(p in s for p in RETRY_PATTERNS)


def _call(system_instruction: str, contents: list) -> str:
    client = _get_client()
    last_err = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                    temperature=TEMPERATURE,
                ),
            )
            return resp.text or ""
        except Exception as e:
            last_err = e
            if not _is_retriable(e) or attempt == MAX_ATTEMPTS - 1:
                raise
            time.sleep(0.5 * (2 ** attempt))  # 0.5s, 1s, 2s
    if last_err:
        raise last_err
    raise RuntimeError("Crida a Gemini fallida sense raó coneguda")


# ───────────────────────────── parseig ────────────────────────────────── #

def _format_position_marker(current_position: dict, cap_total: int,
                            n_passos: int) -> str:
    cap = current_position.get("capitol")
    pas = current_position.get("pas")
    if cap is None or pas is None:
        return ""
    return f"[Posició actual: Capítol {cap} de {cap_total} · Pas {pas} de {n_passos}]"


def _split_reply_and_control(raw: str):
    if CONTROL_SEPARATOR not in raw:
        return (raw.strip(), None, False)
    a, b = raw.split(CONTROL_SEPARATOR, 1)
    return (a.strip(), b.strip(), True)


def _parse_control_block(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError
    except Exception:
        return {"action": "stay", "_parse_error": True}
    action = data.get("action", "stay")
    if action not in VALID_ACTIONS:
        action = "stay"
    return {"action": action, "_parse_error": False}


# ───────────────────────── mode de reserva (sense IA) ─────────────────── #

def _normalitza(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def _fallback_turn(capitol, current_position, transcript) -> dict:
    """Torn sense IA: heurística per paraules clau perquè el flux es
    pugui provar sense clau d'API. No és pedagògicament intel·ligent."""
    pas_num = current_position.get("pas", 1)
    passos = capitol["passos"]
    pas = passos[pas_num - 1]
    ultim_student = next(
        (t["content"] for t in reversed(transcript) if t["role"] == "student"),
        "",
    )

    if "(L'alumne demana una pista)" in ultim_student:
        pistes = pas.get("pistes", [])
        pista = pistes[0] if pistes else "Comencem pel primer càlcul, amb calma."
        return {"reply": f"Una pista: {pista}", "action": "stay",
                "n_api_calls": 0, "raw_output": "", "control_parse_ok": True}

    resp = _normalitza(ultim_student)
    claus = [_normalitza(c) for c in pas.get("conceptes_clau", [])]
    encerts = 0
    for c in claus:
        parts = [p.strip() for p in c.split(",")] if "," in c else [c]
        if any(p and p in resp for p in parts):
            encerts += 1
    prou = encerts >= max(1, (len(claus) + 1) // 2)

    if prou:
        if pas_num < len(passos):
            seg = passos[pas_num]
            reply = f"Molt bé! 🎉 Ho has entès. Passem al següent:\n\n{seg['pregunta']}"
        else:
            reply = "Molt bé! 🎉 Has tancat aquest capítol."
        return {"reply": reply, "action": "advance",
                "n_api_calls": 0, "raw_output": "", "control_parse_ok": True}

    pistes = pas.get("pistes", [])
    pista = pistes[0] if pistes else "Torna-ho a provar pas a pas."
    return {"reply": f"Encara no hi som del tot. Una pista: {pista}",
            "action": "stay", "n_api_calls": 0, "raw_output": "",
            "control_parse_ok": True}


# ──────────────────────── constructor de contents ─────────────────────── #

def _build_contents(transcript: list, marker: str) -> list:
    """Converteix el transcript intern en la llista de `contents` per a
    l'API de Gemini: mapeja tutor→model i student→user, i prepend el
    marcador de posició al darrer torn d'usuari.

    Extret com a funció pròpia per poder-se testejar independentment
    sense crida a l'API.
    """
    last_idx = len(transcript) - 1
    contents = []
    for i, turn in enumerate(transcript):
        role = "model" if turn["role"] == "tutor" else "user"
        text = turn["content"]
        if i == last_idx and role == "user" and marker:
            text = f"{marker}\n\n{text}"
        contents.append({"role": role, "parts": [{"text": text}]})
    return contents


# ───────────────────────── funció pública ─────────────────────────────── #

def tutor_turn(capitol: dict, current_position: dict,
               transcript: list, cap_total: int = 5) -> dict:
    """
    Un torn del tutor.

    Args:
        capitol: el capítol actual (dict de problems.CAPITOLS).
        current_position: {"capitol": int, "pas": int}.
        transcript: [{"role": "tutor"|"student", "content": str}, ...]
            del CAPÍTOL actual. Ha d'alternar i acabar en "student".
        cap_total: nombre total de capítols (per al marcador).

    Returns:
        {reply, action, n_api_calls, raw_output, control_parse_ok}
    """
    if not transcript:
        raise ValueError("tutor_turn requereix un transcript no buit.")
    if transcript[-1]["role"] != "student":
        raise ValueError(
            f"El transcript ha d'acabar en torn 'student', acaba en "
            f"'{transcript[-1]['role']}'."
        )
    for i in range(1, len(transcript)):
        if transcript[i]["role"] == transcript[i - 1]["role"]:
            raise ValueError(
                f"El transcript ha d'alternar tutor/student; als índexs "
                f"{i-1} i {i} hi ha dos torns '{transcript[i]['role']}' seguits."
            )

    if not ia_disponible():
        return _fallback_turn(capitol, current_position, transcript)

    system_instruction = _load_system_prompt(capitol, cap_total)
    marker = _format_position_marker(
        current_position, cap_total, len(capitol["passos"])
    )

    contents = _build_contents(transcript, marker)

    raw = _call(system_instruction, contents)
    reply, control_text, sep_found = _split_reply_and_control(raw)

    # Guard: bloqueig de seguretat o truncament poden retornar reply buit.
    # En lloc de mostrar un missatge en blanc, fem veure un error recuperable.
    if not reply:
        reply = (
            "Ho sento, ara no puc formular una resposta. "
            "Pots tornar a escriure el que has dit? 🙏"
        )

    if sep_found and control_text:
        control = _parse_control_block(control_text)
        parse_ok = not control.get("_parse_error", False)
    else:
        control = {"action": "stay"}
        parse_ok = False

    return {
        "reply": reply,
        "action": control["action"],
        "n_api_calls": 1,
        "raw_output": raw,
        "control_parse_ok": parse_ok,
    }
