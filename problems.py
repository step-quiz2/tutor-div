"""
Definició dels capítols del Tutor de Divisibilitat (1r ESO).

Disseny pensat per a l'Aran (12 anys), que encara:
  - confon "múltiple" i "divisor",
  - no veu que els múltiples són infinits,
  - confon "imparell" amb "nombre primer".

Per això cada PAS demana **una sola cosa**, amb frases molt curtes.
Val més fer molts passos petits que un de gros.

Cada capítol té:
  - id, titol, emoji, introduccio (text curt que veu l'alumne)
  - passos: cadascun amb
      id              → "1.1", "1.2", ...
      pregunta        → text que veu l'alumne (UNA sola pregunta, curta)
      descripcio_pas  → resum intern (per al tutor LLM)
      resposta_ref    → resposta de referència (MAI es mostra a l'alumne)
      conceptes_clau  → llista de conceptes a detectar (per al LLM i el mode reserva)
      pistes          → pistes progressives (curtes, una idea cada una)
"""

CAPITOLS = [
    # ------------------------------------------------------------------ #
    # CAPÍTOL 1 · Múltiples: 12 de 3 o 3 de 12?                          #
    # ------------------------------------------------------------------ #
    {
        "id": 1,
        "titol": "Múltiples",
        "emoji": "✖️",
        "introduccio": "Avui mirem què vol dir **ser múltiple**. Treballem amb el 12 i el 3.",
        "passos": [
            {
                "id": "1.1",
                "pregunta": "Quant fa **12 ÷ 3**?",
                "descripcio_pas": "Calcular 12÷3 i veure que és exacta.",
                "resposta_ref": "12 ÷ 3 = 4. Surt rodó, és exacta.",
                "conceptes_clau": ["4", "exacta"],
                "pistes": [
                    "Reparteix 12 caramels en 3 bosses iguals. Quants en toca a cada bossa?",
                    "12 ÷ 3 = 4. No en sobra cap, per això és exacta.",
                ],
            },
            {
                "id": "1.2",
                "pregunta": "Ara fes **3 ÷ 12**. Et surt un nombre sencer?",
                "descripcio_pas": "Veure que 3÷12 no és exacta.",
                "resposta_ref": "3 ÷ 12 = 0,25. No és sencer, no és exacta.",
                "conceptes_clau": ["no", "0,25", "no exacta"],
                "pistes": [
                    "Vols donar 3 caramels a 12 nens. Arriba a tocar-ne un sencer a cadascú?",
                    "3 ÷ 12 = 0,25. Com que no és sencer, no és exacta.",
                ],
            },
            {
                "id": "1.3",
                "pregunta": "El **12 és múltiple del 3**? (Pista: mira quina divisió surt exacta.)",
                "descripcio_pas": "Aplicar la definició: A és múltiple de B si A÷B és exacta.",
                "resposta_ref": (
                    "Sí. 12 és múltiple de 3 perquè 12÷3 és exacta. "
                    "En canvi, 3 no és múltiple de 12."
                ),
                "conceptes_clau": ["si", "12 es multiple de 3"],
                "pistes": [
                    "Múltiple vol dir que la divisió surt exacta. Quina ha sortit exacta?",
                    "12 ÷ 3 = 4, és exacta. Per tant el 12 és múltiple del 3.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 2 · Divisors i múltiples de 15 (els múltiples són infinits) #
    # ------------------------------------------------------------------ #
    {
        "id": 2,
        "titol": "Divisors i múltiples del 15",
        "emoji": "➗",
        "introduccio": "Ara veiem la diferència entre **divisors** i **múltiples**, amb el 15.",
        "passos": [
            {
                "id": "2.1",
                "pregunta": (
                    "El 15 es divideix exacte per 1, 3, 5 i 15. "
                    "Aquests són els seus **divisors**. Quants en té?"
                ),
                "descripcio_pas": "Comptar els divisors del 15 (en té 4).",
                "resposta_ref": "El 15 té 4 divisors: 1, 3, 5 i 15.",
                "conceptes_clau": ["4", "quatre"],
                "pistes": [
                    "Compta'ls a poc a poc: 1, 3, 5, 15.",
                    "Són quatre nombres, així que el 15 té 4 divisors.",
                ],
            },
            {
                "id": "2.2",
                "pregunta": "Ara escriu els **3 primers múltiples** del 15.",
                "descripcio_pas": "Calcular 15·1, 15·2, 15·3.",
                "resposta_ref": "15, 30, 45 (que són 15×1, 15×2 i 15×3).",
                "conceptes_clau": ["15", "30", "45"],
                "pistes": [
                    "15 × 1 = 15. 15 × 2 = 30. I el següent?",
                    "15 × 3 = 45. Per tant: 15, 30, 45.",
                ],
            },
            {
                "id": "2.3",
                "pregunta": "Els múltiples del 15, **s'acaben en algun moment**?",
                "descripcio_pas": "Veure que els múltiples són infinits.",
                "resposta_ref": (
                    "No s'acaben mai. Sempre pots multiplicar per un nombre més gran. "
                    "Els múltiples són infinits."
                ),
                "conceptes_clau": ["no", "no s'acaben", "mai", "infinits"],
                "pistes": [
                    "Pots fer 15 × 100? I 15 × 1.000?",
                    "Sempre pots posar un nombre més gran. Per això no s'acaben mai.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 3 · Pocs o molts divisors                                  #
    # ------------------------------------------------------------------ #
    {
        "id": 3,
        "titol": "Pocs o molts divisors",
        "emoji": "📊",
        "introduccio": "Alguns nombres tenen pocs divisors i d'altres en tenen molts. Mirem-ho!",
        "passos": [
            {
                "id": "3.1",
                "pregunta": "Quins d'aquests nombres són **divisors del 7**? (1, 2, 3, 4, 5, 6, 7)",
                "descripcio_pas": "Triar els divisors del 7 de la llista (només 1 i 7).",
                "resposta_ref": "Només l'1 i el 7. El 7 té 2 divisors.",
                "conceptes_clau": ["1 i 7", "2 divisors", "dos"],
                "pistes": [
                    "Mira quins divideixen exacte el 7: 7÷1, 7÷2, 7÷3...",
                    "Només 7÷1 i 7÷7 surten exactes. Per tant: 1 i 7.",
                ],
            },
            {
                "id": "3.2",
                "pregunta": "Ara els divisors del **12**. Quins nombres el divideixen exacte?",
                "descripcio_pas": "Trobar els divisors del 12 (en té 6).",
                "resposta_ref": "1, 2, 3, 4, 6 i 12. El 12 té 6 divisors.",
                "conceptes_clau": ["1 2 3 4 6 12", "6 divisors", "sis"],
                "pistes": [
                    "Prova 12÷1, 12÷2, 12÷3, 12÷4, 12÷6, 12÷12.",
                    "Surten: 1, 2, 3, 4, 6, 12. Són sis.",
                ],
            },
            {
                "id": "3.3",
                "pregunta": "Qui té **més divisors**, el 7 o el 12?",
                "descripcio_pas": "Comparar la quantitat de divisors.",
                "resposta_ref": "El 12 (en té 6), molt més que el 7 (que en té 2).",
                "conceptes_clau": ["12", "el 12"],
                "pistes": [
                    "El 7 en té 2. El 12 en té 6.",
                    "6 és més que 2, així que el 12 en té més.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 4 · Nombres primers (i imparell ≠ primer)                  #
    # ------------------------------------------------------------------ #
    {
        "id": 4,
        "titol": "Nombres primers",
        "emoji": "⭐",
        "introduccio": (
            "Un **nombre primer** té només 2 divisors: l'1 i ell mateix. Anem a descobrir-los!"
        ),
        "passos": [
            {
                "id": "4.1",
                "pregunta": "El **7** té només 2 divisors (1 i 7). Llavors, el 7 és primer?",
                "descripcio_pas": "Confirmar que el 7 és primer.",
                "resposta_ref": "Sí. El 7 té només 2 divisors, l'1 i el 7. És primer.",
                "conceptes_clau": ["si", "7 es primer", "primer"],
                "pistes": [
                    "Primer vol dir: només 2 divisors, l'1 i ell mateix.",
                    "El 7 té 1 i 7. Són 2. Per tant és primer.",
                ],
            },
            {
                "id": "4.2",
                "pregunta": "Ara el **9**. Fixa't: **9 ÷ 3 = 3**. El 9 és primer?",
                "descripcio_pas": "Veure que el 9 NO és primer (té el 3 com a divisor).",
                "resposta_ref": (
                    "No. El 9 té 3 divisors: 1, 3 i 9. Com que té el 3, no és primer."
                ),
                "conceptes_clau": ["no", "no es primer", "te el 3"],
                "pistes": [
                    "El 9 es divideix exacte per 3. Llavors té un divisor de més.",
                    "Divisors del 9: 1, 3, 9. Són 3, no 2. Per tant no és primer.",
                ],
            },
            {
                "id": "4.3",
                "pregunta": "Explica-ho amb les teves paraules: **què és un nombre primer**?",
                "descripcio_pas": "Definir primer amb paraules pròpies.",
                "resposta_ref": (
                    "Un primer només es pot dividir exacte per l'1 i per ell mateix. "
                    "Té només 2 divisors. Per exemple, el 7."
                ),
                "conceptes_clau": ["nomes 1 i ell mateix", "2 divisors"],
                "pistes": [
                    "Pensa en el 7: per quins nombres es divideix exacte?",
                    "Un primer no es pot partir en grups iguals, només amb l'1 o amb ell sencer.",
                ],
            },
        ],
    },
]


# ───────────────────────── helpers ───────────────────────────────────── #

def get_capitol(id_cap: int) -> dict | None:
    for c in CAPITOLS:
        if c["id"] == id_cap:
            return c
    return None


def num_capitols() -> int:
    return len(CAPITOLS)
