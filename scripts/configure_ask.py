#!/usr/bin/env python3
"""Configure ASK CLI credentials from environment variables."""
import json, os

ask_dir = os.path.expanduser("~/.ask")
os.makedirs(ask_dir, exist_ok=True)

cfg = {
    "profiles": {
        "default": {
            "vendor_id": os.environ["ASK_VENDOR_ID"],
            "token": {
                "access_token": os.environ["ASK_ACCESS_TOKEN"],
                "refresh_token": os.environ["ASK_REFRESH_TOKEN"],
                "token_type": "bearer",
                "expires_in": 3600,
            },
        }
    },
    "machine_id": "github-actions",
}

path = os.path.join(ask_dir, "cli_config")
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)

print(f"ASK CLI configured for vendor: {cfg['profiles']['default']['vendor_id']}")
