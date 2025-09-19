
import streamlit as st
import json
from app import scoring, filters, explain, data_loader

st.set_page_config(page_title="Buscador de Financiación Climática EU", layout="wide")

# Sidebar form
st.sidebar.header("📋 Perfil del proyecto")
temas = st.sidebar.multiselect("Áreas temáticas", ["clima","energía","energía renovable","economía circular","resiliencia","agricultura regenerativa"])
trl = st.sidebar.slider("Nivel de madurez (TRL)", 1, 9, 5)
regiones = st.sidebar.multiselect("Regiones de impacto", ["África","LatAm","Asia","MENA","global EM"])
org_type = st.sidebar.multiselect("Tipo de organización", ["startup","SME","ONG","cooperativa","universidad"])
instrumentos = st.sidebar.multiselect("Instrumentos preferidos", ["grant","equity","convertible","TA/tech-assistance","blended"])
ticket = st.sidebar.number_input("Monto solicitado (€)", min_value=50000, max_value=2000000, step=50000)
cofin = st.sidebar.selectbox("¿Tienes cofinanciación?", ["Sí","No"])

if st.sidebar.button("🔍 Buscar financiación"):
    proyecto = {
        "temas": temas,
        "TRL": trl,
        "regiones_objetivo": regiones,
        "org_type": org_type,
        "instrumentos_preferidos": instrumentos,
        "ticket_solicitado": ticket,
        "cofin": cofin == "Sí"
    }

    actors = data_loader.load_actors()
    matches = []

    for actor in actors:
        if filters.passes_hard_filters(actor, proyecto):
            final_score = scoring.calculate_final_score(actor, proyecto)
            why = explain.why_fit(actor, proyecto)
            actor["puntuacion_final"] = final_score
            actor["justificacion"] = why
            matches.append(actor)

    if matches:
        matches = sorted(matches, key=lambda x: x["puntuacion_final"], reverse=True)
        st.success(f"✅ ¡Encontramos {len(matches)} opciones de financiación para tu proyecto!")

        for actor in matches:
            with st.container():
                st.subheader(f"{actor['actor']} — {actor['puntuacion_final']}%")
                st.caption(f"{actor['categoria']} • Tickets {actor['ticket_min_eur']}–{actor['ticket_max_eur']}€")
                st.text(f"Instrumentos: {', '.join(actor['instrumentos'])}")
                st.text(f"Regiones cubiertas: {', '.join(actor['mercados_objetivo'][:3])}")

                # Elegibility bullets
                crits = actor.get("criterios_elegibilidad", {})
                for k,v in list(crits.items())[:3]:
                    st.markdown(f"✓ {k}: {v}")

                st.markdown(f"💡 Por qué encaja: {actor['justificacion']}")

                evids = actor.get("evidencias", [])
                if evids:
                    st.markdown("📄 Evidencias recientes:")
                    for ev in evids[:2]:
                        st.markdown(f"- [{ev['tipo']}]({ev['fuente']})")

                with st.expander("Ver detalles de puntuación"):
                    st.json(actor.get("puntuacion_componentes", {}))
