"""
Configuration module for the Health Chatbot application.

This module loads environment variables and provides centralized configuration
settings for the Flask application, Gemini API, and chatbot behavior.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Centralized configuration class for the application.
    
    All configuration settings are loaded from environment variables with
    sensible defaults for development and production environments.
    """
    
    # ==================== Flask Configuration ====================
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # ==================== Gemini API Configuration ====================
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # ==================== Model Configuration ====================
    MODEL_NAME = "gemini-flash-latest"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # ==================== Chat Configuration ====================
    MAX_HISTORY_LENGTH = 10

