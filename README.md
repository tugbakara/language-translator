# Language Translator

A web-based language translation application built with Python Dash framework. The application provides text translation between 80+ languages using Google Translate API, with text-to-speech and clipboard copy functionality.

## 📋 Prerequisites

- Python 3.7 or higher
- Internet connection (required for translation service)

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/tugbakara/language-translator.git
cd language-translator
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Project Structure**
```
language-translator/
│
├── app.py                    # Main application file
├── translation_service.py    # Translation logic
├── constants.py              # Language mappings
├── config.json              # Configuration settings
├── requirements.txt         # Python dependencies
├── README.md               # Documentation
│
├── assets/                 # Static assets
│   ├── mic.png            # Microphone icon
│   └── copy.png           # Copy icon
│
├── fonts/                 # Custom fonts
│   └── CenturyGothic/
│       ├── centurygothic.ttf
│       └── centurygothic_bold.ttf
│
└── bg/                    # Background images (optional)
    ├── image1.jpg
    ├── image2.png
    └── ...
```

## 🏃 Running the Application

1. **Start the server**
```bash
python app.py
```

2. **Access the application**
Open your web browser and navigate to:
```
http://127.0.0.1:8050
```

3. **Using the translator**
   - Select source and target languages (or enable auto-detect)
   - Enter text in the input area (max 5000 characters)
   - Click "Translate" button
   - Use microphone icon for text-to-speech
   - Use copy icon to copy text to clipboard
   - Click "Clear all" to reset both fields

## 📦 Dependencies

- `dash>=2.0.0` - Web application framework
- `dash-bootstrap-components>=1.0.0` - Bootstrap components for Dash
- `googletrans==4.0.0rc1` - Translation service (Google Translate API)
- `flask>=2.0.0` - Web server (included with Dash)

## 🎨 Customization

### Background Images

The application supports animated background slideshows:

1. Create a `bg` folder in the project root
2. Add images in supported formats: jpg, png, jpeg, webp, avif, gif
3. The application automatically cycles through up to 8 images
4. Animation duration: 4 seconds per image (configurable in `config.json`)

If no background images are found, a gradient animation displays as fallback.

### Custom Fonts

To use custom fonts:

1. Place font files in the `fonts` directory structure
2. Update font paths in `config.json`:
```json
"fonts": {
  "century_gothic": {
    "regular": "fonts/CenturyGothic/centurygothic.ttf",
    "bold": "fonts/CenturyGothic/centurygothic_bold.ttf"
  }
}
```

The application uses Century Gothic as the primary font and Playfair Display for headings.

### UI Icons

Replace default icons in the `assets` folder:
- `mic.png` - Microphone/listen button icon
- `copy.png` - Copy to clipboard button icon

Recommended format: PNG with transparent background, 18x18 pixels.

## 🛠️ Technical Details

### Architecture

The application consists of four main components:

1. **app.py**: Main application logic with Dash layout and callbacks. Handles UI rendering, user interactions, and coordinates between components.

2. **translation_service.py**: Translation service wrapper that interfaces with googletrans library. Includes error handling and caching for translator instances.

3. **constants.py**: Language code mappings and TTS locale definitions. Contains 80+ language definitions with ISO codes and BCP 47 locale mappings for text-to-speech.

4. **config.json**: Centralized configuration for paths, application settings, UI parameters, and cache sizes.


## 🐛 Troubleshooting

### Translation Service Unavailable
**Error**: "Translation library (googletrans) is not installed"  
**Solution**: Run `pip install googletrans==4.0.0rc1`

### Font Not Loading
**Solution**: 
- Verify font files exist in the `fonts` directory
- Check paths in `config.json` match directory structure
- Clear browser cache

### Background Images Not Showing
**Solution**:
- Ensure images are in correct folder (default: `bg`)
- Verify supported format: jpg, png, jpeg, webp, avif, gif
- Check file permissions


## 🤝 Contributing

Contributions are welcome. Please submit pull requests with clear descriptions of changes.

## ⚠️ Important Notes

- Uses unofficial Google Translate API via `googletrans` library
