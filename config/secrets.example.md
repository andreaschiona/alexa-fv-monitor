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

## Come impostare i secrets

1. Vai su https://github.com/andreaschiona/alexa-fv-monitor/settings/secrets/actions
2. Clicca New repository secret
3. Inserisci nome e valore per ogni secret
