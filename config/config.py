# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to load from Streamlit secrets first (for cloud deployment)
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        API_KEY = st.secrets.get("API_KEY", os.getenv("API_KEY", ""))
        API_ENDPOINT = st.secrets.get("API_ENDPOINT", os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions"))
        MODEL_NAME = st.secrets.get("MODEL_NAME", os.getenv("MODEL_NAME", "gpt-6-luna"))
    else:
        # Fall back to environment variables
        API_KEY = os.getenv("API_KEY", "")
        API_ENDPOINT = os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions")
        MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-luna")
except:
    # Fall back to environment variables
    API_KEY = os.getenv("API_KEY", "")
    API_ENDPOINT = os.getenv("API_ENDPOINT", "https://genai.hkbu.edu.hk/api/v1/chat/completions")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-luna")

# Application Configuration
APP_TITLE = "SkinInsight"
APP_ICON = "🔬"

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
