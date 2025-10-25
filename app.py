import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import json

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# --- Configurazione Iniziale ---
st.set_page_config(
    page_title="Ad-Visor",
    page_icon="📹",
    layout="wide"
)

# Configura la chiave API di Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Chiave API di Gemini non trovata. Assicurati di averla impostata nel file .env")
    st.stop()


def carica_vincoli_culturali(paese):
    """Carica le linee guida culturali da un file JSON."""
    if not paese or paese == "Nessuna selezione specifica":
        return None
    filename = f"cultural_guidelines/{paese.lower().replace(' ', '_')}.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        st.warning(f"File di linee guida per '{paese}' non trovato.")
        return None
    except Exception as e:
        st.error(f"Errore nel caricamento del file JSON per '{paese}': {e}")
        return None

def visualizza_risultati_strutturati(risultati):
    """
    Funzione per visualizzare l'output JSON in modo formattato su Streamlit.
    """
    try:
        data = json.loads(risultati)

        # 1. Mostra il verdetto complessivo
        verdetto = data.get("verdetto_complessivo", "NON_DEFINITO")
        motivazione_verdetto = data.get("motivazione_verdetto", "Nessuna motivazione fornita.")

        st.markdown("---")
        st.subheader("Verdetto Complessivo")

        if verdetto == "CONSIGLIATO":
            st.success(f"✅ **Consigliato:** {motivazione_verdetto}")
        elif verdetto == "CONSIGLIATO_CON_RISERVA":
            st.warning(f"⚠️ **Consigliato con Riserva:** {motivazione_verdetto}")
        elif verdetto == "NON_CONSIGLIATO":
            st.error(f"❌ **Non Consigliato:** {motivazione_verdetto}")
        else:
            st.info(f"ℹ️ **Verdetto non definito:** {motivazione_verdetto}")

        # 2. Mostra la checklist di analisi
        st.markdown("---")
        st.subheader("Checklist di Analisi Dettagliata")

        checklist = data.get("checklist_analisi", [])
        if not checklist:
            st.write("Nessun dettaglio fornito nella checklist.")
            return

        for item in checklist:
            categoria = item.get("categoria", "Senza Categoria")
            status = item.get("status", "INFO")
            punto_analizzato = item.get("punto_analizzato", "N/A")
            motivazione_item = item.get("motivazione", "N/A")

            with st.expander(f"{categoria}: {punto_analizzato}", expanded=status != "OK"):
                if status == "OK":
                    st.markdown(f"**Status:** <span style='color:green;'>✅ OK</span>", unsafe_allow_html=True)
                elif status == "ATTENZIONE":
                    st.markdown(f"**Status:** <span style='color:orange;'>⚠️ ATTENZIONE</span>", unsafe_allow_html=True)
                elif status == "CRITICO":
                    st.markdown(f"**Status:** <span style='color:red;'>❌ CRITICO</span>", unsafe_allow_html=True)
                
                st.markdown(f"**Motivazione:** {motivazione_item}")

    except json.JSONDecodeError:
        st.error("Errore: L'output del modello non è un JSON valido. Visualizzazione del testo grezzo:")
        st.code(risultati)
    except Exception as e:
        st.error(f"Si è verificato un errore durante la visualizzazione dei risultati: {e}")
        st.code(risultati)


def main():
    """Funzione principale per l'applicazione Ad-Visor."""
    with st.sidebar:
        st.title("Ad-Visor")
        st.markdown("---")
        scelta_tool = st.radio(
            "Seleziona uno strumento:",
            ("Video Checker", "Report Hub (Disabilitato)")
        )
        st.markdown("---")
        st.info("Ad-Visor è il tuo assistente AI per l'analisi pre-lancio di contenuti video pubblicitari.")

    st.title("📹 Ad-Visor: Analisi Video con AI")

    if scelta_tool == "Video Checker":
        video_checker_tool()
    elif scelta_tool == "Report Hub (Disabilitato)":
        tool_disabilitato()

def video_checker_tool():
    """Funzione per lo strumento di analisi video."""
    st.header("🔍 Video Checker")
    st.write("Carica un video per analizzare aspetti culturali, DE&I e potenziali problematiche di comunicazione.")

    video_caricato = st.file_uploader("Scegli un file video", type=["mp4", "mov", "avi", "mkv"])

    st.markdown("---")
    st.subheader("Impostazioni di Analisi Avanzata (Opzionale)")

    paesi_disponibili = ["Nessuna selezione specifica", "Italia", "Giappone", "Cina", "Stati Uniti", "Arabia Saudita"]
    paese_selezionato = st.selectbox(
        "Seleziona un mercato di riferimento per un'analisi culturale mirata:", 
        paesi_disponibili
    )

    controlli_personalizzati = st.text_area(
        "Aggiungi controlli personalizzati (uno per riga):", 
        placeholder="Esempio: Non deve contenere simboli cristiani.\nEsempio: Verificare che il logo sia sempre visibile."
    )

    st.markdown("---")

    if video_caricato is not None:
        st.video(video_caricato)

        if st.button("Analizza il Video"):
            with st.spinner("Analisi in corso... Questo processo potrebbe richiedere alcuni minuti."):
                try:
                    with open(video_caricato.name, "wb") as f:
                        f.write(video_caricato.getbuffer())

                    video_file = genai.upload_file(path=video_caricato.name, display_name="video_da_analizzare")
                    while video_file.state.name == "PROCESSING":
                        st.write("In attesa che il video venga processato dal sistema...")
                        time.sleep(5)
                        video_file = genai.get_file(video_file.name)
                    
                    if video_file.state.name == "FAILED":
                        st.error(f"Elaborazione del video fallita: {video_file.state}")
                        st.stop()

                    # --- NUOVO PROMPT PER OUTPUT STRUTTURATO (JSON) ---
                    prompt_template = f"""
                    Sei "Ad-Visor", un consulente esperto di marketing e comunicazione globale.
                    Analizza attentamente il video fornito.
                    La tua risposta DEVE essere unicamente un blocco di codice JSON valido, senza testo o markdown prima o dopo.

                    Il JSON deve avere la seguente struttura:
                    {{
                      "verdetto_complessivo": "...",
                      "motivazione_verdetto": "...",
                      "checklist_analisi": [
                        {{
                          "categoria": "...",
                          "punto_analizzato": "...",
                          "status": "...",
                          "motivazione": "..."
                        }}
                      ]
                    }}

                    SPIEGAZIONE DEI CAMPI:
                    - "verdetto_complessivo": Deve essere una di queste tre stringhe: "CONSIGLIATO", "CONSIGLIATO_CON_RISERVA", "NON_CONSIGLIATO".
                    - "motivazione_verdetto": Una frase che riassume il perché del verdetto complessivo.
                    - "checklist_analisi": Una lista di oggetti, ognuno rappresentante un punto di analisi.
                      - "categoria": L'area di analisi (es. "Analisi Culturale", "DE&I", "Rilevamento Rischi", "Controlli Personalizzati").
                      - "punto_analizzato": Lo specifico aspetto esaminato (es. "Uso di simboli religiosi", "Rappresentazione di genere").
                      - "status": Deve essere una di queste tre stringhe: "OK", "ATTENZIONE", "CRITICO".
                      - "motivazione": Spiegazione dettagliata del perché è stato assegnato quello status.

                    ISTRUZIONI PER L'ANALISI:
                    1.  **Analisi Generale:** Valuta aspetti culturali, DE&I e rischi generali. Per ciascuno, crea una voce nella checklist.
                    2.  **Analisi Specifica per Paese (se richiesta):** Se sono fornite le linee guida per un paese, usale per creare voci specifiche nella checklist nella categoria "Analisi Culturale - {paese_selezionato}".
                    3.  **Controlli Personalizzati (se richiesti):** Per ogni controllo personalizzato fornito, crea una voce nella checklist nella categoria "Controlli Personalizzati".

                    ---
                    INFORMAZIONI PER L'ANALISI CORRENTE:
                    - Paese di Riferimento: {paese_selezionato}
                    - Linee Guida Specifiche: {carica_vincoli_culturali(paese_selezionato) or "Nessuna"}
                    - Controlli Personalizzati dall'Utente: {controlli_personalizzati or "Nessuno"}
                    ---

                    Ora analizza il video e fornisci l'output JSON.
                    """

                    model = genai.GenerativeModel(model_name="gemini-flash-latest")
                    response = model.generate_content(
                        [prompt_template, video_file], 
                        request_options={'timeout': 600}
                    )
                    
                    # Rimuove eventuali ```json ... ``` dal testo della risposta
                    clean_response_text = response.text.strip().replace("```json", "").replace("```", "")

                    st.success("Analisi completata!")
                    st.subheader("Risultati dell'Analisi di Ad-Visor")
                    
                    # Usa la nuova funzione per visualizzare i risultati
                    visualizza_risultati_strutturati(clean_response_text)

                    genai.delete_file(video_file.name)
                    os.remove(video_caricato.name)

                except Exception as e:
                    st.error(f"Si è verificato un errore durante l'analisi: {e}")

def tool_disabilitato():
    """Funzione per la sezione disabilitata."""
    st.header("📊 Report Hub")
    st.warning("Questa funzionalità non è ancora attiva.")
    st.info("Qui potrai visualizzare e gestire i report delle analisi precedenti.")

if __name__ == "__main__":
    main()