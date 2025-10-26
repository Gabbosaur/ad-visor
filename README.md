# 📹 Ad-Visor

**Il tuo assistente AI per l'analisi strategica dei video pubblicitari**

Ad-Visor è un'applicazione web sviluppata con Streamlit che utilizza l'intelligenza artificiale di Google Gemini per analizzare video pubblicitari e fornire insight strategici per ottimizzare le campagne marketing.

## 🚀 Funzionalità Principali

### 🔍 Video Checker
Analizza un singolo video per:
- **Aspetti culturali e DE&I**: Verifica la sensibilità culturale e l'inclusività
- **Analisi persuasiva**: Valuta l'efficacia secondo il modello AIDA e i principi di Cialdini
- **Notizie recenti**: Ricerca notizie web che potrebbero impattare il brand/prodotto
- **Performance prediction**: Predice engagement e potenziale virale sui social media
- **Ottimizzazioni per piattaforma**: Consigli specifici per Facebook, Instagram, TikTok, YouTube

### 📊 Competitive Benchmark
Confronta il tuo video con quello di un competitor:
- **Analisi SWOT**: Punti di forza, debolezze, opportunità e minacce
- **Tabella comparativa**: Confronto feature-by-feature con 15+ caratteristiche chiave
- **Raccomandazioni strategiche**: Consigli per superare la concorrenza

### 📊 Report Hub
(In sviluppo) Gestione e visualizzazione delle analisi precedenti

## 🛠️ Tecnologie Utilizzate

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini (gemini-flash-latest)
- **Data Processing**: Pandas, JSON
- **Environment**: Python 3.8+

## 📋 Prerequisiti

- Python 3.8 o superiore
- Chiave API di Google Gemini
- Connessione internet per l'analisi AI

## ⚙️ Installazione

1. **Clona il repository**
```bash
git clone <repository-url>
cd ad-visor
```

2. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

3. **Configura l'API Key**
Crea un file `.env` nella root del progetto:
```env
GEMINI_API_KEY="la_tua_chiave_api_gemini"
```

4. **Avvia l'applicazione**
```bash
streamlit run app.py
```

## 📁 Struttura del Progetto

```
ad-visor/
├── app.py                      # Homepage principale
├── utils.py                    # Funzioni di utilità e visualizzazione
├── requirements.txt            # Dipendenze Python
├── .env                       # Variabili d'ambiente (API keys)
├── pages/                     # Pagine Streamlit
│   ├── 1_video_checker.py     # Tool di analisi video singolo
│   ├── 2_competitive_benchmark.py  # Tool di confronto competitivo
│   └── 3_report_hub.py        # Hub dei report (in sviluppo)
├── cultural_guidelines/       # Linee guida culturali per paese
│   ├── italia.json
│   ├── giappone.json
│   ├── cina.json
│   ├── stati_uniti.json
│   └── arabia_saudita.json
└── images/                    # Risorse grafiche
```

## 🎯 Come Usare Ad-Visor

### Video Checker
1. Carica un video (formati supportati: MP4, MOV, AVI, MKV)
2. Seleziona le opzioni di analisi avanzata:
   - Mercato di riferimento per analisi culturale
   - Controlli personalizzati
   - Analisi persuasiva (AIDA)
   - Ricerca notizie recenti
   - Analisi performance
3. Clicca "Analizza il Video"
4. Visualizza i risultati strutturati con verdetto e raccomandazioni

### Competitive Benchmark
1. Carica il tuo video e quello del competitor
2. Configura le impostazioni di analisi
3. Avvia l'analisi comparativa
4. Esamina la matrice SWOT e la tabella comparativa

## 🌍 Mercati Supportati

- Italia
- Giappone
- Cina
- Stati Uniti
- Arabia Saudita

Ogni mercato ha linee guida culturali specifiche per un'analisi mirata.

## 📊 Output dell'Analisi

### Verdetti Possibili
- ✅ **CONSIGLIATO**: Video pronto per il lancio
- ⚠️ **CONSIGLIATO CON RISERVA**: Modifiche minori consigliate
- ❌ **NON CONSIGLIATO**: Modifiche sostanziali necessarie

### Sezioni del Report
- **Checklist di Analisi**: Controlli dettagliati per categoria
- **Analisi Persuasiva**: Valutazione AIDA e principi di neuromarketing
- **Notizie Recenti**: Context awareness del mercato
- **Performance Prediction**: Metriche previste e ottimizzazioni
- **Raccomandazioni Strategiche**: Consigli actionable

## 🔧 Configurazione Avanzata

### Controlli Personalizzati
Aggiungi controlli specifici per il tuo brand:
```
Non deve contenere loghi di competitor
Verificare che il logo sia sempre visibile
Controllare la pronuncia del brand name
```

### Linee Guida Culturali
Personalizza i file JSON in `cultural_guidelines/` per aggiungere nuovi mercati o modificare le regole esistenti.

## 🚨 Limitazioni

- Dimensione massima file video: dipende dai limiti di Google Gemini
- Tempo di elaborazione: 2-5 minuti per video complessi
- Formati supportati: MP4, MOV, AVI, MKV
- Richiede connessione internet stabile

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 📞 Supporto

Per supporto, bug report o richieste di feature, apri un issue su GitHub.

---

**Ad-Visor** - Trasforma i tuoi video pubblicitari in campagne di successo con l'intelligenza artificiale! 🚀