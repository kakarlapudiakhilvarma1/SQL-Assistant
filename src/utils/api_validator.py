"""
API key validation utilities for the Healthcare Database Request Assistant.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.config import LLM_MODEL


def validate_api_key(api_key):
    """
    Validate the API key by testing the LLM initialization.
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        tuple: (is_valid, error_message) - is_valid is a boolean indicating if the key is valid,
               error_message is None if valid, otherwise contains the error message
    """
    if not api_key:
        return False, "API key is empty"
    
    try:
        # Try to initialize the LLM with the provided API key
        # We don't need to generate any text, just test if initialization works
        ChatGoogleGenerativeAI(model=LLM_MODEL, api_key=api_key)
        return True, None
    except Exception as e:
        return False, str(e)
