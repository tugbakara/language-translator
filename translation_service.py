from functools import lru_cache
from constants import LANG_TTS_MAP
import asyncio
import json
import os

# Load configuration
def load_config():
    """Load application configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

CONFIG = load_config()

# Check if translation library is available
TRANSLATOR_AVAILABLE = True
try:
    from googletrans import Translator
except ImportError:
    TRANSLATOR_AVAILABLE = False

@lru_cache(maxsize=CONFIG['cache']['translator_size'])
def get_translator():
    """
    Create and cache translator instance
    Returns:
        Translator object or None if library not available
    """
    if not TRANSLATOR_AVAILABLE:
        return None
    print("[DEBUG] Translator object created and cached.")
    return Translator()

def get_tts_language(lang_code):
    """
    Map language code to TTS (Text-to-Speech) compatible code
    Args:
        lang_code: Language code (e.g., 'en', 'tr')
    Returns:
        TTS-compatible language code (e.g., 'en-US', 'tr-TR')
    """
    return LANG_TTS_MAP.get(lang_code, lang_code)

def translate_text(txt, src, tgt):
    """
    Translate text from source language to target language
    Args:
        txt: Text to translate
        src: Source language code (use 'auto' for auto-detection)
        tgt: Target language code
    Returns:
        Tuple of (translated_text, detected_source_language)
    """
    translator = get_translator()
    
    # Check if translator is available
    if not translator:
        return "Error: Translation library (googletrans) is not installed on the server.", src

    # Return empty string for empty input
    if not txt.strip():
        return "", "en"

    try:
        # Perform translation
        res = translator.translate(txt, src=src, dest=tgt)

        detected_src = res.src
        translated_text = res.text

        # Check if translation actually occurred (service sometimes returns original text)
        if detected_src and detected_src.lower() != tgt.lower() and translated_text.strip() == txt.strip():
            error_message = (
                "Translation failed. The service returned the original text. "
                "This may be due to a temporary network issue or an unsupported language."
            )
            return error_message, detected_src

        return translated_text, detected_src

    except Exception as e:
        # Handle translation errors
        print(f"[ERROR] An error occurred during translation: {e}")
        error_message = (
            "Translation error: Could not connect to the service. "
            "Please check your internet connection or try again later."
        )
        detected_source_on_error = src if src != "auto" else "en"
        return error_message, detected_source_on_error

async def translate_text_async(txt, src, tgt):
    """
    Asynchronous wrapper for translate_text function
    Args:
        txt: Text to translate
        src: Source language code
        tgt: Target language code
    Returns:
        Result from translate_text function
    """
    return await asyncio.to_thread(translate_text, txt, src, tgt)