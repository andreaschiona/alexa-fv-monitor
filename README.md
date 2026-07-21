# Alexa FV Monitor

Alexa Custom Skill + AWS Lambda per monitoraggio fotovoltaico WiseSolar Plus.

## Architettura

"Alexa, chiedi a FV Monitor la produzione"
         |
         v
+---------------------------+
|  Alexa Skills Kit (ASK)   |
|  Invocation: "fv monitor" |
+---------------------------+
         |
         v
+---------------------------+
|  AWS Lambda (Python 3.12) |
|  - Login AES-ECB WiseSolar|
|  - Fetch dati real-time   |
|  - Risposta speech text   |
+---------------------------+
         |
         v
WiseSolar Cloud API

## Comandi vocali

| Frase Alexa | Risposta |
|---|---|
| "Alexa, chiedi a FV Monitor la produzione" | "L impianto sta producendo 1800 watt. Oggi hai generato 12.5 kWh" |
| "Alexa, chiedi a FV Monitor lo stato" | "Impianto normale. Produzione 1800 W, consumo casa 500 W" |
| "Alexa, chiedi a FV Monitor il consumo" | "Oggi hai consumato 8.3 kWh" |
| "Alexa, chiedi a FV Monitor quanto ho guadagnato" | "Oggi hai guadagnato 2.15 euro" |

## Setup

### Requisiti
- Account AWS (free tier)
- Account Amazon Developer (per Alexa Skills)
- Credenziali WiseSolar Plus

### Deploy
1. Configura i GitHub Secrets (vedi config/secrets.example.md)
2. Push su master -> il workflow deploy.yml fa il deploy automatico
3. Crea la Alexa Skill in developer.amazon.com -> collega la Lambda

### GitHub Secrets richiesti

| Secret | Descrizione |
|---|---|
| AWS_ACCESS_KEY_ID | Chiave API AWS |
| AWS_SECRET_ACCESS_KEY | Secret key AWS |
| AWS_REGION | Regione AWS (es. eu-west-1) |
| FV_USER | Email WiseSolar |
| FV_PASS | Password WiseSolar |
| FV_STATION_ID | ID stazione (default: 3680) |

## Licenza
MIT
# Deploy test Tue Jul 21 23:24:43 CEST 2026
# Deploy test Tue Jul 21 23:25:11 CEST 2026
