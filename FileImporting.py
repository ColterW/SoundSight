from tkinter import filedialog
from AudioController import AudioController

def SelectFile(audioController: AudioController):
    file = filedialog.askopenfile(
        mode="rb",
        filetypes=[
            ("Audio Files", "*.wav *.mp3 *.flac *.ogg *.aac"),
            ("All Files", "*.*")
        ]
    )
    
    if not file:
        return None
    
    audioController.LoadFile(file.name)
    audioController.Play()

def LoadDirectory():
    dirPath = filedialog.askdirectory()