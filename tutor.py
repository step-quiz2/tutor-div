"""
tutor.py · Màquina d'estats del Tutor de Divisibilitat (arquitectura v2).

No depèn de Streamlit. El model (llm.tutor_turn) retorna una acció
("stay" o "advance"); aquí mantenim l'estat (capítol, pas, transcript del
capítol, finished) i apliquem les transicions.

Cada CAPÍTOL és una unitat conversacional pròpia: el seu system prompt i
el seu transcript es construeixen per separat. Quan s'avança més enllà de
l'últim pas d'un capítol, Python tanca el capítol i obre el següent (no ho
fa el model).
"""

from __future__ import annotations

import time

import problems

PISTA_MARKER = "(L'alumne demana una pista)"


# ───────────────────────────── sessió ─────────────────────────────────── #

def new_session() -> dict:
    """Estat inicial. El tutor obre amb la presentació del Capítol 1 +
    la primera pregunta (generat per Python, sense crida a l'IA)."""
    cap = problems.CAPITOLS[0]
    return {
        "started_at": time.time(),
        "cap_idx": 0,                 # índex del capítol actual (0-based)
        "pas_idx": 0,                 # índex del pas dins del capítol (0-based)
        "finished": False,
        # transcript del CAPÍTOL actual (es reinicia en canviar de capítol)
        "transcript": [{"role": "tutor", "content": missatge_obertura_capitol(cap)}],
        # historial complet per mostrar a la UI (tots els capítols)
        "display": [{"role": "tutor", "content": missatge_obertura_capitol(cap)}],
        "turn_count": 0,
        "history": [],                # rastre per torn (per al professor)
        "last_raw_output": None,
    }


def capitol_actual(state: dict) -> dict:
    return problems.CAPITOLS[state["cap_idx"]]


def pas_actual(state: dict) -> dict:
    return capitol_actual(state)["passos"][state["pas_idx"]]


def position_dict(state: dict) -> dict:
    """Posició 1-based per al marcador que rep llm.tutor_turn."""
    return {"capitol": state["cap_idx"] + 1, "pas": state["pas_idx"] + 1}


def total_capitols() -> int:
    return len(problems.CAPITOLS)


# ───────────────────────── transicions d'estat ───────────────────────── #

def apply_action(state: dict, action: str) -> str:
    """
    Aplica l'acció del control block. Retorna un codi del que ha passat:
        "stay"             → ens quedem al mateix pas
        "seguent_pas"      → avancem a un pas dins del mateix capítol
        "seguent_capitol"  → comencem un capítol nou (Python l'obre)
        "fi"               → s'han completat tots els capítols

    Quan s'inicia un capítol nou, aquesta funció ja afegeix el missatge
    d'obertura tant al transcript (nou) com al display, perquè el següent
    torn del model rebi un transcript que comença pel tutor.
    """
    if action != "advance":
        return "stay"

    cap = capitol_actual(state)
    if state["pas_idx"] + 1 < len(cap["passos"]):
        state["pas_idx"] += 1
        return "seguent_pas"

    # Final del capítol.
    if state["cap_idx"] + 1 < total_capitols():
        state["cap_idx"] += 1
        state["pas_idx"] = 0
        nou_cap = capitol_actual(state)
        obertura = missatge_obertura_capitol(nou_cap)
        # Nou context conversacional per al capítol nou.
        state["transcript"] = [{"role": "tutor", "content": obertura}]
        state["display"].append({"role": "tutor", "content": obertura})
        return "seguent_capitol"

    state["finished"] = True
    return "fi"


def add_student(state: dict, text: str) -> None:
    state["transcript"].append({"role": "student", "content": text})
    state["display"].append({"role": "student", "content": text})


def add_tutor(state: dict, text: str) -> None:
    state["transcript"].append({"role": "tutor", "content": text})
    state["display"].append({"role": "tutor", "content": text})


def pop_last_student(state: dict) -> None:
    """Treu l'últim torn d'alumne (s'usa si la crida a l'IA falla, per
    no trencar l'alternança del transcript en el reintent)."""
    if state["transcript"] and state["transcript"][-1]["role"] == "student":
        state["transcript"].pop()
    if state["display"] and state["display"][-1]["role"] == "student":
        state["display"].pop()


# ───────────────────────── generació de textos ────────────────────────── #

def missatge_obertura_capitol(cap: dict) -> str:
    """Presentació d'un capítol + primera pregunta (la genera Python)."""
    primer = cap["passos"][0]
    return (
        f"## {cap['emoji']} Capítol {cap['id']} · {cap['titol']}\n\n"
        f"{cap['introduccio']}\n\n---\n\n"
        f"**Pas {primer['id']}.** {primer['pregunta']}"
    )


MISSATGE_BENVINGUDA = (
    "Hola! 👋 Sóc en **Pitàgoras**, el teu tutor de matemàtiques.\n\n"
    "Avui explorarem la **divisibilitat** en 5 capítols: múltiples, divisors, "
    "una propietat sorprenent del 6, i els misteriosos **nombres primers**.\n\n"
    "No et preocupis si t'equivoques: per a això hi sóc jo, per ajudar-te a "
    "pensar pas a pas. Quan vulguis, prem **Comença**! 🚀"
)

MISSATGE_FINAL = (
    "🎉 **Ho has aconseguit!** Has completat els 5 capítols sobre divisibilitat.\n\n"
    "Ara saps què és un **múltiple**, què és un **divisor**, per què els "
    "múltiples són infinits però els divisors no, quan un nombre divisible per "
    "2 i per 3 ho és també per 6, i què fa especials els **nombres primers**.\n\n"
    "Estic molt orgullós de tu. Bona feina! 🌟"
)
