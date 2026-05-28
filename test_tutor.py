"""
Tests del Tutor de Divisibilitat. No requereixen clau d'API: exerciten
la lògica de parseig, la màquina d'estats i el mode de reserva.

Executa amb:  python3 test_tutor.py
"""

import os
import re

os.environ.pop("GEMINI_API_KEY", None)  # forcem mode de reserva als tests

import llm
import problems
import tutor

_passats = 0


def check(cond, nom):
    global _passats
    assert cond, f"FALLA: {nom}"
    _passats += 1


def transcript_valid(t):
    return (
        bool(t)
        and t[0]["role"] == "tutor"
        and all(t[i]["role"] != t[i - 1]["role"] for i in range(1, len(t)))
    )


# ── parseig del control block ──────────────────────────────────────────── #
def test_parsing():
    r, c, found = llm._split_reply_and_control("Hola\n\n---CONTROL---\n{\"action\":\"advance\"}")
    check((r, c, found) == ("Hola", '{"action":"advance"}', True), "split amb separador")
    check(llm._split_reply_and_control("text")[2] is False, "split sense separador")
    check(llm._parse_control_block('{"action":"advance"}')["action"] == "advance", "control advance")
    check(llm._parse_control_block('```json\n{"action":"stay"}\n```')["action"] == "stay", "control amb fences")
    check(llm._parse_control_block("garbage")["action"] == "stay", "control invàlid -> stay")
    check(llm._parse_control_block('{"action":"jump"}')["action"] == "stay", "acció desconeguda -> stay")


# ── marcador de posició ───────────────────────────────────────────────── #
def test_marker():
    m = llm._format_position_marker({"capitol": 2, "pas": 3}, 5, 3)
    check(m == "[Posició actual: Capítol 2 de 5 · Pas 3 de 3]", "marcador format")
    check(llm._format_position_marker({}, 5, 3) == "", "marcador buit sense posició")


# ── el prompt es renderitza per a tots els capítols ───────────────────── #
def test_prompt_render():
    for cap in problems.CAPITOLS:
        llm._prompt_cache.clear()
        sp = llm._load_system_prompt(cap, 5)
        check(not re.findall(r"\{\{[A-Z_0-9]+\}\}", sp), f"sense placeholders cap {cap['id']}")
        check("---CONTROL---" in sp, f"separador al prompt cap {cap['id']}")


# ── màquina d'estats: recorregut complet ──────────────────────────────── #
def test_walkthrough():
    state = tutor.new_session()
    check(transcript_valid(state["transcript"]), "transcript inicial vàlid")

    transitions, guard = [], 0
    while not state["finished"] and guard < 200:
        guard += 1
        tutor.add_student(state, "resposta")
        check(transcript_valid(state["transcript"]), f"transcript vàlid (student) torn {guard}")
        tutor.add_tutor(state, "feedback")
        check(transcript_valid(state["transcript"]), f"transcript vàlid (tutor) torn {guard}")
        trans = tutor.apply_action(state, "advance")
        transitions.append(trans)
        if trans == "seguent_capitol":
            check(state["transcript"][0]["role"] == "tutor", "capítol nou comença amb tutor")
            n_tutor = sum(1 for m in state["transcript"] if m["role"] == "tutor")
            check(n_tutor == 1, "transcript del capítol nou reiniciat")

    check(state["finished"], "sessió acabada")
    check(transitions.count("seguent_capitol") == 4, "4 transicions de capítol")
    check(transitions[-1] == "fi", "última transició és fi")
    total = sum(len(c["passos"]) for c in problems.CAPITOLS)
    check(guard == total, f"un torn per pas ({total})")


# ── stay no avança ────────────────────────────────────────────────────── #
def test_stay():
    state = tutor.new_session()
    tutor.add_student(state, "no ho sé")
    tutor.add_tutor(state, "pista")
    cap0, pas0 = state["cap_idx"], state["pas_idx"]
    trans = tutor.apply_action(state, "stay")
    check(trans == "stay" and (state["cap_idx"], state["pas_idx"]) == (cap0, pas0),
          "stay no canvia de pas")


# ── pop_last_student manté l'alternança en cas d'error d'API ──────────── #
def test_pop_on_error():
    state = tutor.new_session()
    tutor.add_student(state, "resposta")
    tutor.pop_last_student(state)
    check(transcript_valid(state["transcript"]), "transcript vàlid després de pop")
    check(state["transcript"][-1]["role"] == "tutor", "acaba en tutor després de pop")


# ── mode de reserva ───────────────────────────────────────────────────── #
def test_fallback():
    check(not llm.ia_disponible(), "ia no disponible sense clau")
    state = tutor.new_session()
    tutor.add_student(state, "3 6 9 12 15, el quart es 12 (3x4 multiplicar taula)")
    r = llm.tutor_turn(tutor.capitol_actual(state), tutor.position_dict(state),
                       state["transcript"], cap_total=5)
    check(r["action"] in ("stay", "advance"), "fallback retorna acció vàlida")
    check(r["n_api_calls"] == 0, "fallback no fa crides a l'API")

    state2 = tutor.new_session()
    tutor.add_student(state2, tutor.PISTA_MARKER)
    r2 = llm.tutor_turn(tutor.capitol_actual(state2), tutor.position_dict(state2),
                        state2["transcript"], cap_total=5)
    check(r2["action"] == "stay", "pista no avança")


# ── invariants de tutor_turn ──────────────────────────────────────────── #
def test_invariants():
    try:
        llm.tutor_turn(problems.CAPITOLS[0], {"capitol": 1, "pas": 1},
                       [{"role": "tutor", "content": "x"}], 5)
        check(False, "hauria d'haver llançat (acaba en tutor)")
    except ValueError:
        check(True, "invariant acaba-en-student")
    try:
        llm.tutor_turn(problems.CAPITOLS[0], {"capitol": 1, "pas": 1},
                       [{"role": "student", "content": "a"},
                        {"role": "student", "content": "b"}], 5)
        check(False, "hauria d'haver llançat (rols consecutius)")
    except ValueError:
        check(True, "invariant alternança")


if __name__ == "__main__":
    for fn in [test_parsing, test_marker, test_prompt_render, test_walkthrough,
               test_stay, test_pop_on_error, test_fallback, test_invariants]:
        fn()
        print(f"  ✓ {fn.__name__}")
    print(f"\n{_passats} comprovacions superades ✅")
