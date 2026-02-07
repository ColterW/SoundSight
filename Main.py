from AudioController import AudioController
from Window import Window

# Persistent/Singleton AudioController
audioController = AudioController()

window = Window(audioController)
window.MainWindow.mainloop()