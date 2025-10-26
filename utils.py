# utils.py
import streamlit as st
import google.generativeai as genai
import json
import os
import time
from dotenv import load_dotenv

def configure_gemini():
    """Carica le variabili d'ambiente e configura l'API di Gemini."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    else:
        st.error("Chiave API di Gemini non trovata. Assicurati di averla impostata nel file .env")
        st.stop()
        return False

def upload_and_process_video(uploaded_file, display_name="video"):
    """
    Salva, carica, processa e restituisce un file video per Gemini.
    Gestisce anche la pulizia del file locale.
    """
    file_gemini = None
    local_path = uploaded_file.name
    try:
        with open(local_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write(f"Caricamento di '{display_name}'...")
        file_gemini = genai.upload_file(path=local_path, display_name=display_name)
        
        st.write(f"Processamento di '{display_name}'...")
        while file_gemini.state.name == "PROCESSING":
            time.sleep(5)
            file_gemini = genai.get_file(file_gemini.name)
        
        if file_gemini.state.name == "FAILED":
            st.error(f"Elaborazione del video '{display_name}' fallita.")
            return None
            
        return file_gemini
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

def carica_vincoli_culturali(paese):
    """Carica le linee guida culturali da un file JSON."""
    if not paese or paese == "Nessuna selezione specifica": return None
    filename = f"cultural_guidelines/{paese.lower().replace(' ', '_')}.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        st.warning(f"File di linee guida per '{paese}' non trovato.")
        return None

# --- Funzioni di Visualizzazione ---

def _display_single_analysis(analysis_data):
    """Funzione helper per visualizzare una singola analisi."""
    verdetto = analysis_data.get("verdetto_complessivo", "N/D")
    motivazione_verdetto = analysis_data.get("motivazione_verdetto", "N/A")

    if verdetto == "CONSIGLIATO": st.success(f"✅ **Consigliato:** {motivazione_verdetto}")
    elif verdetto == "CONSIGLIATO_CON_RISERVA": st.warning(f"⚠️ **Consigliato con Riserva:** {motivazione_verdetto}")
    elif verdetto == "NON_CONSIGLIATO": st.error(f"❌ **Non Consigliato:** {motivazione_verdetto}")

    checklist = analysis_data.get("checklist_analisi", [])
    for item in checklist:
        with st.expander(f"{item.get('categoria', '')}: {item.get('punto_analizzato', '')}", expanded=item.get('status') != "OK"):
            status = item.get('status')
            if status == "OK": st.markdown(f"**Status:** <span style='color:green;'>✅ OK</span>", unsafe_allow_html=True)
            elif status == "ATTENZIONE": st.markdown(f"**Status:** <span style='color:orange;'>⚠️ ATTENZIONE</span>", unsafe_allow_html=True)
            elif status == "CRITICO": st.markdown(f"**Status:** <span style='color:red;'>❌ CRITICO</span>", unsafe_allow_html=True)
            st.markdown(f"**Motivazione:** {item.get('motivazione', 'N/A')}")

def visualizza_analisi_persuasiva(data_persuasiva):
    st.markdown("---")
    st.subheader("🧠 Analisi dell'Efficacia Persuasiva")
    with st.expander("Modello AIDA (Attenzione, Interesse, Desiderio, Azione)", expanded=True):
        aida = data_persuasiva.get("modello_aida", {})
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**Attenzione:** {'✅' if aida.get('attenzione', {}).get('presente') else '❌'}")
            st.caption(aida.get('attenzione', {}).get('motivazione', 'N/D'))
        with col2:
            st.markdown(f"**Interesse:** {'✅' if aida.get('interesse', {}).get('presente') else '❌'}")
            st.caption(aida.get('interesse', {}).get('motivazione', 'N/D'))
        with col3:
            st.markdown(f"**Desiderio:** {'✅' if aida.get('desiderio', {}).get('presente') else '❌'}")
            st.caption(aida.get('desiderio', {}).get('motivazione', 'N/D'))
        with col4:
            st.markdown(f"**Azione:** {'✅' if aida.get('azione', {}).get('presente') else '❌'}")
            st.caption(aida.get('azione', {}).get('motivazione', 'N/D'))

def visualizza_notizie_recenti(data_notizie):
    st.markdown("---")
    st.subheader("📰 Notizie Recenti Rilevanti")
    
    prodotto = data_notizie.get("prodotto_identificato", "N/A")
    st.info(f"**Prodotto/Servizio identificato:** {prodotto}")
    
    notizie = data_notizie.get("notizie_rilevanti", [])
    if notizie:
        st.markdown("**🌐 Notizie trovate in rete:**")
        for i, notizia in enumerate(notizie, 1):
            if isinstance(notizia, dict):
                impatto = notizia.get('impatto', 'NEUTRO')
                rilevanza = notizia.get('rilevanza', 'MEDIA')
                titolo = notizia.get('titolo', 'N/A')
                descrizione = notizia.get('descrizione', 'N/A')
                
                # Container per ogni notizia
                with st.container():
                    if impatto == 'POSITIVO':
                        st.markdown(f"""<div style='background-color: #d4edda; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 10px;'>
                        <h4 style='margin: 0; color: #155724;'>📰 Notizia #{i} - Impatto {impatto} ({rilevanza} rilevanza)</h4>
                        <h5 style='margin: 5px 0; color: #155724;'>✅ {titolo}</h5>
                        <p style='margin: 5px 0; color: #155724;'>{descrizione}</p>
                        <small style='color: #6c757d;'>🔍 Fonte: Ricerca web recente</small>
                        </div>""", unsafe_allow_html=True)
                    elif impatto == 'NEGATIVO':
                        st.markdown(f"""<div style='background-color: #f8d7da; padding: 15px; border-radius: 10px; border-left: 5px solid #dc3545; margin-bottom: 10px;'>
                        <h4 style='margin: 0; color: #721c24;'>📰 Notizia #{i} - Impatto {impatto} ({rilevanza} rilevanza)</h4>
                        <h5 style='margin: 5px 0; color: #721c24;'>❌ {titolo}</h5>
                        <p style='margin: 5px 0; color: #721c24;'>{descrizione}</p>
                        <small style='color: #6c757d;'>🔍 Fonte: Ricerca web recente</small>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style='background-color: #d1ecf1; padding: 15px; border-radius: 10px; border-left: 5px solid #17a2b8; margin-bottom: 10px;'>
                        <h4 style='margin: 0; color: #0c5460;'>📰 Notizia #{i} - Impatto {impatto} ({rilevanza} rilevanza)</h4>
                        <h5 style='margin: 5px 0; color: #0c5460;'>ℹ️ {titolo}</h5>
                        <p style='margin: 5px 0; color: #0c5460;'>{descrizione}</p>
                        <small style='color: #6c757d;'>🔍 Fonte: Ricerca web recente</small>
                        </div>""", unsafe_allow_html=True)
    else:
        st.info("🔍 Nessuna notizia rilevante trovata nella ricerca web recente.")
    
    # Raccomandazioni strategiche dettagliate
    raccomandazioni = data_notizie.get("raccomandazioni_strategiche", {})
    if raccomandazioni:
        st.subheader("🎯 Raccomandazioni Strategiche")
        
        timing = raccomandazioni.get("timing_lancio", "")
        if timing == "PROCEDI":
            st.success(f"✅ **Timing di Lancio:** {timing} - Via libera per il lancio")
        elif timing == "ATTENDI":
            st.warning(f"⏳ **Timing di Lancio:** {timing} - Considera di posticipare")
        elif timing == "MODIFICA_PRIMA":
            st.error(f"✏️ **Timing di Lancio:** {timing} - Modifiche necessarie prima del lancio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            opportunita = raccomandazioni.get("opportunita_da_sfruttare", [])
            if opportunita:
                st.markdown("**🚀 Opportunità da Sfruttare:**")
                for opp in opportunita:
                    st.write(f"• {opp}")
            
            modifiche = raccomandazioni.get("modifiche_consigliate", [])
            if modifiche:
                st.markdown("**✏️ Modifiche Consigliate:**")
                for mod in modifiche:
                    st.write(f"• {mod}")
        
        with col2:
            rischi = raccomandazioni.get("rischi_da_mitigare", [])
            if rischi:
                st.markdown("**⚠️ Rischi da Mitigare:**")
                for rischio in rischi:
                    st.write(f"• {rischio}")
        
        strategia = raccomandazioni.get("strategia_comunicazione", "")
        if strategia:
            st.info(f"**💬 Strategia di Comunicazione:** {strategia}")

def visualizza_analisi_performance(data_performance):
    st.markdown("---")
    st.subheader("📈 Analisi Performance Video")
    
    # Previsione engagement
    engagement = data_performance.get("previsione_engagement", {})
    livello_eng = engagement.get("livello", "MEDIO")
    if livello_eng == "ALTO":
        st.success(f"🚀 **Engagement Previsto:** {livello_eng}")
    elif livello_eng == "BASSO":
        st.error(f"📉 **Engagement Previsto:** {livello_eng}")
    else:
        st.warning(f"📈 **Engagement Previsto:** {livello_eng}")
    st.write(engagement.get("motivazione", "N/A"))
    
    # Potenziale virale
    virale = data_performance.get("potenziale_virale", {})
    prob_virale = virale.get("probabilita", "MEDIA")
    col1, col2 = st.columns(2)
    
    with col1:
        if prob_virale == "ALTA":
            st.success(f"✨ **Potenziale Virale:** {prob_virale}")
        elif prob_virale == "BASSA":
            st.error(f"🚫 **Potenziale Virale:** {prob_virale}")
        else:
            st.info(f"🎯 **Potenziale Virale:** {prob_virale}")
        
        fattori = virale.get("fattori_chiave", [])
        if fattori:
            st.markdown("**Fattori Chiave:**")
            for fattore in fattori:
                st.write(f"• {fattore}")
    
    with col2:
        # Metriche previste
        metriche = data_performance.get("metriche_previste", {})
        st.markdown("**📊 Metriche Previste:**")
        if metriche.get("view_rate"):
            st.write(f"**View Rate:** {metriche.get('view_rate')}")
        if metriche.get("completion_rate"):
            st.write(f"**Completion Rate:** {metriche.get('completion_rate')}")
        if metriche.get("share_potential"):
            st.write(f"**Share Potential:** {metriche.get('share_potential')}")
    
    # Ottimizzazioni per piattaforma
    st.subheader("📱 Ottimizzazioni per Piattaforma")
    ottimizzazioni = data_performance.get("ottimizzazioni_consigliate", {})
    
    tab1, tab2, tab3, tab4 = st.tabs(["Facebook", "Instagram", "TikTok", "YouTube"])
    
    with tab1:
        facebook_tips = ottimizzazioni.get("per_facebook", [])
        for tip in facebook_tips:
            st.write(f"• {tip}")
    
    with tab2:
        instagram_tips = ottimizzazioni.get("per_instagram", [])
        for tip in instagram_tips:
            st.write(f"• {tip}")
    
    with tab3:
        tiktok_tips = ottimizzazioni.get("per_tiktok", [])
        for tip in tiktok_tips:
            st.write(f"• {tip}")
    
    with tab4:
        youtube_tips = ottimizzazioni.get("per_youtube", [])
        for tip in youtube_tips:
            st.write(f"• {tip}")
    
    # Insight strategici
    insights = data_performance.get("insight_strategici", [])
    if insights:
        st.subheader("💡 Insight Strategici")
        for insight in insights:
            st.info(f"• {insight}")

def visualizza_risultati_checker(risultati):
    try:
        if isinstance(risultati, str):
            data = json.loads(risultati)
        else:
            data = risultati
            
        if not isinstance(data, dict):
            raise ValueError("I dati non sono nel formato dizionario atteso")
        st.subheader("Risultati dell'Analisi di Ad-Visor")
        _display_single_analysis(data)
        if "analisi_persuasiva" in data:
            visualizza_analisi_persuasiva(data["analisi_persuasiva"])
        if "notizie_recenti" in data:
            visualizza_notizie_recenti(data["notizie_recenti"])
        if "analisi_performance" in data:
            visualizza_analisi_performance(data["analisi_performance"])
    except Exception as e:
        st.error(f"Errore nella visualizzazione dei risultati: {e}")
        st.code(risultati)

def visualizza_risultati_benchmark(risultati):
    try:
        if isinstance(risultati, str):
            data = json.loads(risultati)
        else:
            data = risultati
            
        if not isinstance(data, dict):
            raise ValueError("I dati non sono nel formato dizionario atteso")
        
        # Header principale
        st.title("📊 Report Comparativo")
        
        # Sezione confronto diretto
        st.header("⚖️ Confronto Diretto")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Il Tuo Video")
            tuo_video = data.get("analisi_tuo_video", {})
            verdetto_tuo = tuo_video.get("verdetto_complessivo", "N/D")
            if verdetto_tuo == "CONSIGLIATO":
                st.success(f"✅ {verdetto_tuo}")
            elif verdetto_tuo == "CONSIGLIATO_CON_RISERVA":
                st.warning(f"⚠️ {verdetto_tuo}")
            else:
                st.error(f"❌ {verdetto_tuo}")
            st.write(tuo_video.get("motivazione_verdetto", "N/A"))
            
        with col2:
            st.markdown("### 🏢 Video Competitor")
            comp_video = data.get("analisi_video_competitor", {})
            verdetto_comp = comp_video.get("verdetto_complessivo", "N/D")
            if verdetto_comp == "CONSIGLIATO":
                st.success(f"✅ {verdetto_comp}")
            elif verdetto_comp == "CONSIGLIATO_CON_RISERVA":
                st.warning(f"⚠️ {verdetto_comp}")
            else:
                st.error(f"❌ {verdetto_comp}")
            st.write(comp_video.get("motivazione_verdetto", "N/A"))
        
        # Analisi SWOT strutturata
        st.header("🎯 Analisi SWOT Strategica")
        comparativa = data.get("analisi_comparativa", {})
        
        # Matrice SWOT 2x2
        swot_col1, swot_col2 = st.columns(2)
        
        with swot_col1:
            # Punti di Forza
            with st.container():
                st.markdown("#### 💪 **STRENGTHS** (Punti di Forza)")
                st.markdown("<div style='background-color: #d4edda; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                for item in comparativa.get("punti_di_forza_tuo", []):
                    st.markdown(f"• {item}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("")
            
            # Debolezze
            with st.container():
                st.markdown("#### ⚠️ **WEAKNESSES** (Aree di Miglioramento)")
                st.markdown("<div style='background-color: #fff3cd; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                for item in comparativa.get("aree_di_miglioramento_tuo", []):
                    st.markdown(f"• {item}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        with swot_col2:
            # Opportunità
            with st.container():
                st.markdown("#### 🚀 **OPPORTUNITIES** (Opportunità)")
                st.markdown("<div style='background-color: #cce5ff; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                for item in comparativa.get("opportunita_mercato", []):
                    st.markdown(f"• {item}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("")
            
            # Minacce
            with st.container():
                st.markdown("#### 🚨 **THREATS** (Minacce)")
                st.markdown("<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                for item in comparativa.get("minacce_competitor", []):
                    st.markdown(f"• {item}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Raccomandazione finale
        st.header("💡 Raccomandazione Strategica")
        st.info(comparativa.get('raccomandazione_strategica', 'N/A'))
        
        # Tabella comparativa
        st.header("📊 Tabella Comparativa")
        tabella_comp = data.get("tabella_comparativa", [])
        if tabella_comp:
            import pandas as pd
            
            table_data = []
            for item in tabella_comp:
                if isinstance(item, dict):
                    caratteristica = item.get('caratteristica', 'N/A')
                    tuo_video_check = "✅" if item.get('tuo_video', False) else "❌"
                    competitor_check = "✅" if item.get('competitor', False) else "❌"
                    table_data.append({
                        'Caratteristica': caratteristica,
                        'Il Tuo Video': tuo_video_check,
                        'Competitor': competitor_check
                    })
            
            if table_data:
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.write("Nessun dato comparativo disponibile")
        else:
            st.write("Tabella comparativa non disponibile")
                    
    except Exception as e:
        st.error(f"Errore nella visualizzazione dei risultati: {e}")
        st.code(risultati)