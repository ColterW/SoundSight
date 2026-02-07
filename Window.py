from tkinter import *
from AudioController import AudioController
import FileImporting

class Window:
    # 3 Second inactivity timeout (no mouse movement)
    INACTIVITY_TIMEOUT_MS = 3000

    MainWindow: Frame
    ControlFrame: Frame
    AudioController

    _hideControlsAfterId: str

    def __init__(self, audioController: AudioController):
        # Setup application window
        self.MainWindow = Tk()
        self.MainWindow.title('SoundSight')

        self.MainWindow.geometry("1280x720")
        self.MainWindow.config(background = "black")

        # Require audio controller as it is necessary for the application
        self.AudioController = audioController

        self._InitializeMenuBar()
        self._InitializePlaybackControls()

        # Track mouse activity
        self.MainWindow.bind("<Motion>", self._OnMouseMove)
        self._hideControlsAfterId = None

    def _OnMouseMove(self, event = None):
        # Cancel any existing scheduled hide
        if self._hideControlsAfterId:
            self.MainWindow.after_cancel(self._hideControlsAfterId)

        # Show controls if hidden
        if not self.ControlFrame.winfo_ismapped():
            self._AnimateShowStep()
            # controlsHeight = self.ControlFrame.winfo_reqheight()
            # self.ControlFrame.place(x=0, y=self.MainWindow.winfo_height() - controlsHeight)
        
        # Schedule controls to hide after timeout
        self._hideControlsAfterId = self.MainWindow.after(
            self.INACTIVITY_TIMEOUT_MS,
            self._HideControls
        )

    def _InitializeMenuBar(self):
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
            command = self.AudioController.Stop
        )

        filemenu.add_separator()

        filemenu.add_command(
            label = "Exit", 
            command = self.Shutdown
        )

        self.MainWindow.config(menu = menubar)

    def _InitializePlaybackControls(self):
        self.ControlFrame = Frame(self.MainWindow, bg="black")
        # self.ControlFrame.pack(side=BOTTOM, fill=X, pady=10)

        # Secondary frame just for buttons
        # This is done to center the controls on the window
        buttonFrame = Frame(self.ControlFrame, bg="black")
        buttonFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        prevBtn = Button(
            buttonFrame,
            text="⏮",
            width=5,
            command=self.OnPrevious
        )
        prevBtn.pack(side=LEFT, padx=10)

        playPauseBtn = Button(
            buttonFrame,
            text="⏯",
            width=5,
            command=self.AudioController.TogglePlayPause
        )
        playPauseBtn.pack(side=LEFT, padx=10)

        nextBtn = Button(
            buttonFrame,
            text="⏭",
            width=5,
            command=self.OnNext
        )
        nextBtn.pack(side=LEFT, padx=10)

        # Volume slider 0-100
        # TODO: Add mute button
        volumeSlider = Scale(
            self.ControlFrame,
            from_=0,
            to=100,
            resolution=1,
            orient=HORIZONTAL,
            troughcolor="SkyBlue1",
            label="Volume",
            length=200,
            command = lambda v: self.AudioController.SetVolume(float(v))
        )
        volumeSlider.set(self.AudioController.Volume * 100)
        volumeSlider.configure(relief = "raised", bd = 3)
        volumeSlider.pack(side=RIGHT, padx=20)

        self.MainWindow.update_idletasks()
        frameHeight = self.ControlFrame.winfo_reqheight()
        frameWidth = self.MainWindow.winfo_width()
        # Place at bottom with 10px padding
        self.ControlFrame.place(
            x=0,
            y=self.MainWindow.winfo_height() - frameHeight - 10,
            width=frameWidth,
            height=frameHeight
        )

    def _HideControls(self):
        if self.AudioController.IsPlaying:
            self._AnimateHideStep()

    def _AnimateHideStep(self):
        # Get current y position
        y = self.ControlFrame.winfo_y()
        h = self.ControlFrame.winfo_height()
        max_y = self.MainWindow.winfo_height()  # slide completely off the bottom

        if y < max_y:
            # Move controls down by 5 pixels per step
            y += 5
            self.ControlFrame.place(y=y)
            self.MainWindow.after(10, self._AnimateHideStep)
        else:
            # Fully hidden
            self.ControlFrame.place_forget()

    def _AnimateShowStep(self):
        y = self.ControlFrame.winfo_y()
        targetY = self.MainWindow.winfo_height() - self.ControlFrame.winfo_height()
        x = 0
        width = self.MainWindow.winfo_width()

        if y > targetY:
            y -= 5
            self.ControlFrame.place(x=x, y=y, width=width)
            self.MainWindow.after(10, self._AnimateShowStep)
        else:
            # Ensure exact final position
            self.ControlFrame.place(x=x, y=targetY, width=width)

    def OnPrevious(self):
        # TODO: hook into playlist
        self.AudioController.Stop()

    def OnNext(self):
        # TODO: hook into playlist
        self.AudioController.Stop()

    def Shutdown(self):
        self.AudioController.Stop()
        self.MainWindow.quit()