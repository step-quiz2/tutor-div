"""
Definició dels 5 capítols del Tutor de Divisibilitat (1r ESO).

Cada capítol té:
  - id: enter 1–5
  - titol: nom curt del capítol
  - introduccio: text d'entrada que veu l'alumne
  - passos: llista de passos, cadascun amb:
      id              → "1.1", "1.2", etc.
      pregunta        → text que veu l'alumne
      descripcio_pas  → resum intern (per al tutor LLM)
      resposta_ref    → resposta de referència (MAI es mostra a l'alumne)
      conceptes_clau  → llista de conceptes que cal detectar (per al LLM)
      pistes          → llista de pistes progressives (màx. 3)
"""

CAPITOLS = [
    # ------------------------------------------------------------------ #
    # CAPÍTOL 1 · Múltiples: 12 de 3 o 3 de 12?                          #
    # ------------------------------------------------------------------ #
    {
        "id": 1,
        "titol": "Múltiples",
        "emoji": "✖️",
        "introduccio": (
            "Avui repassem què vol dir **ser un múltiple**. "
            "Practiquem amb els nombres 12 i 3."
        ),
        "passos": [
            {
                "id": "1.1",
                "pregunta": (
                    "Fes aquestes dues divisions: **12 ÷ 3** i **3 ÷ 12**. "
                    "Quina de les divisions és exacta?"
                ),
                "descripcio_pas": "Comprovar quina divisió és exacta.",
                "resposta_ref": (
                    "12÷3=4 (exacte). "
                    "3÷12=0,25 (no és enter, no és exacta)."
                ),
                "conceptes_clau": ["12÷3", "exacta", "no exacta", "3÷12"],
                "pistes": [
                    "Pensa: repartim 12 caramels entre 3 persones, a parts iguals. Quants toca a cada bossa?",
                    "En canvi, si vols repartir 3 euros entre 12 perones, creus que surt un nombre enter?",
                ],
            },
            {
                "id": "1.2",
                "pregunta": (
                    "Tu diries que **12 és múltiple de 3**, o bé que **3 és múltiple de 12?** "
                    "Per què?"
                ),
                "descripcio_pas": "Aplicar la definició de múltiple.",
                "resposta_ref": (
                    "12 és múltiple de 3 perquè 12÷3=4 és exacta. "
                    "3 NO és múltiple de 12 perquè 3÷12 no dona un nombre enter."
                ),
                "conceptes_clau": ["12 és múltiple de 3", "12÷3 exacta", "3 no és múltiple"],
                "pistes": [
                    "12÷3 = 4, i 3÷12=0,25",
                    "Com que 12÷3 = 4, vol dir que 12=3·4, o sigui, que 12 és un múltiple de 3",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 2 · Divisors i múltiples de 15                              #
    # ------------------------------------------------------------------ #
    {
        "id": 2,
        "titol": "Divisors i múltiples de 15",
        "emoji": "➗",
        "introduccio": (
            "Ara veurem la diferència entre **divisors** i **múltiples**. "
            "Farem servir el 15 com a exemple."
        ),
        "passos": [
            {
                "id": "2.1",
                "pregunta": (
                    "Fes: **15÷1, 15÷3, 15÷5 i 15÷15**. "
                    "Surten exactes? Aquests nombres (1, 3, 5, 15) s'anomenen **divisors** de 15. "
                    "Per què creus que es diuen divisors?"
                ),
                "descripcio_pas": "Trobar divisors de 15 i entendre el concepte.",
                "resposta_ref": (
                    "Les quatre divisions surten exactes. "
                    "Es diuen divisors perquè divideixen el 15 sense deixar resta."
                ),
                "conceptes_clau": ["exacta", "divisors", "divideixen", "sense resta"],
                "pistes": [
                    "15÷1=15 ✓, 15÷3=5 ✓. Prova 15÷5 i 15÷15.",
                    "Totes surten exactes! Es diuen 'divisors' perquè 'divideixen' el 15 en parts iguals.",
                ],
            },
            {
                "id": "2.2",
                "pregunta": (
                    "Escriu els **primers 5 múltiples de 15** (15 · 1, 15 · 2, 15 · 3, 15 · 4, 15 · 5). "
                    "Creus que els múltiples s'acaben algun dia, o continuen per sempre?"
                ),
                "descripcio_pas": "Calcular múltiples de 15 i concloure que són infinits.",
                "resposta_ref": (
                    "15, 30, 45, 60, 75. Els múltiples no s'acaben: "
                    "sempre podem multiplicar per un nombre més gran."
                ),
                "conceptes_clau": ["15", "30", "45", "60", "75", "infinits", "no s'acaben"],
                "pistes": [
                    "15 · 1=15, 15 · 2=30... Escriu-los tots cinc.",
                    "Podem calcular 15 · 100? I 15 · 1.000? Sempre podem continuar...",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 3 · Múltiple de 2 i de 3 → múltiple de 6?                  #
    # ------------------------------------------------------------------ #
    {
        "id": 3,
        "titol": "Múltiple de 2 i de 3... és múltiple de 6?",
        "emoji": "🔍",
        "introduccio": (
            "Ara investigarem una cosa curiosa. "
            "Si un nombre és divisible per 2 **i** per 3, "
            "**serà també divisible per 6?** Ho comprovarem."
        ),
        "passos": [
            {
                "id": "3.1",
                "pregunta": (
                    "Fes: **12÷2**, **12÷3**. Són totes les divisions exactes? "
                    "Ara prova  **12÷6**. És exacta la divisió?"
                ),
                "descripcio_pas": "Comprovar divisibilitat de 12 per 2, 3 i 6.",
                "resposta_ref": (
                    "12÷2=6 ✓, 12÷3=4 ✓, 12÷6=2 ✓. "
                    "12 és múltiple de 2, de 3 i de 6."
                ),
                "conceptes_clau": ["12÷2", "12÷3", "12÷6", "exacta", "sí totes"],
                "pistes": [
                    "12 és parell, oi? Llavors 12÷2 és exacta. Ara prova 12÷3.",
                    "12÷2=6 ✓, 12÷3=4 ✓. Ara 12÷6=?",
                ],
            },
            {
                "id": "3.2",
                "pregunta": (
                    "Ara fes aquestes divisions **10÷2**, **10÷3** i i **10÷6**. "
                    "Quines surten exactes? "
                    "**Què passa quan un nombre és múltiple de 2 i de 3 alhora?**"
                ),
                "descripcio_pas": "Contraexemple amb 10 i generalitzar la regla.",
                "resposta_ref": (
                    "10÷2=5 ✓, 10÷3≈3,33 ✗, 10÷6≈1,67 ✗. "
                    "10 és múltiple de 2 però NO de 3 ni de 6. "
                    "Conclusió: si un nombre és múltiple de 2 i de 3, aleshores també ho és de 6."
                ),
                "conceptes_clau": ["10÷3 no exacta", "10÷6 no exacta", "múltiple de 2 i 3 → múltiple de 6"],
                "pistes": [
                    "10 és parell → 10÷2=5 ✓. Ara 10÷3: reparteixes 10 en 3 grups iguals... surt exacte?",
                    "10÷3=3,33 (no exacta). El 12 era múltiple de 2 i de 3, i també de 6. El 10 és de 2 però no de 3. I de 6?",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 4 · Pocs o molts divisors (entre 1 i 20)                    #
    # ------------------------------------------------------------------ #
    {
        "id": 4,
        "titol": "Pocs o molts divisors",
        "emoji": "📊",
        "introduccio": (
            "Alguns nombres tenen molt pocs divisors i d'altres en tenen molts. "
            "Anem a veure-ho!"
        ),
        "passos": [
            {
                "id": "4.1",
                "pregunta": (
                    "Escriu tots els divisors del **7**. "
                    "Quants divisors té?"
                ),
                "descripcio_pas": "Trobar divisors del 7 (nombre primer) i comprovar que només en té 2.",
                "resposta_ref": (
                    "7 té 2 divisors: 1 i 7. "
                    "7÷1=7 ✓, 7÷2=3,5 ✗, 7÷3≈2,3 ✗, ... 7÷7=1 ✓."
                ),
                "conceptes_clau": ["2 divisors", "1 i 7", "pocs"],
                "pistes": [
                    "Prova: 7÷1, 7÷2, 7÷3, 7÷4, 7÷5, 7÷6, 7÷7. Quines surten exactes?",
                    "7÷2=3,5 ✗, 7÷3≈2,3 ✗, ... Sembla que només l'1 i el 7 el divideixen exactament.",
                ],
            },
            {
                "id": "4.2",
                "pregunta": (
                    "Ara escriu tots els divisors del **12**. "
                    "Quin nombre en té més, el 7 o el 12?"
                ),
                "descripcio_pas": "Trobar divisors del 12 i comparar amb el 7.",
                "resposta_ref": (
                    "12 té 6 divisors: 1, 2, 3, 4, 6, 12. "
                    "El 12 en té molts més que el 7."
                ),
                "conceptes_clau": ["6 divisors", "1, 2, 3, 4, 6, 12", "12 en té més"],
                "pistes": [
                    "Prova: 12÷1, 12÷2, 12÷3, 12÷4, 12÷5, 12÷6, ..., 12÷12. Quines surten exactes?",
                    "12÷1 ✓, 12÷2 ✓, 12÷3 ✓, 12÷4 ✓, 12÷5 ✗, 12÷6 ✓, 12÷7..11 ✗, 12÷12 ✓. Compta'ls!",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 5 · Nombres primers: el mínim de divisors                    #
    # ------------------------------------------------------------------ #
    {
        "id": 5,
        "titol": "Nombres primers",
        "emoji": "⭐",
        "introduccio": (
            "Hem vist que el 7 té molt pocs divisors. "
            "Els nombres amb **exactament 2 divisors** (l'1 i ell mateix) "
            "s'anomenen **nombres primers**. Anem a descobrir-los!"
        ),
        "passos": [
            {
                "id": "5.1",
                "pregunta": (
                    "Mira aquesta llista: **2, 4, 7, 9, 11**. "
                    "Quins d'ells tenen **exactament 2 divisors** (l'1 i ell mateix)? "
                    "Comprova-ho fent les divisions."
                ),
                "descripcio_pas": "Identificar nombres primers de la llista.",
                "resposta_ref": (
                    "2 → {1,2} = 2 divisors ✓ (primer). "
                    "4 → {1,2,4} = 3 divisors ✗. "
                    "7 → {1,7} = 2 divisors ✓ (primer). "
                    "9 → {1,3,9} = 3 divisors ✗. "
                    "11 → {1,11} = 2 divisors ✓ (primer)."
                ),
                "conceptes_clau": ["2, 7, 11", "exactament 2 divisors", "1 i ell mateix"],
                "pistes": [
                    "Comprova el 4: 4÷2=2 (exacta!). Té un divisor entre l'1 i el 4. "
                    "I el 7: 7÷2, 7÷3, 7÷4, 7÷5, 7÷6... cap surt exacte.",
                    "El 4 té 3 divisors (1, 2, 4), no és primer. El 2 i el 7 només en tenen 2. I el 9 i l'11?",
                ],
            },
            {
                "id": "5.2",
                "pregunta": (
                    "Explica amb les teves paraules **què és un nombre primer**. "
                    "Posa un exemple."
                ),
                "descripcio_pas": "Definir nombre primer amb paraules pròpies i un exemple.",
                "resposta_ref": (
                    "Un nombre primer és aquell que només es pot dividir exactament per l'1 i per ell mateix. "
                    "Per exemple, el 7: si proves 7÷2, 7÷3, 7÷4, 7÷5 o 7÷6 no surt exacte."
                ),
                "conceptes_clau": ["només divisible per 1 i ell mateix", "exemple", "exactament 2 divisors"],
                "pistes": [
                    "Pensa en el 11: per quins nombres el pots dividir exactament? "
                    "Explica-ho a partir d'aquest exemple.",
                    "Un nombre primer 'no el pots partir' en trossos iguals "
                    "excepte si uses l'1 o el nombre sencer. Com ho diries tu?",
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
