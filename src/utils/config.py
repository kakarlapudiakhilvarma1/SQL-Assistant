"""
Configuration settings for the Healthcare Database Request Assistant.
Contains paths, model settings, and other configuration parameters.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, "data")
FAISS_DIR = os.path.join(BASE_DIR, "faiss")

# Ensure directories exist
os.makedirs(FAISS_DIR, exist_ok=True)

# File paths
FAISS_INDEX_PATH = os.path.join(FAISS_DIR, "healthcare_index")

# Model settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gemini-2.0-flash"

# Text processing settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# UI settings
PAGE_TITLE = "Healthcare DB Assistant"
PAGE_ICON = "🏥"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"
