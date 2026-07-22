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
| ASK_VENDOR_ID | Alexa Developer Console -> Settings -> Vendor Information | M28OYE72P3JDUA |
| ASK_ACCESS_TOKEN | Da `~/.ask/cli_config` -> profiles.default.token.access_token | Atza\|... |
| ASK_REFRESH_TOKEN | Da `~/.ask/cli_config` -> profiles.default.token.refresh_token | Atzr\|... |
| SKILL_ID | Dopo il primo deploy automatico (viene stampato nel workflow) | amzn1.ask.skill.xxxx |

### Come ottenere i token ASK CLI (da Hermes)

I token ASK CLI sono già configurati su Hermes in `~/.ask/cli_config`. Per estrarli:

```bash
# Vendor ID
grep vendor_id ~/.ask/cli_config | head -1 | cut -d'"' -f4

# Access Token
grep -A1 access_token ~/.ask/cli_config | head -2 | tail -1 | cut -d'"' -f4

# Refresh Token
grep -A1 refresh_token ~/.ask/cli_config | head -2 | tail -1 | cut -d'"' -f4
```

> ⚠️ **Primo deploy**: il workflow creerà la skill automaticamente. Dopo il primo run, prendi il **Skill ID** dall'output del workflow e salvalo come `SKILL_ID` per gli aggiornamenti successivi.

## Come impostare i secrets

1. Vai su https://github.com/andreaschiona/alexa-fv-monitor/settings/secrets/actions
2. Clicca New repository secret
3. Inserisci nome e valore per ogni secret
