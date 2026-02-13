# SoundSight

SoundSight is a desktop audio visualization application built with Python and Tkinter.  
It allows users to load audio files, play them back, seek through playback, and visualize audio data in real time.

This project is being developed incrementally using Agile-style sprints and UML-based design.

---

## Features (Current)

- Load audio files through a file dialog
- Audio playback using a streaming audio output
- Adjustable volume
- Seek bar for navigating playback
- Basic application window and menu system
- Unit tests for core audio controller logic

---

## Requirements

- Python 3.11 (recommended)
- FFmpeg (required by pydub)

### Python Packages

Install required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

From the project root directory, run:

```bash
python Main.py
```