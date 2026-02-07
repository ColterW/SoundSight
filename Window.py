from tkinter import *
from AudioController import AudioController
import FileImporting

class Window:
    def __init__(self, audioController: AudioController):
        # Setup application window
        self.MainWindow = Tk()
        self.MainWindow.title('SoundSight')

        self.MainWindow.geometry("1280x720")
        self.MainWindow.config(background = "black")

        # Require audio controller as it is necessary for the application
        self.AudioController = audioController

        self.__InitializeMenuBar()

    def __InitializeMenuBar(self):
        # Create menu bar
        menubar = Menu(self.MainWindow)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu = filemenu)

        filemenu.add_command(
            label="Open File", 
            command = lambda: FileImporting.SelectFile(self.AudioController)
        )

        filemenu.add_command(
            label="Open Directory", 
            command = lambda: None
        )

        filemenu.add_command(
            label = "Close File", 
            command = lambda: None
        )

        filemenu.add_separator()

        filemenu.add_command(
            label = "Exit", 
            command = self.Shutdown
        )

        self.MainWindow.config(menu = menubar)

    def Shutdown(self):
        self.AudioController.Stop()
        self.MainWindow.quit()