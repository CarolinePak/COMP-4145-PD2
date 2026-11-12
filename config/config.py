# config/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_ENDPOINT = os.getenv(
    "API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions"
)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-luna")

# Only query Streamlit secrets when a secrets file exists. This keeps local
# previews quiet while retaining support for local and hosted secrets files.
secrets_files = [
    Path(__file__).resolve().parents[1] / ".streamlit" / "secrets.toml",
    Path.home() / ".streamlit" / "secrets.toml",
]
if any(path.is_file() for path in secrets_files):
    try:
        import streamlit as st

        API_KEY = st.secrets.get("API_KEY", API_KEY)
        API_ENDPOINT = st.secrets.get("API_ENDPOINT", API_ENDPOINT)
        MODEL_NAME = st.secrets.get("MODEL_NAME", MODEL_NAME)
    except Exception:
        pass

# Application Configuration
APP_TITLE = "SkinInsight"
APP_ICON = ":material/flare:"

# File Paths
DATA_DIR = "data"
USERS_DIR = os.path.join(DATA_DIR, "users")
ANALYSES_DIR = os.path.join(DATA_DIR, "analyses")

# API Settings
API_TIMEOUT = 30  # seconds
API_MAX_RETRIES = 3
API_MAX_TOKENS = 1500

# Image Settings
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]

# Session Settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds
