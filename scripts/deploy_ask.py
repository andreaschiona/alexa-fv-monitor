#!/usr/bin/env python3
"""Deploy Alexa Skill via 'ask deploy --target skill-package'.
Handles both first deploy (create) and updates.
Injects Lambda ARN into skill.json before deploy."""
import json, os, subprocess, sys

SKILL_ID = os.environ.get("SKILL_ID", "")
LAMBDA_ARN = os.environ.get("LAMBDA_ARN", "")

# 1. If SKILL_ID is known (from GitHub Secrets), write it to .ask/config
#    so 'ask deploy' knows to UPDATE instead of CREATE.
if SKILL_ID:
    ask_dir = ".ask"
    ask_config_path = os.path.join(ask_dir, "config")
    os.makedirs(ask_dir, exist_ok=True)
    cfg = {
        "profiles": {
            "default": {
                "skillMetadata": {
                    "type": "SKILL_PACKAGE"
                },
                "skillId": SKILL_ID
            }
        }
    }
    with open(ask_config_path, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Set skill ID in .ask/config: {SKILL_ID}")
else:
    print(f"NO SKILL_ID set — first deploy mode (will create new skill)")

# 2. Inject Lambda ARN into skill.json
skill_json_path = "skill-package/skill.json"
with open(skill_json_path) as f:
    skill_data = json.load(f)

if LAMBDA_ARN:
    endpoint = skill_data.get("manifest", {}).get("apis", {}).get("custom", {}).get("endpoint", {})
    if endpoint:
        old_uri = endpoint.get("uri", "")
        if old_uri != LAMBDA_ARN:
            print(f"URI: {old_uri[:40]}... -> {LAMBDA_ARN[:40]}...")
            endpoint["uri"] = LAMBDA_ARN
            with open(skill_json_path, "w") as f:
                json.dump(skill_data, f, indent=2)
            print("skill.json updated with Lambda ARN")
    else:
        print("WARNING: No endpoint in skill.json")
else:
    print("WARNING: LAMBDA_ARN not set, using existing URI")

# 3. Run ask deploy
print(f"\n=== ask deploy --target skill-package ===")
result = subprocess.run(
    ["ask", "deploy", "--target", "skill-metadata", "interaction-model", "--debug"],
    capture_output=True, text=True
)

out = result.stdout.strip()
err = result.stderr.strip()
if out:
    print(f"[OUT] {out[:2000]}")
if err:
    print(f"[ERR] {err[:1000]}", file=sys.stderr)

if result.returncode != 0:
    print(f"ask deploy FAILED (exit {result.returncode})")
    sys.exit(result.returncode)

print("ask deploy succeeded")

# 4. Extract Skill ID from .ask/config (created/updated by ask deploy)
ask_config_path = ".ask/config"
if os.path.exists(ask_config_path):
    with open(ask_config_path) as f:
        ask_cfg = json.load(f)
    sid = ask_cfg.get("profiles", {}).get("default", {}).get("skillId", "")
    if sid:
        SKILL_ID = sid
        print(f"\nSkill ID: {SKILL_ID}")
    else:
        print("\nWARNING: No skillId in .ask/config")

# 5. Export Skill ID for GitHub Actions
github_output = os.environ.get("GITHUB_OUTPUT", "")
if github_output and SKILL_ID:
    with open(github_output, "a") as out:
        out.write(f"skill_id={SKILL_ID}\n")
    print(f"Exported skill_id={SKILL_ID} to GITHUB_OUTPUT")

if not SKILL_ID:
    print("\n=== FAILED: No Skill ID ===")
    sys.exit(1)
else:
    print(f"\n=== SUCCESS ===")
    print(f"Skill ID: {SKILL_ID}")
    if not os.environ.get("SKILL_ID"):
        print("=" * 50)
        print(">>> IMPORTANT: Save as GitHub Secret 'SKILL_ID' <<<")
        print("=" * 50)


