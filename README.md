# OSS 117 Soundboard

An interactive soundboard featuring iconic quotes from the French film "OSS 117: Le Caire, nid d'espions". Browse, search, play, and create custom loops from 782 memorable sound clips.

## Features

- **Interactive Waveforms**: Visual representation of each sound using WaveSurfer.js
- **Loop Creation**: Click and drag on waveforms to create custom loops
- **Search**: Filter through hundreds of quotes instantly
- **Save Loops**: Save your favorite loops to a dedicated final soundboard
- **Playback Controls**: Play, stop, random play, and more
- **Responsive Design**: Works on desktop and mobile devices

## Screenshots

The soundboard displays all quotes with:
- Visual waveforms for each sound
- Search and filtering capabilities
- Loop creation by dragging on waveforms
- Ability to save custom loops

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd osssoundboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests beautifulsoup4
   ```

4. **Download the sound files**
   ```bash
   python download_sounds.py
   ```

   This will:
   - Download 782 sound clips (approximately 96 pages)
   - Create a `sounds/` directory
   - Save all MP3 files and metadata
   - Take approximately 10-15 minutes (includes polite delays between requests)

### Running the Soundboard

Once the sounds are downloaded, simply open the HTML files in your browser:

**Main Soundboard** (browse all sounds):
```bash
# On Linux/Mac:
open soundboard.html

# On Windows:
start soundboard.html

# Or double-click soundboard.html in your file manager
```

**Final Soundboard** (view saved loops):
```bash
# On Linux/Mac:
open final-soundboard.html

# On Windows:
start final-soundboard.html
```

Or use a local web server (recommended for better performance):
```bash
python -m http.server 8000
# Then open http://localhost:8000/soundboard.html in your browser
```

## Usage Guide

### Main Soundboard (soundboard.html)

- **Click** on a waveform to play from that position
- **Drag** on a waveform to create a loop region
- **Drag the edges** of a region to adjust the loop boundaries
- **Double-click** on a region to remove it
- Use the **search bar** to filter quotes
- Click **Save** button to save a loop to the Final Soundboard

### Keyboard Shortcuts

- `ESC` - Stop all playing sounds
- `SPACE` - Play a random sound

### Control Buttons

- **Stop All** - Stop all currently playing sounds
- **Clear All Loops** - Remove all loop regions
- **Random** - Play a random sound from the filtered results
- **Sort by Duration** - Sort sounds by length
- **Sort by Order** - Return to original order

### Final Soundboard (final-soundboard.html)

- View all your saved loops
- Export loops as individual MP3 files
- Delete loops you no longer want
- All loops are saved in browser localStorage

## Project Structure

```
osssoundboard/
├── download_sounds.py      # Script to download all sounds from source
├── soundboard.html         # Main interactive soundboard
├── final-soundboard.html   # Saved loops soundboard
├── README.md              # This file
├── .gitignore             # Git ignore file
└── sounds/                # Created by download script
    ├── metadata.json      # Sound metadata (title, duration, size, etc.)
    └── *.mp3             # 782 sound files
```

## Technical Details

### Dependencies

**Python (for downloading sounds):**
- `requests` - HTTP library for downloading
- `beautifulsoup4` - HTML parsing
- `ffprobe` (optional) - Audio duration detection

**JavaScript (included via CDN):**
- WaveSurfer.js v7 - Audio waveform visualization
- Regions plugin - Loop region creation

### Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Internet Explorer: Not supported

### Storage

- Sound files: ~75 MB total
- Saved loops stored in browser localStorage (no file size limit impact)

## Known Issues

- The metadata.json contains 3 duplicate entries (785 entries for 782 unique files)
- This doesn't affect functionality, just shows the same sound twice

## Credits

- Sound clips sourced from zonesons.com
- Film: "OSS 117: Le Caire, nid d'espions" (2006)
- Director: Michel Hazanavicius
- Starring: Jean Dujardin

## License

This project is for educational and entertainment purposes only. All sound clips belong to their respective copyright holders.

## Troubleshooting

**Sounds not loading:**
- Make sure you've run `download_sounds.py` first
- Check that the `sounds/` directory contains MP3 files
- Try using a local web server instead of opening the HTML directly

**Download script fails:**
- Check your internet connection
- The source website may be temporarily unavailable
- Try running the script again (it will skip already downloaded files)

**Waveforms not displaying:**
- Make sure you have a modern browser
- Check browser console for JavaScript errors
- Try clearing browser cache
