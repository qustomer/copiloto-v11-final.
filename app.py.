import streamlit as st
import hashlib
import json
from duckduckgo_search import DDGS

# =============================================================================
# C1 — IDENTIDAD SOBERANA (INMUTABLE)
# =============================================================================
IDENTIDAD_SOBERANA = "Claudio Falasca Consultor"
VERSION_SISTEMA = "Heptágono SF v11.5"

# =============================================================================
# C2 — EJES OFICIALES (NO MODIFICABLES)
# =============================================================================
EJES_OFICIALES = [
    "Político-Institucional",
    "Socio-Territorial",
    "Económico-Financiero",
    "Técnico-Minero",
    "Ambiental-Ecosistémico",
    "Hídrico-Soberano",
    "Comunicacional-Estratégico"
]

TRIADA_FRACTURA = [
    "Político-Institucional",
    "Socio-Territorial",
    "Hídrico-Soberano"
]

# =============================================================================
# VALIDACIÓN ESTRUCTURAL
# =============================================================================
def validar_integridad_ejes(scores):
    if set(scores.keys()) != set(EJES_OFICIALES):
        st.error("ERROR: Ejes inconsistentes.")
        st.stop()

# =============================================================================
# C18 — OSINT REAL CON DUCKDUCKGO (SIN API)
# =============================================================================
def ejecutar_osint_real(proyecto, territorio):

    queries = [
        f"conflicto minero {territorio}",
        f"proyecto minero {territorio} permisos",
        f"protesta minera {territorio}",
        f"litigio ambiental {territorio}",
        f"agua minería {territorio}"
    ]

    impacto = 0
    snippets = []

    palabras_criticas = ["protesta","huelga","amparo","litigio","rechazo"]
    palabras_positivas = ["aprobado","licencia","acuerdo","inversión"]

    with DDGS() as ddgs:
        for q in queries:
            resultados = ddgs.text(q, max_results=3)
            for r in resultados:
                texto = r["title"] + " " + r["body"]
                snippets.append(texto)

                if any(p in texto.lower() for p in palabras_criticas):
                    impacto -= 3
                if any(p in texto.lower() for p in palabras_positivas):
                    impacto += 2

    return impacto, snippets[:10]

# =============================================================================
# C12 — ICR OFICIAL (SIN MULTIPLICADORES)
# =============================================================================
def calcular_icr(scores):
    return 100 - scores["Socio-Territorial"]

# =============================================================================
# C16 — FRICTION INDEX MULTIEJE
# =============================================================================
def calcular_friction_index(scores):
    valores = [scores[e] for e in TRIADA_FRACTURA]
    return round(100 - sum(valores)/3, 2)

# =============================================================================
# C21 — HASH FORENSE DETERMINISTA (SIN TIMESTAMP)
# =============================================================================
def generar_hash_md5(payload):
    serial = json.dumps(payload, sort_keys=True)
    return hashlib.md5(serial.encode()).hexdigest()

# =============================================================================
# PIPELINE MAESTRO FINAL v11.5
# =============================================================================
def ejecutar_pipeline(proyecto, territorio, scores_base, roi):

    impacto_osint, evidencia = ejecutar_osint_real(proyecto, territorio)

    scores_finales = {
        k: max(0, min(100, v + (impacto_osint if k in TRIADA_FRACTURA else 0)))
        for k, v in scores_base.items()
    }

    validar_integridad_ejes(scores_finales)

    icr = calcular_icr(scores_finales)
    friction_index = calcular_friction_index(scores_finales)

    bloqueo_mlc = roi > 30 and icr > 70

    payload = {
        "owner": IDENTIDAD_SOBERANA,
        "version": VERSION_SISTEMA,
        "proyecto": proyecto,
        "territorio": territorio,
        "indicadores": {
            "scores": scores_finales,
            "ICR": icr,
            "Friction_Index": friction_index,
            "ROI": roi
        },
        "OSINT": evidencia,
        "MLC_STATUS": "BLOCKED" if bloqueo_mlc else "CLEAR"
    }

    firma = generar_hash_md5(payload)
    payload["HASH_MD5"] = firma

    return payload

# =============================================================================
# UI STREAMLIT (BLOQUEO ÉTICO CON st.stop())
# =============================================================================
st.title("Copiloto Minero — Heptágono SF v11.5")
st.caption("Risk · Territory · Evidence")

proyecto = st.text_input("Proyecto", "Proyecto Ejemplo")
territorio = st.text_input("Territorio", "San Juan")
roi = st.slider("ROI proyectado (%)", 0, 60, 25)

st.subheader("Scores iniciales")
scores_base = {}
for eje in EJES_OFICIALES:
    scores_base[eje] = st.slider(eje, 0, 100, 60)

if st.button("Ejecutar Diagnóstico"):
    payload = ejecutar_pipeline(proyecto, territorio, scores_base, roi)

    if payload["MLC_STATUS"] == "BLOCKED":
        st.error("GUARDIA MLC — DESPACHO BLOQUEADO")
        st.write("HASH INCIDENTE:", payload["HASH_MD5"])
        st.stop()

    st.success("SISTEMA VALIDADO")
    st.json(payload)
