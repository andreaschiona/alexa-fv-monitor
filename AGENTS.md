# alexa-fv-monitor -- Agent Instructions

## STOP -- Read This First

You are handling a  slash command. You MUST:
1. Parse the command from the triggering comment (analyze, plan, fix, implement, fixCheck, review).
2. Execute ONLY that command's behavior as defined below.
3. For  and : POST A COMMENT ONLY. Do NOT edit files, create branches, or PRs.
4. For : push a branch only. Do NOT create a PR.
5. For : this is the ONLY command that creates a PR.

If the command is  or , your job is DONE after posting one comment.
Do NOT touch any source code files for analyze or plan commands.

## IMPORTANT: Auto-update disabled

The  option in  is set to .

## Project Overview

This project is an Alexa Custom Skill + AWS Lambda for monitoring a WiseSolar Plus
solar photovoltaic installation. It reads data from WiseSolar cloud API and returns
voice responses via Alexa.

## Architecture

-  - Lambda handler (Alexa intents -> responses)
-  - WiseSolar API client (AES-ECB auth)
-  - AWS SAM template
-  - pytest tests

## Verified Commands

| Action | Command |
|--------|---------|
| Build  |  |
| Test   |  |
| Lint   |  |

## Environment

- Python 3.12
- Dependencies: pyaes (AES encryption)
- AWS Lambda runtime

## OpenCode Protocol

The agent MUST handle slash-commands found in issue or PR comments.

### Dispatch Table

| Command | Scope | Behaviour |
|---------|-------|-----------|
|  | Issue | Apply a quick fix. Push branch only. No PR. |
|  | Issue | Post analysis as comment only. |
|  | Issue | Post technical plan as comment only. |
|  | Issue | Create branch, implement, open PR with . |
|  | PR | Fix CI failures on existing PR. |
|  | PR | Code review + fix CI failures. |

### CRITICAL RULES

-  and  MUST ONLY post a comment.
-  MUST NOT create a PR.
-  is the ONLY command that creates a PR.
- Execute EXACTLY ONE command per invocation.

### Model Overrides

| Keyword | Model |
|---------|-------|
|  |  |
|  |  |
| (default) |  |

## Commit Convention

-  -- new feature
-  -- bug fix
-  -- maintenance
-  or  -- breaking changes

## Branch Naming

Branches:  from .

## Security Rules

- NEVER commit real credentials (API keys, passwords, tokens)
- All secrets go in GitHub Secrets
- Use environment variables at runtime
-  documents required secrets
