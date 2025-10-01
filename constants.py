"""
Language constants and mappings for the translator application
Contains language codes, names, and TTS (Text-to-Speech) locale mappings
"""

# List of supported languages with their display names and ISO codes
# Format: (Display Name, ISO Language Code)
LANGUAGES = [
    ("English (US)", "en"), ("English (UK)", "en"), ("Turkish", "tr"), ("French", "fr"),
    ("German", "de"), ("Spanish", "es"), ("Portuguese", "pt"), ("Italian", "it"),
    ("Japanese", "ja"), ("Korean", "ko"), ("Chinese (Simplified)", "zh-cn"),
    ("Chinese (Traditional)", "zh-tw"), ("Arabic", "ar"), ("Russian", "ru"),
    ("Dutch", "nl"), ("Polish", "pl"), ("Greek", "el"), ("Hebrew", "he"),
    ("Hindi", "hi"), ("Thai", "th"), ("Vietnamese", "vi"), ("Indonesian", "id"),
    ("Malay", "ms"), ("Filipino", "tl"), ("Swedish", "sv"), ("Norwegian", "no"),
    ("Danish", "da"), ("Finnish", "fi"), ("Czech", "cs"), ("Slovak", "sk"),
    ("Hungarian", "hu"), ("Romanian", "ro"), ("Bulgarian", "bg"), ("Croatian", "hr"),
    ("Serbian", "sr"), ("Ukrainian", "uk"), ("Lithuanian", "lt"), ("Latvian", "lv"),
    ("Estonian", "et"), ("Slovenian", "sl"), ("Catalan", "ca"), ("Basque", "eu"),
    ("Galician", "gl"), ("Welsh", "cy"), ("Irish", "ga"), ("Icelandic", "is"),
    ("Maltese", "mt"), ("Esperanto", "eo"), ("Latin", "la"), ("Persian", "fa"),
    ("Urdu", "ur"), ("Bengali", "bn"), ("Tamil", "ta"), ("Telugu", "te"),
    ("Gujarati", "gu"), ("Punjabi", "pa"), ("Marathi", "mr"), ("Kannada", "kn"),
    ("Malayalam", "ml"), ("Sinhalese", "si"), ("Nepali", "ne"), ("Burmese", "my"),
    ("Khmer", "km"), ("Lao", "lo"), ("Georgian", "ka"), ("Armenian", "hy"),
    ("Azerbaijani", "az"), ("Kazakh", "kk"), ("Kyrgyz", "ky"), ("Uzbek", "uz"),
    ("Tajik", "tg"), ("Mongolian", "mn"), ("Tibetan", "bo"), ("Swahili", "sw"),
    ("Amharic", "am"), ("Somali", "so"), ("Zulu", "zu"), ("Xhosa", "xh"),
    ("Afrikaans", "af"), ("Hausa", "ha"), ("Yoruba", "yo"), ("Igbo", "ig"),
]

# Dictionary mapping language names to their ISO codes
# Used for dropdown options: {"English (US)": "en", "Turkish": "tr", ...}
LANG_BY_NAME = {n: c for n, c in LANGUAGES}

# Dictionary mapping ISO codes to language names
# Reverse mapping for displaying language names: {"en": "English (US)", "tr": "Turkish", ...}
LANG_BY_CODE = {c: n for n, c in LANGUAGES}

# List of all language display names
# Used for filtering and searching: ["English (US)", "Turkish", "French", ...]
LANG_NAMES = [n for n, _ in LANGUAGES]

# Mapping of ISO language codes to BCP 47 locale codes for Text-to-Speech
# TTS engines require locale-specific codes (e.g., "en-US" instead of "en")
# Format: {iso_code: locale_code}
LANG_TTS_MAP = {
    "en": "en-US",      # English -> US English
    "tr": "tr-TR",      # Turkish -> Turkey Turkish
    "fr": "fr-FR",      # French -> France French
    "de": "de-DE",      # German -> Germany German
    "es": "es-ES",      # Spanish -> Spain Spanish
    "pt": "pt-BR",      # Portuguese -> Brazilian Portuguese
    "it": "it-IT",      # Italian -> Italy Italian
    "ja": "ja-JP",      # Japanese -> Japan Japanese
    "ko": "ko-KR",      # Korean -> South Korea Korean
    "zh-cn": "zh-CN",   # Chinese Simplified -> China Chinese
    "zh-tw": "zh-TW",   # Chinese Traditional -> Taiwan Chinese
    "ar": "ar-SA",      # Arabic -> Saudi Arabia Arabic
    "ru": "ru-RU",      # Russian -> Russia Russian
    "nl": "nl-NL",      # Dutch -> Netherlands Dutch
    "pl": "pl-PL",      # Polish -> Poland Polish
    "el": "el-GR",      # Greek -> Greece Greek
    "he": "he-IL",      # Hebrew -> Israel Hebrew
    "hi": "hi-IN",      # Hindi -> India Hindi
    "th": "th-TH",      # Thai -> Thailand Thai
    "vi": "vi-VN",      # Vietnamese -> Vietnam Vietnamese
    "id": "id-ID",      # Indonesian -> Indonesia Indonesian
    "ms": "ms-MY",      # Malay -> Malaysia Malay
    "tl": "tl-PH",      # Filipino -> Philippines Filipino
    "sv": "sv-SE",      # Swedish -> Sweden Swedish
    "no": "no-NO",      # Norwegian -> Norway Norwegian
    "da": "da-DK",      # Danish -> Denmark Danish
    "fi": "fi-FI",      # Finnish -> Finland Finnish
    "cs": "cs-CZ",      # Czech -> Czech Republic Czech
    "sk": "sk-SK",      # Slovak -> Slovakia Slovak
    "hu": "hu-HU",      # Hungarian -> Hungary Hungarian
    "ro": "ro-RO",      # Romanian -> Romania Romanian
    "bg": "bg-BG",      # Bulgarian -> Bulgaria Bulgarian
    "hr": "hr-HR",      # Croatian -> Croatia Croatian
    "sr": "sr-RS",      # Serbian -> Serbia Serbian
    "uk": "uk-UA",      # Ukrainian -> Ukraine Ukrainian
    "lt": "lt-LT",      # Lithuanian -> Lithuania Lithuanian
    "lv": "lv-LV",      # Latvian -> Latvia Latvian
    "et": "et-EE",      # Estonian -> Estonia Estonian
    "sl": "sl-SI",      # Slovenian -> Slovenia Slovenian
    "ca": "ca-ES",      # Catalan -> Spain Catalan
    "cy": "cy-GB",      # Welsh -> Great Britain Welsh
    "ga": "ga-IE",      # Irish -> Ireland Irish
    "is": "is-IS",      # Icelandic -> Iceland Icelandic
    "mt": "mt-MT",      # Maltese -> Malta Maltese
    "fa": "fa-IR",      # Persian -> Iran Persian
    "ur": "ur-PK",      # Urdu -> Pakistan Urdu
    "bn": "bn-IN",      # Bengali -> India Bengali
    "ta": "ta-IN",      # Tamil -> India Tamil
    "te": "te-IN",      # Telugu -> India Telugu
    "gu": "gu-IN",      # Gujarati -> India Gujarati
    "pa": "pa-IN",      # Punjabi -> India Punjabi
    "mr": "mr-IN",      # Marathi -> India Marathi
    "kn": "kn-IN",      # Kannada -> India Kannada
    "ml": "ml-IN",      # Malayalam -> India Malayalam
    "si": "si-LK",      # Sinhalese -> Sri Lanka Sinhalese
    "ne": "ne-NP",      # Nepali -> Nepal Nepali
    "my": "my-MM",      # Burmese -> Myanmar Burmese
    "km": "km-KH",      # Khmer -> Cambodia Khmer
    "lo": "lo-LA",      # Lao -> Laos Lao
    "ka": "ka-GE",      # Georgian -> Georgia Georgian
    "hy": "hy-AM",      # Armenian -> Armenia Armenian
    "az": "az-AZ",      # Azerbaijani -> Azerbaijan Azerbaijani
    "kk": "kk-KZ",      # Kazakh -> Kazakhstan Kazakh
    "ky": "ky-KG",      # Kyrgyz -> Kyrgyzstan Kyrgyz
    "uz": "uz-UZ",      # Uzbek -> Uzbekistan Uzbek
    "tg": "tg-TJ",      # Tajik -> Tajikistan Tajik
    "mn": "mn-MN",      # Mongolian -> Mongolia Mongolian
    "sw": "sw-KE",      # Swahili -> Kenya Swahili
    "am": "am-ET",      # Amharic -> Ethiopia Amharic
    "so": "so-SO",      # Somali -> Somalia Somali
    "zu": "zu-ZA",      # Zulu -> South Africa Zulu
    "xh": "xh-ZA",      # Xhosa -> South Africa Xhosa
    "af": "af-ZA",      # Afrikaans -> South Africa Afrikaans
    "ha": "ha-NG",      # Hausa -> Nigeria Hausa
    "yo": "yo-NG",      # Yoruba -> Nigeria Yoruba
    "ig": "ig-NG"       # Igbo -> Nigeria Igbo
}