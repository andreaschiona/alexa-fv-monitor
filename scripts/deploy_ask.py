#!/usr/bin/env python3
"""Deploy Alexa Skill Model: create config, inject ARN, run ask deploy, capture skill ID."""
import json, os, subprocess, sys

SKILL_ID = os.environ.get("SKILL_ID", "")

# 0. Check ask CLI version
result = subprocess.run(["ask", "--version"], capture_output=True, text=True)
print(f"ASK CLI version: {result.stdout.strip() or result.stderr.strip()}")

# 1. Generate ask-resources.json (required by ASK CLI v2 — use "src" for v1 compat)
ask_resources = {
    "askcliResourcesVersion": "2020-03-31",
    "profiles": {
        "default": {
            "skillMetadata": {
                "type": "SKILL_PACKAGE",
                "skillPackage": {
                    "path": "skill-package",
                    "src": "skill-package"
                }
            }
        }
    }
}
with open("ask-resources.json", "w") as f:
    json.dump(ask_resources, f, indent=2)

# 2. Generate .ask/config with skill ID if available
os.makedirs(".ask", exist_ok=True)
cfg = {
    "profiles": {
        "default": {
            "skillMetadata": {"type": "SKILL_PACKAGE"},
        }
    }
}
if SKILL_ID:
    cfg["profiles"]["default"]["skillId"] = SKILL_ID
    print(f"Using existing skill ID: {SKILL_ID}")
else:
    print("No SKILL_ID set — will create new skill on first deploy")

with open(".ask/config", "w") as f:
    json.dump(cfg, f, indent=2)

# 3. Inject Lambda ARN into skill.json
try:
    lambda_arn = os.environ["LAMBDA_ARN"]
except KeyError:
    print("ERROR: LAMBDA_ARN not set", file=sys.stderr)
    sys.exit(1)

skill_json_path = "skill-package/skill.json"
with open(skill_json_path) as f:
    content = f.read()

content = content.replace("LAMBDA_ARN_PLACEHOLDER", lambda_arn)

with open(skill_json_path, "w") as f:
    f.write(content)

print(f"ARN injected into skill.json: {lambda_arn}")

# 4. Run ask deploy — target only skill-metadata + interaction-model
#    (Lambda is already deployed via SAM, skip --target lambda)
result = subprocess.run(
    ["ask", "deploy", "--profile", "default",
     "--target", "skill-metadata", "interaction-model"],
    capture_output=True, text=True
)

# Print ALL output BEFORE checking exit code
if result.stdout:
    print(f"[ASK stdout]\n{result.stdout}")
if result.stderr:
    print(f"[ASK stderr]\n{result.stderr}", file=sys.stderr)
print(f"[ASK exit code] {result.returncode}")

if result.returncode != 0:
    sys.exit(result.returncode)

# 5. Capture new skill ID
try:
    with open(".ask/config") as f:
        cfg = json.load(f)
    sid = cfg.get("profiles", {}).get("default", {}).get("skillId", "")
    if sid:
        github_output = os.environ.get("GITHUB_OUTPUT", "")
        if github_output:
            with open(github_output, "a") as out:
                out.write(f"skill_id={sid}\n")
        print(f"Skill ID: {sid}")
        if not SKILL_ID:
            print("=" * 60)
            print(">>> IMPORTANT: Save this Skill ID as GitHub Secret SKILL_ID <<<")
            print("=" * 60)
except Exception as e:
    print(f"Could not capture skill ID: {e}")
