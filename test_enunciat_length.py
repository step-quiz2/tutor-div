"""
test_enunciat_length.py — guarda-raïls de longitud dels enunciats.

Motivació (suggeriment de millora #1): els enunciats que Python injecta com
a bombolla pròpia s'havien d'anar retallant a mà. Aquest test fa que el
límit el faci complir la suite: si algú allarga una `pregunta` per sobre del
llindar, el test falla abans que ho noti un alumne fent scroll.

Al tutor-div el camp visible és `pregunta` (a diferència del tutor-ic, on és
`canonical_question`). Els enunciats d'aquí han de ser MOLT curts: l'app està
pensada per a un alumne de 12 anys i cada pas demana una sola cosa.

Llindars (generosos sobre el màxim real actual, ~168 car / 6 línies al pas
4.1, que mostra dades de context abans de les dues preguntes):
"""

import problems


MAX_PREGUNTA_CHARS = 240
MAX_PREGUNTA_LINES = 7


def _iter_passos():
    """Genera (capitol_id, pas) per a tots els passos de tots els capítols."""
    for cap in problems.CAPITOLS:
        for pas in cap["passos"]:
            yield cap["id"], pas


def test_pregunta_present():
    """Tot pas ha de tenir una `pregunta` no buida."""
    fails = []
    for cid, pas in _iter_passos():
        p = pas.get("pregunta", "")
        if not isinstance(p, str) or not p.strip():
            fails.append(f"Cap {cid} pas {pas.get('id')}: pregunta buida")
    assert not fails, "Passos sense pregunta:\n" + "\n".join(fails)


def test_pregunta_not_too_long():
    """La pregunta visible no supera els llindars de car/línies."""
    fails = []
    for cid, pas in _iter_passos():
        p = pas.get("pregunta", "") or ""
        n_chars = len(p)
        n_lines = p.count("\n") + 1
        if n_chars > MAX_PREGUNTA_CHARS:
            fails.append(
                f"Cap {cid} pas {pas.get('id')}: {n_chars} car "
                f"(> {MAX_PREGUNTA_CHARS})"
            )
        if n_lines > MAX_PREGUNTA_LINES:
            fails.append(
                f"Cap {cid} pas {pas.get('id')}: {n_lines} línies "
                f"(> {MAX_PREGUNTA_LINES})"
            )
    assert not fails, (
        "Enunciats massa llargs per a un alumne de 12 anys:\n"
        + "\n".join(fails)
    )


# ----------------------------------------------------------------------- #
# Runner mínim sense pytest (coherent amb test_tutor.py)
# ----------------------------------------------------------------------- #
if __name__ == "__main__":
    tests = [test_pregunta_present, test_pregunta_not_too_long]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {t.__name__}\n    {e}")
            failed += 1
    print("=" * 60)
    print(f"Tests passats: {passed}")
    print(f"Tests fallits: {failed}")
    print("=" * 60)
    raise SystemExit(1 if failed else 0)
