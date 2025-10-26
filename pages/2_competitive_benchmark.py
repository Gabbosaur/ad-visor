# pages/2_Competitive_Benchmark.py
import streamlit as st
import utils
import google.generativeai as genai

# Configura API e titolo pagina
st.set_page_config(page_title="Competitive Benchmark", page_icon="📊")
utils.configure_gemini()

st.header("📊 Competitive Benchmark")
st.write("Confronta il tuo video con quello di un competitor per ottenere un'analisi strategica e una SWOT.")

col1, col2 = st.columns(2)
video_tuo = col1.file_uploader("Carica il tuo video", key="your_video", type=["mp4", "mov"])
video_competitor = col2.file_uploader("Carica video del competitor", key="competitor_video", type=["mp4", "mov"])

st.markdown("---")
with st.expander("Impostazioni di Analisi (applicate a entrambi)"):
    paesi = ["Nessuna selezione specifica", "Italia", "Giappone", "Cina", "Stati Uniti", "Arabia Saudita"]
    paese_sel = st.selectbox("Seleziona un mercato di riferimento:", paesi)
    controlli_pers = st.text_area("Aggiungi controlli personalizzati (uno per riga):")

st.markdown("---")

if video_tuo and video_competitor:
    if st.button("Avvia Analisi Comparativa"):
        with st.spinner("Analisi comparativa in corso... Potrebbe richiedere più tempo del normale."):
            file_tuo, file_comp = None, None
            try:
                file_tuo = utils.upload_and_process_video(video_tuo, "Il Tuo Video")
                file_comp = utils.upload_and_process_video(video_competitor, "Video Competitor")

                if file_tuo and file_comp:
                    prompt_completo = f"""
                    Sei Ad-Visor, un Senior Marketing Strategist. Hai due video da analizzare: "Il Tuo Video" e "Video del Competitor".
                    La tua risposta DEVE essere unicamente un blocco JSON valido.

                    STRUTTURA JSON RICHIESTA:
                    {{
                        "analisi_tuo_video": {{"verdetto_complessivo": "...", "motivazione_verdetto": "..."}},
                        "analisi_video_competitor": {{"verdetto_complessivo": "...", "motivazione_verdetto": "..."}},
                        "tabella_comparativa": [
                            {{"caratteristica": "Logo/Brand visibile e riconoscibile", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Call-to-Action chiara e specifica", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Hook iniziale coinvolgente (primi 3 sec)", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Storytelling/Narrativa strutturata", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Testimonial/Persone reali", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Dimostrazione prodotto/servizio", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Sottotitoli/Testo sovrapposto", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Musica/Audio di qualità", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Qualità video professionale", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Elementi di scarsità/urgenza", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Benefici chiari del prodotto", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Riprova sociale (recensioni/numeri)", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Finale memorabile/impattante", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Adatto al target demografico", "tuo_video": true/false, "competitor": true/false}},
                            {{"caratteristica": "Ottimizzato per mobile/social", "tuo_video": true/false, "competitor": true/false}}
                        ],
                        "analisi_comparativa": {{
                            "punti_di_forza_tuo": ["Punto di forza 1", "..."],
                            "aree_di_miglioramento_tuo": ["Debolezza 1", "..."],
                            "opportunita_mercato": ["Opportunità 1", "..."],
                            "minacce_competitor": ["Minaccia 1", "..."],
                            "raccomandazione_strategica": "Consiglio finale..."
                        }}
                    }}
                    
                    INFO PER L'ANALISI:
                    - Mercato Target: {paese_sel}
                    - Linee Guida Culturali: {utils.carica_vincoli_culturali(paese_sel) or "Nessuna"}
                    - Controlli Personalizzati: {controlli_pers or "Nessuno"}

                    Analizza entrambi i video e fornisci il report comparativo JSON.
                    """
                    
                    model = genai.GenerativeModel(model_name="gemini-flash-latest")
                    response = model.generate_content(
                        [prompt_completo, "Il Tuo Video:", file_tuo, "Video del Competitor:", file_comp], 
                        request_options={'timeout': 900}
                    )
                    
                    clean_response_text = response.text.strip().replace("```json", "").replace("```", "")
                    st.success("Analisi comparativa completata!")
                    utils.visualizza_risultati_benchmark(clean_response_text)

            except Exception as e:
                st.error(f"Si è verificato un errore durante l'analisi: {e}")
            finally:
                if file_tuo: genai.delete_file(file_tuo.name)
                if file_comp: genai.delete_file(file_comp.name)