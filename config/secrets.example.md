# GitHub Secrets Setup

Questo file documenta i secret necessari per il deploy. NON committare mai valori reali.

## AWS Secrets

| Secret | Dove trovarlo | Formato |
|---|---|---|
| AWS_ACCESS_KEY_ID | AWS IAM -> Users -> Security credentials | AKIA... |
| AWS_SECRET_ACCESS_KEY | AWS IAM -> Users -> Security credentials | Lunga stringa |
| AWS_REGION | AWS Console in alto a destra | eu-west-1 |

## WiseSolar Secrets

| Secret | Dove trovarlo | Formato |
|---|---|---|
| FV_USER | Email WiseSolar Plus | email@esempio.com |
| FV_PASS | Password WiseSolar Plus | Stringa |
| FV_STATION_ID | WiseSolar app -> Info stazione | 3680 (default) |

## Alexa / ASK CLI Secrets

Per il deploy automatico della skill Alexa tramite ASK CLI in GitHub Actions.

| Secret | Dove trovarlo | Formato |
|---|---|---|
| ASK_VENDOR_ID | Alexa Developer Console -> Settings -> Vendor ID | Numerico |
| ASK_CLIENT_ID | Amazon Developer Console -> Login with Amazon -> Security Profile | amzn1.application-oa2-client.xxxx |
| ASK_CLIENT_SECRET | Amazon Developer Console -> Login with Amazon -> Security Profile | Stringa |
| SKILL_ID | Dopo il primo deploy automatico (viene stampato nel workflow) | amzn1.ask.skill.xxxx |

### Come ottenere i credential ASK CLI

1. Vai su https://developer.amazon.com/loginwithamazon/console/applist.html
2. Clicca **Create a New Security Profile**
3. Nome: `ASK CLI` (o simile)
4. Dopo la creazione, clicca **Manage** e poi **Web Settings**
5. In **Allowed Return URLs** aggiungi: `https://alexa.amazon.com/api/skill/lifecycle`
6. In **Allowed Origins** aggiungi: `https://alexa.amazon.com`
7. Prendi **Client ID** e **Client Secret** e salvali come `ASK_CLIENT_ID` e `ASK_CLIENT_SECRET`
8. Trova il tuo **Vendor ID** su https://developer.amazon.com/alexa/console/ask -> Settings -> Vendor Information
9. Salva come `ASK_VENDOR_ID`

> ⚠️ **Primo deploy**: il workflow creerà la skill automaticamente. Dopo il primo run, prendi il **Skill ID** dall'output del workflow e salvalo come `SKILL_ID` per gli aggiornamenti successivi.

## Come impostare i secrets

1. Vai su https://github.com/andreaschiona/alexa-fv-monitor/settings/secrets/actions
2. Clicca New repository secret
3. Inserisci nome e valore per ogni secret
