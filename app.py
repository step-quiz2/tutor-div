"""
app.py · Interfície Streamlit del Tutor de Divisibilitat (arquitectura v2).

Executa amb:   streamlit run app.py

Flux de cada torn (igual que els tutors germans):
  1. afegim el missatge de l'alumne al transcript,
  2. cridem llm.tutor_turn amb el transcript del capítol,
  3. si l'API falla, treiem el missatge de l'alumne (per no trencar
     l'alternança) i ho tractem com a incident tècnic, NO com a error,
  4. afegim el reply del tutor al transcript ABANS d'aplicar l'acció,
  5. apliquem l'acció (stay/advance) a la màquina d'estats.
"""

from __future__ import annotations

import streamlit as st

import llm
import tutor

st.set_page_config(page_title="Tutor de Divisibilitat", page_icon="➗",
                   layout="centered")

st.markdown(
    """
    <style>
    .block-container { max-width: 760px; }
    [data-testid="stChatMessage"] { border-radius: 16px; font-size: 1.2rem; }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span { font-size: 1.2rem; }
    .stChatInput textarea { font-size: 1.2rem !important; }
    h2 { color: #1f4e79; font-size: 1.44rem !important; }
    p, li, label, .stMarkdown { font-size: 1.2rem; }
    .barra { background:#eef2f7; border-radius:10px; height:12px;
             overflow:hidden; margin:4px 0 10px 0; }
    .barra > div { background:linear-gradient(90deg,#4f8df9,#6fc3a0); height:100%; }
    .petit { color:#6b7280; font-size:1.02rem; }

    /* ── Codi de colors: mode determinista (Python) vs heurístic (IA) ── */
    .mode-badge {
        display:inline-block; font-size:.82rem; font-weight:700;
        padding:2px 10px; border-radius:999px; margin-bottom:8px;
        letter-spacing:.02em;
    }
    .mode-ai { background:#ede9fe; color:#5b21b6; border:1px solid #c4b5fd; }
    .mode-py { background:#d1fae5; color:#065f46; border:1px solid #6ee7b7; }
    /* Vora esquerra de color a la bombolla segons el mode */
    .stChatMessage:has(.mode-ai) { border-left:5px solid #8b5cf6; }
    .stChatMessage:has(.mode-py) { border-left:5px solid #10b981; }
    .llegenda { display:flex; gap:14px; flex-wrap:wrap; margin:2px 0 6px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ───────────────────────────── estat de sessió ────────────────────────── #

if "state" not in st.session_state:
    st.session_state.state = None  # None = encara no s'ha començat


def reinicia():
    st.session_state.state = None

# ─────────────────────────────── sidebar ──────────────────────────────── #

with st.sidebar:
    if llm.ia_disponible():
        st.success(f"IA connectada ✓ ({llm.MODEL})")
    else:
        st.warning(
            "Sense `GEMINI_API_KEY`: mode de **reserva** (avaluació "
            "senzilla, sense IA). Defineix la variable d'entorn i recarrega "
            "per a l'experiència completa."
        )

    st.markdown(
        '<div class="llegenda">'
        '<span class="mode-badge mode-ai">🤖 IA</span>'
        '<span class="mode-badge mode-py">🐍 Python</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    state = st.session_state.state
    if state is not None:
        st.divider()
        if state["finished"]:
            st.success("Tots els capítols completats! 🎉")
        else:
            cap = tutor.capitol_actual(state)
            pas_num = state["pas_idx"] + 1
            total_passos = len(cap["passos"])
            frac = (state["cap_idx"] + (pas_num - 1) / total_passos) / tutor.total_capitols()
            st.markdown(
                f"**Capítol {state['cap_idx']+1}/{tutor.total_capitols()}** · "
                f"pregunta {pas_num}/{total_passos}"
            )
            st.markdown(
                f'<div class="barra"><div style="width:{frac*100:.0f}%"></div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<span class="petit">{cap["emoji"]} {cap["titol"]}</span>',
                unsafe_allow_html=True,
            )

    st.divider()
    if st.button("🔄 Tornar a començar", use_container_width=True):
        reinicia()
        st.rerun()

    with st.expander("Com funciona?"):
        st.markdown(
            "- El tutor et fa preguntes i tu respons al quadre de baix.\n"
            "- No et donarà la solució: t'ajudarà amb **pistes**.\n"
            "- Si et quedes encallat, prem **💡 Pista**.\n"
            "- Pots equivocar-te tantes vegades com calgui."
        )


# ─────────────────────────────── capçalera ────────────────────────────── #

st.title("Tutor de Divisibilitat")


# ─────────────────────────── pantalla d'inici ─────────────────────────── #

if st.session_state.state is None:
    st.info(tutor.MISSATGE_BENVINGUDA)
    if st.button("🚀 Comença", type="primary", use_container_width=True):
        st.session_state.state = tutor.new_session()
        st.rerun()
    st.stop()

state = st.session_state.state


# ─────────────────────────── historial del xat ────────────────────────── #

for m in state["display"]:
    if m["role"] == "tutor":
        source = m.get("source", "ai")
        if source == "py":
            avatar, role = "🐍", "assistant"
            badge = '<span class="mode-badge mode-py">🐍 Python</span>'
        else:
            avatar, role = "🧑‍🏫", "assistant"
            badge = '<span class="mode-badge mode-ai">🤖 IA</span>'
        with st.chat_message(role, avatar=avatar):
            st.markdown(badge, unsafe_allow_html=True)
            st.markdown(m["content"])
    else:
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(m["content"])


# ─────────────────────────── processament d'un torn ───────────────────── #

def processa(text_alumne: str):
    state = st.session_state.state
    tutor.add_student(state, text_alumne)

    try:
        result = llm.tutor_turn(
            tutor.capitol_actual(state),
            tutor.position_dict(state),
            state["transcript"],
            cap_total=tutor.total_capitols(),
        )
    except Exception as e:
        # Incident tècnic: treiem el torn de l'alumne perquè el transcript
        # no quedi amb dos torns 'student' seguits al reintent.
        tutor.pop_last_student(state)
        st.error(
            "Ui, ara mateix no em puc connectar a la IA 😅. "
            f"Torna-ho a provar d'aquí un moment.\n\n_({e})_"
        )
        return

    # font determinista (py) si ha respost el mode de reserva; si no, IA (ai).
    font = "py" if result.get("mode") == "py" or result["n_api_calls"] == 0 else "ai"
    tutor.add_tutor(state, result["reply"], source=font)  # ABANS d'aplicar l'acció
    state["turn_count"] += 1
    state["last_raw_output"] = result["raw_output"]
    pos_abans = tutor.position_dict(state)

    trans = tutor.apply_action(state, result["action"])

    if trans == "seguent_pas":
        # El model (o el mode de reserva) NO inclou la pregunta del pas nou:
        # Python la mostra com a bombolla determinista pròpia, sempre.
        pas = tutor.pas_actual(state)
        q_canonica = f"**PREGUNTA.** {pas['pregunta']}"
        tutor.enrich_last_tutor(state, q_canonica)

    if trans == "fi":
        tutor.add_tutor(state, tutor.MISSATGE_FINAL, source="py")

    state["history"].append({
        "position_before": pos_abans,
        "action": result["action"],
        "transition": trans,
        "control_parse_ok": result["control_parse_ok"],
        "n_api_calls": result["n_api_calls"],
    })


# ─────────────────────────── entrada de l'alumne ──────────────────────── #

if not state["finished"]:
    col1, col2 = st.columns([4, 1])
    with col2:
        demana_pista = st.button("💡 Pista", use_container_width=True)
    with col1:
        acabar = st.button("🚪 Acabar", use_container_width=True)

    if demana_pista:
        with st.spinner("En Pitàgoras prepara una pista…"):
            processa(tutor.PISTA_MARKER)
        st.rerun()

    if acabar:
        state["finished"] = True
        st.rerun()

    entrada = st.chat_input("Escriu la teva resposta aquí…")
    if entrada:
        with st.spinner("En Pitàgoras hi està pensant…"):
            processa(entrada)
        st.rerun()
else:
    st.success("Has acabat. Prem «Tornar a començar» per repetir-ho. 🎉")

# Mode debug: ?debug=1 a la URL mostra l'estat intern i el rastre.
if st.query_params.get("debug") == "1":
    with st.expander("🔧 Debug"):
        st.json({
            "cap_idx": state["cap_idx"], "pas_idx": state["pas_idx"],
            "finished": state["finished"], "turn_count": state["turn_count"],
            "transcript_len": len(state["transcript"]),
        })
        st.write("Últim raw_output:")
        st.code(state.get("last_raw_output") or "(cap)")
        st.write("Rastre:")
        st.json(state["history"])
