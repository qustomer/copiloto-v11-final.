import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import hashlib, json
from fpdf import FPDF
from duckduckgo_search import DDGS

# =========================================================
# IDENTIDAD SOBERANA
# =========================================================
ID_SOBERANA = "Claudio Falasca Consultor"
VERSION = "Heptágono SF v12.0"

EJES = [
    "Político-Institucional",
    "Socio-Territorial",
    "Económico-Financiero",
    "Técnico-Minero",
    "Ambiental-Ecosistémico",
    "Hídrico-Soberano",
    "Comunicacional-Estratégico"
]

st.set_page_config(page_title=VERSION, layout="wide")

# =========================================================
# ESTILO MIDNIGHT GOLD
# =========================================================
st.markdown("""
<style>
.stApp { background:#05070a; color:#e5e7eb }
[data-testid="stSidebar"] { background:#0e1117 }
.hash-footer { color:#6b7280; font-family:monospace; text-align:center }
</style>
""", unsafe_allow_html=True)

# =========================================================
# PDF REAL (C22)
# =========================================================
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial","B",12)
        self.cell(0,10,f"{ID_SOBERANA} — Executive Summary",0,1,"C")

def generar_pdf(data, firma):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.multi_cell(0,8,f"Proyecto: {data['proyecto']}")
    pdf.multi_cell(0,8,f"Territorio: {data['territorio']}")
    pdf.multi_cell(0,8,f"ICR: {data['icr']} | ROI: {data['roi']}")

    pdf.ln(4)
    pdf.multi_cell(0,8,"Scores Heptágono:")
    for eje,val in data["scores"].items():
        pdf.cell(0,8,f"{eje}: {val}",ln=True)

    pdf.ln(6)
    pdf.multi_cell(0,8,f"Firma MD5: {firma}")
    return pdf.output(dest="S").encode("latin-1")

# =========================================================
# OSINT REAL (C18)
# =========================================================
def osint_busqueda(territorio):
    noticias=[]
    with DDGS() as ddgs:
        for r in ddgs.text(f"minería {territorio} conflicto", max_results=5):
            noticias.append(r["title"])
    return noticias

# =========================================================
# LAYOUT 3 COLUMNAS OCD
# =========================================================
st.title(f"🏛️ {ID_SOBERANA}")
col1,col2,col3 = st.columns([1,2,1])

# ================= COLUMNA CONTROL =================
with col1:
    proyecto = st.text_input("Proyecto","Josemaría")
    territorio = st.text_input("Territorio","San Juan")
    roi = st.slider("ROI (%)",0,60,30)

    st.subheader("Auditoría Heptágono")
    scores={}
    for eje in EJES:
        scores[eje]=st.slider(eje,0,100,60)

# ================= COLUMNA VISUAL =================
with col2:
    fig = go.Figure(go.Scatterpolar(
        r=list(scores.values()),
        theta=EJES,
        fill="toself",
        line_color="#D4AF37"
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white")
    st.plotly_chart(fig,use_container_width=True)

# ================= COLUMNA AUDITORÍA =================
with col3:
    icr = 100 - scores["Socio-Territorial"]
    st.metric("ICR",icr)

    noticias = osint_busqueda(territorio)
    for n in noticias:
        st.warning(n)

# =========================================================
# PAYLOAD FORENSE + HASH DETERMINISTA
# =========================================================
payload={
    "owner":ID_SOBERANA,
    "version":VERSION,
    "proyecto":proyecto,
    "territorio":territorio,
    "scores":scores,
    "ICR":icr,
    "ROI":roi,
    "OSINT":noticias
}

firma = hashlib.md5(json.dumps(payload,sort_keys=True).encode()).hexdigest()

# =========================================================
# GUARDIA MLC
# =========================================================
if icr>70 and roi>30:
    st.error("🚫 BLOQUEO ÉTICO MLC")
    st.stop()

# =========================================================
# GENERAR PDF REAL
# =========================================================
if st.button("📄 Generar PDF"):
    pdf_bytes=generar_pdf(
        {"proyecto":proyecto,"territorio":territorio,"icr":icr,"roi":roi,"scores":scores},
        firma
    )
    st.download_button("Descargar Reporte",pdf_bytes,file_name=f"Reporte_{firma[:8]}.pdf")

st.markdown(f"<div class='hash-footer'>Hash Forense: {firma}</div>",unsafe_allow_html=True)
