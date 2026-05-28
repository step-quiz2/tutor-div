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
        "titol": "Múltiples: 12 de 3, o 3 de 12?",
        "emoji": "✖️",
        "introduccio": (
            "En aquest capítol descobrirem **què significa la paraula «múltiple»** "
            "i aprendrem a identificar quan un nombre és múltiple d'un altre. "
            "Comencem amb un exemple concret: el 12 i el 3."
        ),
        "passos": [
            {
                "id": "1.1",
                "pregunta": (
                    "Calcula: 3×1, 3×2, 3×3, 3×4, 3×5. "
                    "Escriu els cinc resultats i digues quin és el quart."
                ),
                "descripcio_pas": "Construir la taula del 3 per reconèixer el 12 com a resultat.",
                "resposta_ref": (
                    "3, 6, 9, 12, 15. El quart resultat és 12 (3×4=12)."
                ),
                "conceptes_clau": ["12", "taula", "multiplicar", "3×4"],
                "pistes": [
                    "Multiplica 3 per 1, per 2, per 3... cada cop sumes 3 més. "
                    "Intenta escriure la llista: 3, 6, 9, ...",
                    "3×1=3, 3×2=6, 3×3=9, 3×4=?, 3×5=15. "
                    "Quant val 3×4?",
                ],
            },
            {
                "id": "1.2",
                "pregunta": (
                    "Ara fes les dues divisions: **12 ÷ 3** i **3 ÷ 12**. "
                    "Quina surt exacta (sense decimals ni resta)? Quina no?"
                ),
                "descripcio_pas": "Comprovar quina divisió és exacta per identificar el múltiple.",
                "resposta_ref": (
                    "12÷3=4 (exacte, sense resta). "
                    "3÷12=0,25 (no és enter, no és exacta)."
                ),
                "conceptes_clau": ["12÷3", "exacta", "no exacta", "3÷12"],
                "pistes": [
                    "Fes la primera: 12 entre 3. Quant toca a cada grup si reparteixes 12 coses en 3 grups iguals?",
                    "12÷3=4 (perfecte, sense sobrar res). Ara prova 3÷12: 3 entre 12... et surt un nombre enter?",
                ],
            },
            {
                "id": "1.3",
                "pregunta": (
                    "Usem la regla: *A és múltiple de B quan A÷B és exacta.* "
                    "Aleshores, **12 és múltiple de 3, o bé 3 és múltiple de 12?** "
                    "Explica per què amb les divisions que has calculat."
                ),
                "descripcio_pas": "Aplicar la definició de múltiple per concloure qui és múltiple de qui.",
                "resposta_ref": (
                    "12 és múltiple de 3 perquè 12÷3=4 és exacta. "
                    "3 NO és múltiple de 12 perquè 3÷12 no dona un nombre enter."
                ),
                "conceptes_clau": ["12 és múltiple de 3", "12÷3 exacta", "3 no és múltiple"],
                "pistes": [
                    "Recorda la regla: A és múltiple de B si A÷B és exacta. "
                    "Ara mira els teus resultats: quina divisió era exacta, la de 12÷3 o la de 3÷12?",
                    "12÷3=4 és exacta → 12 SÍ és múltiple de 3. "
                    "3÷12 no és entera → 3 NO és múltiple de 12.",
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
            "Ara que sabem què és un múltiple, aprendrem la diferència entre "
            "**divisors** i **múltiples** d'un nombre, usant el 15 com a exemple. "
            "Descobrirem també una cosa sorprenent sobre els múltiples!"
        ),
        "passos": [
            {
                "id": "2.1",
                "pregunta": (
                    "Divideix 15 entre cada nombre de l'1 al 15: **15÷1, 15÷2, 15÷3, ..., 15÷15**. "
                    "Escriu quines divisions surten exactes (sense resta) "
                    "i llista els nombres que ho aconsegueixen."
                ),
                "descripcio_pas": "Trobar tots els divisors de 15 per inspecció.",
                "resposta_ref": (
                    "Divisors de 15: 1, 3, 5, 15. "
                    "15÷1=15 ✓, 15÷2=7,5 ✗, 15÷3=5 ✓, 15÷4=3,75 ✗, "
                    "15÷5=3 ✓, 15÷6..15÷14 no exactes, 15÷15=1 ✓."
                ),
                "conceptes_clau": ["1", "3", "5", "15", "divisors", "exacta"],
                "pistes": [
                    "Comencem: 15÷1=15 (exacta ✓). 15÷2=7,5 (no exacta ✗). "
                    "15÷3=? Prova-ho.",
                    "Fins ara tens: 1 ✓, 2 ✗, 3 ✓. Segueix: 15÷4, 15÷5, 15÷6... "
                    "Quins més donen exacte?",
                ],
            },
            {
                "id": "2.2",
                "pregunta": (
                    "Amb la llista que has fet, **quants divisors té 15 en total?** "
                    "Escriu la llista completa de divisors i compta'ls."
                ),
                "descripcio_pas": "Comptar els divisors de 15 i dir-ne la quantitat total.",
                "resposta_ref": "15 té 4 divisors: 1, 3, 5 i 15.",
                "conceptes_clau": ["4", "quatre", "1, 3, 5, 15"],
                "pistes": [
                    "Els divisors de 15 són els nombres que el divideixen exactament. "
                    "Has trobat: 1, 3, 5 i 15. Compta'ls.",
                    "Divisors de 15: {1, 3, 5, 15}. Quants n'hi ha?",
                ],
            },
            {
                "id": "2.3",
                "pregunta": (
                    "Ara escriu els **primers 5 múltiples de 15** (15×1, 15×2, 15×3, 15×4, 15×5). "
                    "Creus que els múltiples d'un nombre s'acaben en algun moment, o continuen per sempre?"
                ),
                "descripcio_pas": "Calcular múltiples de 15 i concloure que són infinits.",
                "resposta_ref": (
                    "15, 30, 45, 60, 75. Els múltiples no s'acaben: "
                    "sempre podem multiplicar per un nombre més gran, fins a l'infinit."
                ),
                "conceptes_clau": ["15", "30", "45", "60", "75", "infinits", "no s'acaben"],
                "pistes": [
                    "15×1=15, 15×2=30, 15×3=?... Escriu-los tots cinc.",
                    "Pensa: podem calcular 15×1.000? I 15×1.000.000? "
                    "Sempre podem multiplicar per un nombre més gran...",
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
            "Investigarem una propietat molt interessant: si un nombre és "
            "divisible per 2 **i** per 3 alhora, **serà sempre divisible per 6?** "
            "Ho comprovarem amb exemples concrets."
        ),
        "passos": [
            {
                "id": "3.1",
                "pregunta": (
                    "Comprova si **12** és múltiple de 2, de 3 i de 6. "
                    "Fes les tres divisions: **12÷2**, **12÷3**, **12÷6** "
                    "i digues si cada una surt exacta."
                ),
                "descripcio_pas": "Comprovar divisibilitat de 12 per 2, 3 i 6.",
                "resposta_ref": (
                    "12÷2=6 (exacta ✓), 12÷3=4 (exacta ✓), 12÷6=2 (exacta ✓). "
                    "12 és múltiple de 2, de 3 i de 6."
                ),
                "conceptes_clau": ["12÷2", "12÷3", "12÷6", "exacta", "múltiple dels tres"],
                "pistes": [
                    "Comença per 12÷2: és parell el 12? Si sí, és múltiple de 2.",
                    "12÷2=6 ✓, 12÷3=4 ✓. Ara 12÷6=?",
                ],
            },
            {
                "id": "3.2",
                "pregunta": (
                    "Ara prova amb **18**: fes **18÷2**, **18÷3** i **18÷6**. "
                    "Surten totes exactes?"
                ),
                "descripcio_pas": "Comprovar divisibilitat de 18 per 2, 3 i 6 (segon exemple positiu).",
                "resposta_ref": (
                    "18÷2=9 (exacta ✓), 18÷3=6 (exacta ✓), 18÷6=3 (exacta ✓). "
                    "18 és múltiple de 2, de 3 i de 6."
                ),
                "conceptes_clau": ["18÷2", "18÷3", "18÷6", "exacta", "sí"],
                "pistes": [
                    "18 és parell? → divisible per 2. 18÷3=?",
                    "18÷2=9 ✓, 18÷3=6 ✓. Ara 18÷6=?",
                ],
            },
            {
                "id": "3.3",
                "pregunta": (
                    "Ara prova amb **10**: fes **10÷2**, **10÷3** i **10÷6**. "
                    "Quines divisions surten exactes i quines no?"
                ),
                "descripcio_pas": "Comprovar divisibilitat de 10: contraexemple (múltiple de 2 però no de 3 ni 6).",
                "resposta_ref": (
                    "10÷2=5 (exacta ✓), 10÷3≈3,33 (no exacta ✗), 10÷6≈1,67 (no exacta ✗). "
                    "10 és múltiple de 2 però NO de 3 ni de 6."
                ),
                "conceptes_clau": ["10÷2 exacta", "10÷3 no exacta", "10÷6 no exacta", "no és múltiple de 3"],
                "pistes": [
                    "10 és parell → 10÷2=5 ✓. Ara 10÷3: reparteixes 10 en 3 grups iguals... surt exacte?",
                    "10÷3=3,33... (no exacta). Llavors, 10 és múltiple de 2 però NO de 3. "
                    "I de 6?",
                ],
            },
            {
                "id": "3.4",
                "pregunta": (
                    "Compara els tres casos (12, 18, 10) i completa la conclusió:\n\n"
                    "«Si un nombre és múltiple de 2 **i** de 3, aleshores ________. "
                    "Si és múltiple de 2 però NO de 3, aleshores ________.»"
                ),
                "descripcio_pas": "Generalitzar la propietat: múltiple de 2 i 3 implica múltiple de 6.",
                "resposta_ref": (
                    "Si un nombre és múltiple de 2 i de 3, aleshores també és múltiple de 6. "
                    "Si és múltiple de 2 però no de 3, no és múltiple de 6 (exemple: 10). Tot múltiple de 6 ho és de 3, per tant si no és múltiple de 3 tampoc pot ser-ho de 6."
                ),
                "conceptes_clau": ["múltiple de 6", "sempre", "2 i 3", "no de 3 no de 6"],
                "pistes": [
                    "Quan 12 i 18 eren múltiples de 6? Quan ho eren de 2 i de 3 alhora. "
                    "I el 10 no era múltiple de 6 perquè...",
                    "El 10 era múltiple de 2 però NO de 3. I el resultat? No era múltiple de 6. "
                    "Què passa quan un nombre SÍ que és múltiple dels dos?",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 4 · Pocs o molts divisors (entre 1 i 20)                    #
    # ------------------------------------------------------------------ #
    {
        "id": 4,
        "titol": "Pocs o molts divisors (entre 1 i 20)",
        "emoji": "📊",
        "introduccio": (
            "Alguns nombres entre 1 i 20 tenen molt pocs divisors "
            "i d'altres en tenen molts. Anem a explorar-ho: quins nombres "
            "s'amaguen als extrems?"
        ),
        "passos": [
            {
                "id": "4.1",
                "pregunta": (
                    "Digues **un nombre entre 1 i 20** que creguis que té **molt pocs divisors**. "
                    "Escriu tots els seus divisors per comprovar-ho."
                ),
                "descripcio_pas": "Triar un nombre amb pocs divisors i llistar-los (idealment un primer).",
                "resposta_ref": (
                    "Exemples amb pocs divisors: 2 (divisors: 1,2), 3 (1,3), 5 (1,5), "
                    "7 (1,7), 11 (1,11), 13 (1,13), 17 (1,17), 19 (1,19). "
                    "Tots tenen exactament 2 divisors."
                ),
                "conceptes_clau": ["2 divisors", "1 i ell mateix", "pocs"],
                "pistes": [
                    "Prova amb el 7: 7÷1=7 ✓, 7÷2=3,5 ✗, 7÷3≈2,3 ✗, 7÷4, 7÷5, 7÷6 ✗, 7÷7=1 ✓. "
                    "Quants divisors té?",
                    "El 7 només té 2 divisors: l'1 i el 7. Hi ha altres nombres semblants?",
                ],
            },
            {
                "id": "4.2",
                "pregunta": (
                    "Ara digues **un nombre entre 1 i 20** que creguis que té **molts divisors**. "
                    "Escriu tots els seus divisors i compta'ls."
                ),
                "descripcio_pas": "Triar un nombre amb molts divisors (12, 18 o 20) i llistar-los.",
                "resposta_ref": (
                    "Bones opcions: 12 → {1,2,3,4,6,12} = 6 divisors; "
                    "18 → {1,2,3,6,9,18} = 6 divisors; "
                    "20 → {1,2,4,5,10,20} = 6 divisors; "
                    "16 → {1,2,4,8,16} = 5 divisors."
                ),
                "conceptes_clau": ["6 divisors", "12", "18", "20", "molts"],
                "pistes": [
                    "Prova amb el 12: 12÷1 ✓, 12÷2 ✓, 12÷3 ✓, 12÷4 ✓, 12÷5 ✗, 12÷6 ✓, "
                    "12÷7..11 ✗, 12÷12 ✓. Compta'ls!",
                    "El 12 té divisors: 1, 2, 3, 4, 6, 12. Quants en són? "
                    "Hi ha algun altre nombre entre 1 i 20 amb tants o més?",
                ],
            },
            {
                "id": "4.3",
                "pregunta": (
                    "Entre **12, 16, 18 i 20**, quin té MÉS divisors? "
                    "Llista els divisors de cadascun i compara."
                ),
                "descripcio_pas": "Comparar quantitat de divisors de 12, 16, 18 i 20.",
                "resposta_ref": (
                    "12: {1,2,3,4,6,12} → 6 divisors. "
                    "16: {1,2,4,8,16} → 5 divisors. "
                    "18: {1,2,3,6,9,18} → 6 divisors. "
                    "20: {1,2,4,5,10,20} → 6 divisors. "
                    "12, 18 i 20 empatats amb 6 divisors cadascun (el màxim entre 1 i 20)."
                ),
                "conceptes_clau": ["6 divisors", "12", "18", "20", "empat"],
                "pistes": [
                    "Fes una taula: per a cada nombre escriu tots els divisors i compta'ls.",
                    "12→6 divisors, 16→5 divisors. Ara comprova 18 i 20.",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ #
    # CAPÍTOL 5 · Nombres primers: el mínim de divisors                    #
    # ------------------------------------------------------------------ #
    {
        "id": 5,
        "titol": "Nombres primers: el mínim de divisors",
        "emoji": "⭐",
        "introduccio": (
            "Tots els nombres tenen almenys alguns divisors. "
            "Però **quants n'hi ha com a mínim?** "
            "I si un nombre té exactament aquest mínim, com l'anomenem? "
            "Descobrim el concepte de **nombre primer**."
        ),
        "passos": [
            {
                "id": "5.1",
                "pregunta": (
                    "Calcula els divisors del nombre **1**: quants nombres el divideixen exactament? "
                    "Ara calcula els divisors del **6** (prova 6÷1, 6÷2, 6÷3, 6÷6). "
                    "Quina diferència trobes entre el 1 i qualsevol altre nombre?"
                ),
                "descripcio_pas": "Observar que el nombre 1 té 1 sol divisor i tots els altres n'han de tenir almenys 2.",
                "resposta_ref": (
                    "El nombre 1 té exactament 1 divisor (ell mateix: 1÷1=1). "
                    "El 6 té 4 divisors: 1, 2, 3, 6. "
                    "Qualsevol nombre més gran que 1 té almenys 2 divisors: l'1 i ell mateix."
                ),
                "conceptes_clau": ["1 sol divisor", "l'1", "ell mateix", "mínim 2"],
                "pistes": [
                    "Per al nombre 1: 1÷1=1 (exacta). Pots dividir 1 entre 2? Entre 3? "
                    "Quants divisors té exactament?",
                    "Per al 6: 6÷1=6 ✓, 6÷2=3 ✓, 6÷3=2 ✓, 6÷6=1 ✓. "
                    "Qualsevol nombre (>=2) sempre és divisible per l'1 i per ell mateix. "
                    "Quants divisors té com a mínim?",
                ],
            },
            {
                "id": "5.2",
                "pregunta": (
                    "Calcula tots els divisors de: **2, 4, 7, 9, 11, 15, 13**. "
                    "Quins d'ells tenen **exactament 2 divisors** (només l'1 i ell mateix)?"
                ),
                "descripcio_pas": "Identificar els nombres primers de la llista donada.",
                "resposta_ref": (
                    "2 → {1,2} = 2 divisors ✓ (primer). "
                    "4 → {1,2,4} = 3 divisors ✗. "
                    "7 → {1,7} = 2 divisors ✓ (primer). "
                    "9 → {1,3,9} = 3 divisors ✗. "
                    "11 → {1,11} = 2 divisors ✓ (primer). "
                    "15 → {1,3,5,15} = 4 divisors ✗. "
                    "13 → {1,13} = 2 divisors ✓ (primer)."
                ),
                "conceptes_clau": ["2, 7, 11, 13", "exactament 2 divisors", "1 i ell mateix"],
                "pistes": [
                    "Comprova el 4: 4÷2=2 (exacta!). Té un divisor més a part de l'1 i del 4. "
                    "I el 7: 7÷2, 7÷3, 7÷4, 7÷5, 7÷6... cap surt exacte.",
                    "Nombres amb exactament 2 divisors: només divisibles per l'1 i per ells mateixos, "
                    "i per cap altre nombre. De la llista, quins compleixen això?",
                ],
            },
            {
                "id": "5.3",
                "pregunta": (
                    "Els nombres que tenen exactament 2 divisors s'anomenen **nombres primers**. "
                    "Explica amb les teves pròpies paraules, com si li ho expliquessis a un amic/a "
                    "que no sap res de matemàtiques, **què és un nombre primer**. "
                    "Posa un exemple concret."
                ),
                "descripcio_pas": "Definir nombre primer amb paraules pròpies i un exemple.",
                "resposta_ref": (
                    "Un nombre primer és aquell que només es pot dividir exactament per dos nombres: "
                    "l'1 i ell mateix. Per exemple, el 7 només és divisible entre 1 i entre 7; "
                    "si proves de dividir-lo entre 2, 3, 4, 5 o 6 no surt exacte."
                ),
                "conceptes_clau": ["només divisible per 1 i ell mateix", "exemple", "exactament 2 divisors"],
                "pistes": [
                    "Pensa en el 13: per quins nombres el pots dividir exactament? "
                    "Intenta explicar-ho a partir d'aquest exemple.",
                    "Un nombre primer és especial perquè 'no el pots partir' en trossos iguals "
                    "excepte si uses l'1 o el nombre sencer. Com ho explicaries?",
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
