# app.py
import streamlit as st

st.set_page_config(
    page_title="Ad-Visor | Benvenuto",
    page_icon="📹",
    layout="wide"
)

st.title("📹 Benvenuto in Ad-Visor")
st.header("Il tuo assistente AI per l'analisi strategica dei video pubblicitari.")

st.info("👈 **Seleziona uno strumento dalla sidebar a sinistra per iniziare.**")

st.markdown("""
---
### Strumenti Disponibili:

- **🔍 Video Checker:** 
  Analizza un singolo video per rischi culturali, DE&I e ne valuta l'efficacia persuasiva. Ideale per un controllo rapido e approfondito prima del lancio.

- **📊 Competitive Benchmark:** 
  Mette a confronto il tuo video con quello di un competitor per fornirti un'analisi SWOT strategica e identificare i tuoi vantaggi competitivi.

- **📊 Report Hub:** 
  _(In sviluppo)_ Visualizza e gestisci le tue analisi passate.
""")

st.sidebar.success("Seleziona un tool per iniziare.")
st.sidebar.markdown("---")
st.sidebar.info("Ad-Visor è il tuo assistente AI per l'analisi pre-lancio di contenuti video pubblicitari.")