# ➗ Tutor de Divisibilitat (1r d'ESO)

Un tutor de matemàtiques **conversacional**, en català, que ensenya la
**divisibilitat** a alumnes de 1r d'ESO (12-13 anys) pel mètode socràtic:
no dóna mai la solució, sinó que guia l'alumne amb preguntes i pistes.
Funciona amb l'**API de Gemini** (Google).

## Els 5 capítols

| # | Capítol | Idea clau |
|---|---------|-----------|
| 1 | Múltiples: 12 de 3, o 3 de 12? | Què és un múltiple (A÷B exacta) |
| 2 | Divisors i múltiples de 15 | Divisors (finits) vs múltiples (infinits) |
| 3 | Múltiple de 2 i de 3... és de 6? | Divisibilitat combinada |
| 4 | Pocs o molts divisors (1–20) | Comparar quantitat de divisors |
| 5 | Nombres primers | El mínim de divisors → definició de primer |

## Arquitectura (v2 — conversacional)

Inspirada en els projectes germans `tutor-ic` i `tutor-grups`: **una sola
crida al model per torn** (`tutor_turn`), no un classificador per torn.

```
problems.py            → contingut: 5 capítols, passos, respostes de referència, pistes
prompts/tutor_system_v2.md → system prompt (plantilla amb placeholders {{...}})
llm.py                 → tutor_turn(capitol, posició, transcript) → reply + acció
tutor.py               → màquina d'estats (capítol/pas, transcript, transicions)
app.py                 → interfície Streamlit (xat, botons Pista/Acabar, progrés)
test_tutor.py          → 72 comprovacions, sense clau d'API (stub del model)
```

Com funciona un torn:

1. El model rep **la conversa del capítol com a `contents` multi-torn** de
   Gemini (no un text aplanat), amb un **marcador de posició**
   (`[Posició actual: Capítol C de 5 · Pas P de N]`) anteposat a l'últim
   missatge de l'alumne com a font de veritat.
2. El model respon amb **text natural per a l'alumne** + el separador
   literal `---CONTROL---` + un JSON `{"action": "stay"|"advance"}`.
3. **Python decideix el control flow**: manté el pas/capítol i, quan el
   model fa `advance` més enllà de l'últim pas d'un capítol, obre el
   capítol següent (el model mai salta de capítol pel seu compte).

Per què aquest disseny: l'avaluació torn-a-torn aïllada (la v1) rebutjava
respostes correctes dites amb el vocabulari que la pròpia conversa havia
construït. Jutjar la conversa sencera ho evita. (Veure els `CHANGELOG` de
`tutor-ic` per al registre d'aquest canvi en el projecte original.)

## Instal·lació

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="la_teva_clau"   # gratis a aistudio.google.com/apikey
streamlit run app.py
```

Sense `GEMINI_API_KEY`, l'app s'obre igualment en un **mode de reserva**
(avaluació senzilla per paraules clau, sense IA) per provar el flux.

### Opcions

```bash
export GEMINI_MODEL=gemini-2.5-flash   # default (ràpid i econòmic)
# export GEMINI_MODEL=gemini-2.5-pro   # més qualitat, més car i lent
```

Mode debug: afegeix `?debug=1` a la URL per veure l'estat intern, l'últim
`raw_output` del model i el rastre de la sessió.

## Tests

```bash
python3 test_tutor.py   # 72 comprovacions, ~instantani, sense clau d'API
```

## Notes de robustesa (apreses dels projectes germans)

- **`max_output_tokens = 8000`**: Gemini 2.5 Flash compta els tokens de
  raonament intern dins del pressupost; un sostre baix trunca la resposta
  abans del separador de control.
- **Reintents amb backoff** per a errors transitoris de l'API (503, 429…).
- **Invariants del transcript** (alterna tutor/student, acaba en student):
  torns consecutius del mateix rol confonen el model i li fan malgastar el
  pressupost de sortida. Si l'API falla, es retira el torn de l'alumne per
  no trencar l'alternança al reintent.
- **Parseig defensiu** del control block: qualsevol cosa rara → `stay`.

## Personalització

- Preguntes/pistes → `problems.py`.
- To i regles pedagògiques del tutor → `prompts/tutor_system_v2.md`.
- Model → variable d'entorn `GEMINI_MODEL`.
