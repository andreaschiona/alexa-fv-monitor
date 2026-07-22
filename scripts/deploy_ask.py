#!/usr/bin/env python3
"""Deploy Alexa Skill Model via SMAPI (no ask-resources.json needed)."""
import json, os, subprocess, sys

SKILL_ID = os.environ.get("SKILL_ID", "")

def run_ask(args: list[str]) -> dict:
    """Run an `ask smapi` command and return parsed JSON + status."""
    full_cmd = ["ask", "smapi"] + args
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    out = result.stdout.strip()
    err = result.stderr.strip()
    if out:
        print(f"[OUT] {out[:500]}")
    if err:
        print(f"[ERR] {err[:500]}", file=sys.stderr)
    print(f"[exit] {result.returncode}")
    parsed = {}
    if out:
        try:
            parsed = json.loads(out)
        except json.JSONDecodeError:
            pass
    return {"code": result.returncode, "parsed": parsed, "raw_out": out, "raw_err": err}

# 1. Read skill manifest
skill_json_path = "skill-package/skill.json"
with open(skill_json_path) as f:
    manifest = json.load(f)

# 2. Read interaction model
interaction_path = "skill-package/interactionModels/custom/it-IT.json"
with open(interaction_path) as f:
    interaction_model = json.load(f)

if not SKILL_ID:
    # --- CREATE new skill ---
    print("=== Creating new skill ===")
    r = run_ask([
        "create-skill",
        "--manifest", json.dumps(manifest),
        "--vendor-id", os.environ.get("ASK_VENDOR_ID", ""),
    ])
    if r["code"] != 0:
        print("FAILED to create skill")
        sys.exit(r["code"])

    # Extract skill ID from response
    sid = r["parsed"].get("skillId", "")
    if not sid:
        # Try to extract from raw response
        for key in ["skillId", "id", "skill_id"]:
            if key in r["parsed"]:
                sid = r["parsed"][key]
                break
    if sid:
        SKILL_ID = sid
        print(f"Created skill: {SKILL_ID}")
    else:
        print(f"Could not extract skill ID from response: {r['raw_out'][:200]}")
        sys.exit(1)
else:
    # --- UPDATE existing skill ---
    print(f"=== Updating skill {SKILL_ID} ===")
    r = run_ask([
        "update-skill",
        "--skill-id", SKILL_ID,
        "--manifest", json.dumps(manifest),
    ])
    if r["code"] != 0:
        print(f"FAILED to update skill (non-fatal, may already be up to date)")
        # Don't exit — try interaction model anyway

# 3. Deploy interaction model
print(f"=== Deploying interaction model for {SKILL_ID} ===")
r = run_ask([
    "update-interaction-model",
    "--skill-id", SKILL_ID,
    "--locale", "it-IT",
    "--interaction-model", json.dumps(interaction_model),
])
if r["code"] != 0:
    print("FAILED to update interaction model")
    sys.exit(r["code"])

# 4. Save skill ID to .ask/config for future runs
os.makedirs(".ask", exist_ok=True)
with open(".ask/config", "w") as f:
    json.dump({
        "profiles": {
            "default": {
                "skillId": SKILL_ID,
            }
        }
    }, f, indent=2)
print(f"Saved skill ID to .ask/config")

# 5. Export skill ID for GitHub Actions
github_output = os.environ.get("GITHUB_OUTPUT", "")
if github_output:
    with open(github_output, "a") as out:
        out.write(f"skill_id={SKILL_ID}\n")
    print(f"Exported skill_id={SKILL_ID} to GITHUB_OUTPUT")

print(f"\n=== SUCCESS ===")
print(f"Skill ID: {SKILL_ID}")
if not os.environ.get("SKILL_ID"):
    print("=" * 60)
    print(">>> IMPORTANT: Save this Skill ID as GitHub Secret SKILL_ID <<<")
    print("=" * 60)
