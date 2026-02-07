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
        self.__InitializePlaybackControls()

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

    def __InitializePlaybackControls(self):
        controls = Frame(self.MainWindow, bg="black")
        controls.pack(side=BOTTOM, fill=X, pady=10)

        prevBtn = Button(
            controls,
            text="⏮",
            width=5,
            command=self.OnPrevious
        )
        prevBtn.pack(side=LEFT, padx=10)

        playPauseBtn = Button(
            controls,
            text="⏯",
            width=5,
            command=self.AudioController.TogglePlayPause
        )
        playPauseBtn.pack(side=LEFT, padx=10)

        nextBtn = Button(
            controls,
            text="⏭",
            width=5,
            command=self.OnNext
        )
        nextBtn.pack(side=LEFT, padx=10)

        volumeSlider = Scale(
            controls,
            from_=0.0,
            to=1.0,
            resolution=0.01,
            orient=HORIZONTAL,
            label="Volume",
            length=200,
            command=self.AudioController.SetVolume
        )
        volumeSlider.set(self.AudioController.Volume)
        volumeSlider.pack(side=RIGHT, padx=20)

    def OnPrevious(self):
        # TODO: hook into playlist
        self.AudioController.Stop()

    def OnNext(self):
        # TODO: hook into playlist
        self.AudioController.Stop()

    def Shutdown(self):
        self.AudioController.Stop()
        self.MainWindow.quit()