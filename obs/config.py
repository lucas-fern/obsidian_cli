# obs/config.py
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path.home() / ".obs_config.yaml"


def load_config() -> dict:
    """
    Loads config from ~/.obs_config.yaml.
    Expects structure:
      vaults:
        P: /path/to/personal/vault
        W: /path/to/work/vault
      openai_api_key: "sk-xxxxx"
    """
    if not CONFIG_PATH.exists():
        print(f"Error: Config file not found at {CONFIG_PATH}")
        sys.exit(1)
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)
