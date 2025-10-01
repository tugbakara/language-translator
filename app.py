import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import json
import os
import base64
from functools import lru_cache

from constants import LANG_BY_NAME, LANG_TTS_MAP
from translation_service import translate_text, TRANSLATOR_AVAILABLE

# Load configuration from config.json
def load_config():
    """Load application configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

CONFIG = load_config()

@lru_cache(maxsize=CONFIG['cache']['file_encoding_size'])
def encode_file(path):
    """
    Encode file to base64 string with caching
    Args:
        path: File path to encode
    Returns:
        Base64 encoded string or empty string if file not found
    """
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

@lru_cache(maxsize=CONFIG['cache']['background_images_size'])
def get_bg_images_base64():
    """
    Load and encode background images from configured folder
    Returns:
        List of base64 encoded background images (limited by max_background_images)
    """
    folder = CONFIG['paths']['backgrounds']
    if not os.path.exists(folder):
        return []
    
    bg_files = []
    supported_formats = (".jpg", ".png", ".jpeg", ".webp", ".avif", ".gif")
    
    for f in os.listdir(folder):
        if f.lower().endswith(supported_formats):
            file_path = os.path.join(folder, f)
            encoded = encode_file(file_path)
            if encoded:  
                bg_files.append(encoded)
                print(f"[DEBUG] Encoded background image: {f}")
    
    max_images = CONFIG['app']['max_background_images']
    print(f"[DEBUG] Total encoded background images: {len(bg_files)}")
    return bg_files[:max_images]

def generate_background_css():
    """
    Generate CSS for background animation
    Returns:
        CSS string with either image slideshow or gradient animation
    """
    bg_images = get_bg_images_base64()
    
    # Fallback to gradient animation if no images found
    if not bg_images:
        return """
        body {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe);
            background-size: 400% 400%;
            animation: gradientMove 15s ease infinite;
        }
        
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        """
    
    # Generate keyframes for background image slideshow
    frames = "@keyframes bgFade {"
    step = 100 // len(bg_images)
    
    for i, b64_img in enumerate(bg_images):
        percentage = i * step
        frames += f"""
            {percentage}% {{
                background-image: url('data:image/jpeg;base64,{b64_img}');
            }}
        """
    
    # Complete the loop by returning to first image
    frames += f"""
        100% {{
            background-image: url('data:image/jpeg;base64,{bg_images[0]}');
        }}
    }}"""
    
    animation_duration = len(bg_images) * CONFIG['app']['background_animation_duration']
    css = f"""
    {frames}
    
    body {{
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        animation: bgFade {animation_duration}s infinite ease-in-out !important;
    }}
    """
    
    return css

def get_language_options():
    """
    Generate dropdown options for language selection
    Returns:
        List of dicts with label and value for each language
    """
    return [{"label": name, "value": code} for name, code in LANG_BY_NAME.items()]

def get_tts_language(lang_code):
    """
    Map language code to TTS (Text-to-Speech) compatible code
    Args:
        lang_code: Language code (e.g., 'en', 'tr')
    Returns:
        TTS-compatible language code (e.g., 'en-US', 'tr-TR')
    """
    return LANG_TTS_MAP.get(lang_code, lang_code)

def create_icon_buttons_html(text, lang_code, button_prefix="btn", disabled=False):
    """
    Generate HTML for listen and copy buttons with embedded JavaScript
    Args:
        text: Text content to be spoken or copied
        lang_code: Language code for TTS
        button_prefix: Unique prefix for button IDs
        disabled: Whether buttons should be disabled
    Returns:
        HTML string with buttons and functionality
    """
    # Load icon paths from config
    mic_b64 = encode_file(CONFIG['assets']['mic_icon'])
    copy_b64 = encode_file(CONFIG['assets']['copy_icon'])
    
    # Fallback to direct asset paths if encoding fails
    mic_src = f"data:image/png;base64,{mic_b64}" if mic_b64 else f"/{CONFIG['assets']['mic_icon']}"
    copy_src = f"data:image/png;base64,{copy_b64}" if copy_b64 else f"/{CONFIG['assets']['copy_icon']}"

    # Escape text for safe JSON embedding
    safe_text = json.dumps(text if text else "")
    
    # Generate unique ID for this button instance
    unique_id = f"{button_prefix}_{abs(hash(f'{text}{lang_code}{disabled}')) % 10000}"

    # Style definitions based on disabled state
    button_style = (
        "background: rgba(255, 255, 224, 0.9); border: 1px solid rgba(230, 230, 184, 0.8);" 
        if not disabled else 
        "background: rgba(200, 200, 200, 0.5); border: 1px solid rgba(180, 180, 180, 0.6);"
    )
    hover_style = (
        ".icon-button:not(:disabled):hover { background: rgba(255, 250, 205, 0.95); }" 
        if not disabled else ""
    )
    disabled_attr = "disabled" if disabled else ""
    
    button_size = CONFIG['ui']['icon_button_size']
    icon_size = CONFIG['ui']['icon_size']

    # Generate complete HTML with embedded styles and scripts
    html_content = f"""
    <!DOCTYPE html><html><head><meta charset="utf-8" /></head><body style="margin:0; padding:0; overflow:hidden; height: 100%;">
    <style>
        body {{ overflow: hidden !important; height: 100%; }}
        .icon-container {{ 
            position: absolute;
            right: 10px;
            bottom: 5px;
            display: flex; 
            gap: 8px; 
            z-index: 1000;
        }}
        .icon-button {{ 
            {button_style} 
            border-radius: 50%; 
            width: {button_size}px; 
            height: {button_size}px; 
            cursor: {'pointer' if not disabled else 'not-allowed'}; 
            display: inline-flex; 
            align-items: center; 
            justify-content: center; 
            transition: background 0.2s ease; 
            padding: 0; 
            flex-shrink: 0;
        }}
        {hover_style}
        .icon-button img {{ 
            width: {icon_size}px; 
            height: {icon_size}px; 
            opacity: {'1' if not disabled else '0.4'}; 
        }}
    </style>
    <div class="icon-container">
        <button class="icon-button" title="Listen" onclick="parent.speakText_{unique_id}()" {disabled_attr}><img src="{mic_src}" alt="Listen"></button>
        <button id="copy_{unique_id}" class="icon-button" title="Copy" onclick="parent.copyText_{unique_id}()" {disabled_attr}><img src="{copy_src}" alt="Copy"></button>
    </div>
    <script>
        parent.speakText_{unique_id} = function() {{
            if (!'speechSynthesis' in window) return;

            // Stop current speech if already speaking
            if (window.speechSynthesis.speaking) {{
                window.speechSynthesis.cancel();
                return;
            }}

            const text = {safe_text};
            if (!text || !text.trim()) return;

            window.speechSynthesis.cancel(); 
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = '{lang_code}';
            window.speechSynthesis.speak(utterance);
        }}
        parent.copyText_{unique_id} = function() {{
            const text = {safe_text};
            if (!text || !text.trim()) return;
            navigator.clipboard.writeText(text).then(() => {{
                console.log('Text copied to clipboard');
            }}).catch(err => {{
                console.error('Copy failed:', err);
            }});
        }}
    </script></body></html>
    """
    return html_content

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SANDSTONE],
                suppress_callback_exceptions=True)
server = app.server

from flask import send_from_directory

@server.route('/fonts/<path:filename>')
def serve_fonts(filename):
    """
    Flask route to serve font files with proper caching
    Args:
        filename: Font filename to serve
    Returns:
        File response with cache headers or 404 error
    """
    try:
        fonts_path = CONFIG['paths']['fonts']
        response = send_from_directory(fonts_path, filename)
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response
    except Exception as e:
        return f"Font not found: {filename}", 404

# Generate background CSS once at startup
BACKGROUND_CSS = generate_background_css()

# Custom HTML template with embedded styles and fonts
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{CONFIG['app']['title']}</title>
        {{%favicon%}}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        {{%css%}}
        <style>
            @font-face {{
                font-family: 'Century Gothic';
                src: url('/{CONFIG['fonts']['century_gothic']['regular']}') format('truetype');
                font-weight: normal;
                font-style: normal;
            }}

            @font-face {{
                font-family: 'Century Gothic';
                src: url('/{CONFIG['fonts']['century_gothic']['bold']}') format('truetype');
                font-weight: bold;
                font-style: normal;
            }}
            {BACKGROUND_CSS}
            
            html, body {{
                height: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow-x: hidden !important;
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            #react-entry-point {{
                background: transparent !important;
                min-height: 100vh !important;
                position: relative !important;
                z-index: 2 !important;
            }}
            
            ._dash-loading {{
                background: transparent !important;
            }}
            
            h1 {{
                font-family: 'Playfair Display', serif !important;
                color: #2c3e50 !important;
                font-weight: 700 !important;
                text-align: center !important;
                margin-bottom: 30px !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
            }}
            
            h5, p, span, div, label, input, select, option {{
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            .container {{
                background: transparent !important;
                border-radius: 15px !important;
                padding: 30px !important;
                margin: 20px auto !important;
                max-width: 900px !important;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
                backdrop-filter: blur(10px) !important;
            }}
            
            .custom-textarea {{
                background: rgba(255, 255, 255, 0.5) !important;
                border: 2px solid #e3f2fd !important;
                border-radius: 12px !important;
                padding: 15px !important;
                font-size: 16px !important;
                line-height: 1.5 !important;
                transition: all 0.3s ease !important;
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            .custom-textarea:focus {{
                border-color: #4fc3f7 !important;
                box-shadow: 0 0 0 3px rgba(79, 195, 247, 0.1) !important;
                outline: none !important;
            }}

            .action-button {{
                padding: 12px 30px !important;
                border-radius: 25px !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                border: none !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                min-width: 120px !important;
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
                text-transform: capitalize !important;
                background: #dcdcdc !important;  
                color: #2c2c2c !important;        
            }}

            .action-button:hover {{
                background: #b39ddb !important;   
                color: white !important;          
                transform: translateY(-2px) !important;
            }}

            .translate-btn {{
                background: linear-gradient(135deg, #4fc3f7, #29b6f6) !important;
                color: white !important;
            }}
            
            .translate-btn:hover {{
                background: linear-gradient(135deg, #29b6f6, #0288d1) !important;
                transform: translateY(-2px) !important;
            }}
            
            .clear-btn {{
                background: linear-gradient(135deg, #ff7043, #ff5722) !important;
                color: white !important;
                margin-left: 15px !important;
            }}
            
            .clear-btn:hover {{
                background: linear-gradient(135deg, #ff5722, #e64a19) !important;
                transform: translateY(-2px) !important;
            }}
            
            .char-counter {{
                font-size: 14px !important;
                color: #666 !important;
                text-align: right !important;
                margin-top: 5px !important;
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            .icon-button-iframe {{
                position: absolute !important;
                right: 0 !important;
                bottom: 0 !important;
                width: 90px !important;
                height: 45px !important;
                border: none !important;
                pointer-events: auto !important;
                z-index: 100 !important;
            }}
            
            .Select-control {{
                border-radius: 8px !important;
                border: 2px solid #e3f2fd !important;
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            .dash-dropdown .Select-value-label,
            .dash-dropdown .Select-placeholder,
            .dash-dropdown .Select-menu-outer,
            .dash-dropdown .Select-option {{
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            .form-check-label {{
                font-family: 'Century Gothic', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    margin: 10px !important;
                    padding: 20px !important;
                    border-radius: 10px !important;
                }}
                
                .action-button {{
                    padding: 10px 20px !important;
                    font-size: 14px !important;
                    min-width: 100px !important;
                }}
                
                .clear-btn {{
                    margin-left: 0 !important;
                    margin-top: 10px !important;
                }}
            }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# Application layout
app.layout = html.Div([
    dbc.Container([
        html.H1(CONFIG['app']['title'], className="my-4"),

        html.H5("Language Selection"),
        
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span("Source Language", style={
                            "fontWeight": "bold", 
                            "fontSize": "14px", 
                            "color": "#2c3e50",
                            "marginRight": "20px"
                        }),
                        dbc.Checkbox(
                            label="Auto Detect", 
                            value=True, 
                            id="auto-detect-checkbox",
                            style={
                                "display": "inline-block",
                                "fontSize": "14px"
                            }
                        )
                    ], style={
                        "display": "flex", 
                        "alignItems": "center", 
                        "marginBottom": "8px"
                    }),
                    dcc.Dropdown(
                        id="source-lang-dropdown",
                        options=get_language_options(),
                        value=CONFIG['ui']['default_source_lang'],
                        disabled=True
                    )
                ], width=6),
                
                dbc.Col([
                    html.Div("Target Language", style={
                        "fontWeight": "bold", 
                        "fontSize": "14px", 
                        "color": "#2c3e50",
                        "marginBottom": "8px"
                    }),
                    dcc.Dropdown(
                        id="target-lang-dropdown",
                        options=get_language_options(),
                        value=CONFIG['ui']['default_target_lang'],
                        clearable=False
                    )
                ], width=6)
            ], style={"alignItems": "end"})
        ], className="mb-4"),

        html.H5("Input Text"),
        html.Div([
            dbc.Textarea(
                id="input-textarea", 
                placeholder="Enter text to translate...", 
                className="custom-textarea", 
                rows=CONFIG['ui']['textarea_rows']
            ),
            html.Iframe(
                id='input-buttons-iframe', 
                srcDoc=create_icon_buttons_html("", "en-US", disabled=True), 
                className="icon-button-iframe"
            )
        ], style={"position": "relative", "marginBottom": "10px"}),
        
        html.Div(f"0/{CONFIG['app']['max_char_limit']} characters", id="input-char-count", className="char-counter"),

        html.H5("Translation"),
        dcc.Loading(
            id="loading-output",
            type="default",
            children=[
                html.Div([
                    dbc.Textarea(
                        id="output-textarea", 
                        readOnly=True, 
                        placeholder="Translation will appear here...", 
                        className="custom-textarea", 
                        rows=CONFIG['ui']['textarea_rows']
                    ),
                    html.Iframe(
                        id='output-buttons-iframe', 
                        srcDoc=create_icon_buttons_html("", "tr-TR", disabled=True), 
                        className="icon-button-iframe"
                    )
                ], style={"position": "relative", "marginBottom": "10px"}),
                
                html.Div("0 characters", id="output-char-count", className="char-counter"),
            ]
        ),
        html.Div([
            dbc.Button(
                "Translate", 
                id="translate-button", 
                n_clicks=0, 
                className="action-button"
            ),
            dbc.Button(
                "Clear all", 
                id="clear-button", 
                n_clicks=0, 
                className="action-button",
                style={"marginLeft": "15px"}
            )
        ], className="button-container", style={"textAlign": "center", "margin": "30px 0"})

    ], fluid=False, className="container")
])

@app.callback(
    Output("source-lang-dropdown", "disabled"),
    Input("auto-detect-checkbox", "value")
)
def toggle_source_dropdown(is_auto):
    """
    Enable or disable source language dropdown based on auto-detect checkbox
    Args:
        is_auto: Boolean state of auto-detect checkbox
    Returns:
        Boolean to set disabled state of dropdown
    """
    return is_auto

@app.callback(
    Output("output-textarea", "value"),
    Input("translate-button", "n_clicks"),
    State("input-textarea", "value"),
    State("auto-detect-checkbox", "value"),
    State("source-lang-dropdown", "value"),
    State("target-lang-dropdown", "value"),
    prevent_initial_call=True
)
def perform_translation(n_clicks, text, is_auto, src_lang, tgt_lang):
    """
    Perform translation when translate button is clicked
    Args:
        n_clicks: Number of times button was clicked
        text: Input text to translate
        is_auto: Whether auto-detect is enabled
        src_lang: Source language code
        tgt_lang: Target language code
    Returns:
        Translated text string
    """
    if not text or not text.strip():
        return ""
    source = "auto" if is_auto else src_lang
    translated_text, _ = translate_text(text, source, tgt_lang)
    return translated_text

@app.callback(
    Output("input-textarea", "value"),
    Output("output-textarea", "value", allow_duplicate=True),
    Input("clear-button", "n_clicks"),
    prevent_initial_call=True
)
def clear_text(n_clicks):
    """
    Clear both input and output textareas when clear button is clicked
    Args:
        n_clicks: Number of times button was clicked
    Returns:
        Tuple of empty strings for both textareas
    """
    return "", ""

@app.callback(
    Output("input-char-count", "children"),
    Input("input-textarea", "value")
)
def update_input_char_count(text):
    """
    Update character count display for input textarea
    Args:
        text: Current input text
    Returns:
        Formatted string showing character count
    """
    max_chars = CONFIG['app']['max_char_limit']
    return f"{len(text or '')}/{max_chars} characters"

@app.callback(
    Output("output-char-count", "children"),
    Input("output-textarea", "value")
)
def update_output_char_count(text):
    """
    Update character count display for output textarea
    Args:
        text: Current output text
    Returns:
        Formatted string showing character count
    """
    return f"{len(text or '')} characters"

@app.callback(
    Output('input-buttons-iframe', 'srcDoc'),
    Input('input-textarea', 'value'),
    State('source-lang-dropdown', 'value'),
    State('auto-detect-checkbox', 'value'),
)
def update_input_buttons(text, src_lang, is_auto):
    """
    Update input textarea icon buttons based on content and language
    Args:
        text: Current input text
        src_lang: Selected source language
        is_auto: Whether auto-detect is enabled
    Returns:
        HTML string for button iframe
    """
    disabled = not text or not text.strip()
    if is_auto:
        lang_code = "auto"
    else:
        lang_code = get_tts_language(src_lang)
    return create_icon_buttons_html(text, lang_code, "input", disabled)

@app.callback(
    Output('output-buttons-iframe', 'srcDoc'),
    Input('output-textarea', 'value'),
    State('target-lang-dropdown', 'value'),
)
def update_output_buttons(text, tgt_lang):
    """
    Update output textarea icon buttons based on content and language
    Args:
        text: Current output text
        tgt_lang: Selected target language
    Returns:
        HTML string for button iframe
    """
    disabled = not text or not text.strip() or text.startswith("Translation error")
    lang_code = get_tts_language(tgt_lang)
    return create_icon_buttons_html(text, lang_code, "output", disabled)

if __name__ == "__main__":
    print("[DEBUG] Starting application...")
    if not TRANSLATOR_AVAILABLE:
        print("ERROR: googletrans library is not installed. Please run 'pip install googletrans==4.0.0rc1'")
    else:
        app.run(
            debug=CONFIG['app']['debug'], 
            host=CONFIG['app']['host'], 
            port=CONFIG['app']['port']
        )