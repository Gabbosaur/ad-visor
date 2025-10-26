# pages/1_Video_Checker.py
import streamlit as st
import utils
import google.generativeai as genai

# Configura API e titolo pagina
st.set_page_config(page_title="Video Checker", page_icon="🔍")
utils.configure_gemini()

st.header("🔍 Video Checker")
st.write("Carica un video per analizzare aspetti culturali, DE&I e potenziali problematiche di comunicazione.")

video_caricato = st.file_uploader("Scegli un file video", type=["mp4", "mov", "avi", "mkv"])
st.markdown("---")

with st.expander("Impostazioni di Analisi Avanzata (Opzionale)"):
    paesi = ["Nessuna selezione specifica", "Italia", "Giappone", "Cina", "Stati Uniti", "Arabia Saudita"]
    paese_sel = st.selectbox("Seleziona un mercato di riferimento:", paesi)
    controlli_pers = st.text_area("Aggiungi controlli personalizzati (uno per riga):", placeholder="Esempio: Non deve contenere loghi di competitor.")
    analisi_persuasiva_on = st.checkbox("Abilita Analisi dell'Efficacia Persuasiva")
    ricerca_notizie_on = st.checkbox("Abilita Ricerca Notizie Recenti")
    st.caption("Cerca notizie recenti che potrebbero impattare il prodotto/servizio presentato nel video.")
    analisi_performance_on = st.checkbox("Abilita Analisi Performance Video")
    st.caption("Analizza elementi tecnici e di engagement per predire le performance del video.")

st.markdown("---")

if video_caricato:
    st.video(video_caricato, width=300)
    if st.button("Analizza il Video"):
        with st.spinner("Analisi in corso..."):
            file_video_gemini = None
            try:
                file_video_gemini = utils.upload_and_process_video(video_caricato, "video_checker_file")
                
                if file_video_gemini:
                    # --- COSTRUZIONE DINAMICA DEL PROMPT ---
                    json_structure_extra = ""
                    istruzioni_extra = ""
                    
                    if analisi_persuasiva_on:
                        istruzioni_extra += """
4.  **Analisi dell'Efficacia Persuasiva:** Agisci come un esperto di neuromarketing. Valuta l'efficacia del video nel persuadere lo spettatore e inserisci i risultati nella chiave 'analisi_persuasiva'."""
                        json_structure_extra += ''',
                      "analisi_persuasiva": {
                        "modello_aida": {
                          "attenzione": {"presente": true/false, "motivazione": "..."},
                          "interesse": {"presente": true/false, "motivazione": "..."},
                          "desiderio": {"presente": true/false, "motivazione": "..."},
                          "azione": {"presente": true/false, "motivazione": "..."}
                        }
                      }'''
                    
                    if ricerca_notizie_on:
                        istruzioni_extra += """
5.  **Ricerca Notizie Recenti:** Identifica il prodotto/servizio/brand nel video e cerca mentalmente notizie recenti (ultimi 6 mesi) che potrebbero impattare la sua reputazione. Per ogni notizia, valuta se è POSITIVA (da sfruttare), NEGATIVA (da evitare/mitigare) o NEUTRA. Fornisci raccomandazioni strategiche specifiche su come procedere con il lancio del video considerando il contesto mediatico attuale."""
                        json_structure_extra += ''',
                      "notizie_recenti": {
                        "prodotto_identificato": "...",
                        "notizie_rilevanti": [
                          {"titolo": "...", "impatto": "POSITIVO|NEUTRO|NEGATIVO", "descrizione": "...", "rilevanza": "ALTA|MEDIA|BASSA"}
                        ],
                        "raccomandazioni_strategiche": {
                          "timing_lancio": "PROCEDI|ATTENDI|MODIFICA_PRIMA",
                          "modifiche_consigliate": ["..."],
                          "opportunita_da_sfruttare": ["..."],
                          "rischi_da_mitigare": ["..."],
                          "strategia_comunicazione": "..."
                        }
                      }'''
                    
                    if analisi_performance_on:
                        istruzioni_extra += """
6.  **Analisi Performance Video:** Agisci come un esperto di video marketing e social media analytics. Analizza elementi tecnici, di engagement e virali del video per predire le sue performance sui social media e fornire insight strategici."""
                        json_structure_extra += ''',
                      "analisi_performance": {
                        "previsione_engagement": {"livello": "ALTO|MEDIO|BASSO", "motivazione": "..."},
                        "potenziale_virale": {"probabilita": "ALTA|MEDIA|BASSA", "fattori_chiave": ["..."]},
                        "metriche_previste": {
                          "view_rate": "...",
                          "completion_rate": "...",
                          "share_potential": "..."
                        },
                        "ottimizzazioni_consigliate": {
                          "per_facebook": ["..."],
                          "per_instagram": ["..."],
                          "per_tiktok": ["..."],
                          "per_youtube": ["..."]
                        },
                        "insight_strategici": ["..."]
                      }'''

                    prompt_template = f"""
                    Sei "Ad-Visor", un consulente esperto di marketing e comunicazione globale.
                    La tua risposta DEVE essere unicamente un blocco di codice JSON valido.

                    La struttura JSON deve essere:
                    {{
                      "verdetto_complessivo": "CONSIGLIATO|CONSIGLIATO_CON_RISERVA|NON_CONSIGLIATO",
                      "motivazione_verdetto": "...",
                      "checklist_analisi": [
                        {{"categoria": "...", "punto_analizzato": "...", "status": "OK|ATTENZIONE|CRITICO", "motivazione": "..."}}
                      ]{json_structure_extra}
                    }}

                    ISTRUZIONI PER L'ANALISI:
                    1.  **Analisi Generale:** Valuta aspetti culturali, DE&I e rischi generali.
                    2.  **Analisi Specifica per Paese:** Se richiesta, applica le linee guida culturali fornite.
                    3.  **Controlli Personalizzati:** Se richiesti, verificali in modo esplicito.
                    {istruzioni_extra}

                    ---
                    INFO PER L'ANALISI:
                    - Paese di Riferimento: {paese_sel}
                    - Linee Guida Specifiche: {utils.carica_vincoli_culturali(paese_sel) or "Nessuna"}
                    - Controlli Personalizzati: {controlli_pers or "Nessuno"}
                    ---
                    Analizza il video e fornisci l'output JSON.
                    """

                    model = genai.GenerativeModel(model_name="gemini-flash-latest")
                    response = model.generate_content([prompt_template, file_video_gemini], request_options={'timeout': 600})
                    
                    clean_response_text = response.text.strip().replace("```json", "").replace("```", "")

                    st.success("Analisi completata!")
                    utils.visualizza_risultati_checker(clean_response_text)
                    
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")
            finally:
                if file_video_gemini:
                    genai.delete_file(file_video_gemini.name)