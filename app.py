import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

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


def main():
    """
    Funzione principale per l'applicazione Ad-Visor.
    """
    # --- Sidebar ---
    with st.sidebar:
        st.title("Ad-Visor")
        st.markdown("---")
        scelta_tool = st.radio(
            "Seleziona uno strumento:",
            ("Video Checker", "Report Hub (Disabilitato)")
        )

        st.markdown("---")
        st.info("Ad-Visor è il tuo assistente AI per l'analisi pre-lancio di contenuti video pubblicitari.")

    # --- Pagina Principale ---
    st.title("📹 Ad-Visor: Analisi Video con AI")

    if scelta_tool == "Video Checker":
        video_checker_tool()
    elif scelta_tool == "Report Hub (Disabilitato)":
        tool_disabilitato()

def video_checker_tool():
    """
    Funzione per lo strumento di analisi video.
    """
    st.header("🔍 Video Checker")
    st.write("Carica un video per analizzare aspetti culturali, DE&I e potenziali problematiche di comunicazione.")

    video_caricato = st.file_uploader("Scegli un file video", type=["mp4", "mov", "avi", "mkv"])

    if video_caricato is not None:
        st.video(video_caricato)

        if st.button("Analizza il Video"):
            with st.spinner("Analisi in corso... Questo processo potrebbe richiedere alcuni minuti."):
                try:
                    # Salva temporaneamente il file per ottenere un percorso stabile
                    with open(video_caricato.name, "wb") as f:
                        f.write(video_caricato.getbuffer())

                    # Carica il video sull'API di Gemini
                    video_file = genai.upload_file(
                        path=video_caricato.name,
                        display_name="video_da_analizzare"
                    )

                    # Attendi che il file venga processato
                    while video_file.state.name == "PROCESSING":
                        st.write("In attesa che il video venga processato dal sistema...")
                        time.sleep(5)  # Attendi 5 secondi prima di controllare di nuovo
                        video_file = genai.get_file(video_file.name)

                    if video_file.state.name == "FAILED":
                        st.error(f"Elaborazione del video fallita: {video_file.state}")
                        st.stop()

                    # Prepara il prompt per l'analisi
                    prompt = """
                    Sei "Ad-Visor", un consulente esperto di marketing e comunicazione globale.
                    Analizza attentamente questo video pubblicitario e fornisci un report dettagliato basato sui seguenti punti:

                    1.  **Analisi Culturale:** Identifica elementi culturali (simboli, gesti, tradizioni, abbigliamento, ambientazioni) e valuta la loro potenziale risonanza o incomprensione in diversi mercati internazionali (es. Nord America, Europa, Asia, Medio Oriente).

                    2.  **Valutazione DE&I (Diversity, Equity & Inclusion):**
                        *   **Rappresentazione:** Come vengono rappresentati i diversi gruppi di persone (etnia, genere, età, abilità, etc.)? La rappresentazione è autentica o stereotipata?
                        *   **Inclusività:** Il messaggio e le immagini sono inclusivi? C'è il rischio che qualcuno si senta escluso o marginalizzato?

                    3.  **Rilevamento di Rischi e Controversie:**
                        *   **Contenuti Sensibili:** Rileva la presenza di violenza, linguaggio inappropriato, immagini disturbanti, o temi controversi (politici, religiosi).
                        *   **Messaggi Ambigui:** Ci sono messaggi o immagini che potrebbero essere interpretati erroneamente o in modo negativo?

                    4.  **Consigli Strategici:** Basandoti sull'analisi, fornisci suggerimenti chiari e attuabili per migliorare l'efficacia globale del video e minimizzare i rischi.

                    Fornisci una risposta ben strutturata con titoli chiari per ogni sezione.
                    """

                    # Inizializza il modello generativo e genera il contenuto
                    model = genai.GenerativeModel(model_name="gemini-flash-latest")
                    response = model.generate_content([prompt, video_file], request_options={'timeout': 600})

                    st.success("Analisi completata!")
                    st.markdown("---")
                    st.subheader("Risultati dell'Analisi di Ad-Visor")
                    st.markdown(response.text)

                    # Elimina il file per liberare spazio di archiviazione
                    genai.delete_file(video_file.name)
                    os.remove(video_caricato.name) # Rimuovi il file temporaneo locale

                except Exception as e:
                    st.error(f"Si è verificato un errore durante l'analisi: {e}")

def tool_disabilitato():
    """
    Funzione per la sezione disabilitata.
    """
    st.header("📊 Report Hub")
    st.warning("Questa funzionalità non è ancora attiva.")
    st.info("Qui potrai visualizzare e gestire i report delle analisi precedenti.")


if __name__ == "__main__":
    main()