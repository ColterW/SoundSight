from tkinter import *
from AudioController import AudioController
import FileImporting

class Window:
    # 3 Second inactivity timeout (no mouse movement)
    INACTIVITY_TIMEOUT_MS = 3000

    MainWindow: Frame
    MenuBar: Menu
    ControlFrame: Frame
    FullScreen: bool
    AudioController

    _hideControlsAfterId: str
    _controlsAnimating: bool

    def __init__(self, audioController: AudioController):
        # Setup application window
        self.MainWindow = Tk()
        self.MainWindow.title('SoundSight')

        self.MainWindow.geometry("1280x720")
        self.MainWindow.config(background = "black")

        self.FullScreen = False

        # Require audio controller as it is necessary for the application
        self.AudioController = audioController

        self._InitializeMenuBar()
        self._InitializePlaybackControls()

        # Track mouse activity
        self.MainWindow.bind("<Motion>", self._OnMouseMove)
        self._hideControlsAfterId = None

        # Track application resizing
        self.MainWindow.bind("<Configure>", self._OnResize)
        self._controlsAnimating = False

        self.MainWindow.bind("<F11>", self._ToggleFullscreen)

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
        self.MenuBar = Menu(self.MainWindow)
        filemenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="File", menu = filemenu)

        filemenu.add_command(
            label="Open File", 
            command = self._OpenFile
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

        self.MainWindow.config(menu = self.MenuBar)

    def _InitializePlaybackControls(self):
        self.ControlFrame = Frame(self.MainWindow, bg="black")
        # self.ControlFrame.pack(side=BOTTOM, fill=X, pady=10)

        self.SeekVar = DoubleVar()
        self.SeekBar = Scale(
            self.ControlFrame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            length=800,
            troughcolor="midnight blue",
            variable=self.SeekVar,
            showvalue=0
        )
        self.SeekBar.pack(side=TOP, pady=(0, 5))  # above playback buttons
        self.SeekBar.bind("<ButtonRelease-1>", self._OnSeekRelease)
        self.SeekBar.bind("<Button-1>", self._OnSeekClick)


        self._InitializeButtons()

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

    def _InitializeButtons(self):
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

        self._playPauseBtn = Button(
            buttonFrame,
            text="▷",
            width=5,
            command=self._TogglePlayPause
        )
        self._playPauseBtn.pack(side=LEFT, padx=10)

        stopBtn = Button(
            buttonFrame,
            text="▢",
            width=5,
            command=self._OnStop
        )
        stopBtn.pack(side=LEFT, padx=10)

        nextBtn = Button(
            buttonFrame,
            text="⏭",
            width=5,
            command=self.OnNext
        )
        nextBtn.pack(side=LEFT, padx=10)

    def _OpenFile(self):
        FileImporting.SelectFile(self.AudioController)
        self._playPauseBtn.config(text="⏸")
        self.UpdateSeekBar()

    def _TogglePlayPause(self):
        if self.AudioController.Samples is None:
            return

        self.AudioController.TogglePlayPause()
        self._playPauseBtn.config(text="⏸" if self.AudioController.IsPlaying else "▶")

    def _OnStop(self):
        self.AudioController.Stop()
        self._playPauseBtn.config(text="▷")
        self.SeekBar.set(0)

    def _HideControls(self):
        if self.AudioController.IsPlaying:
            self._AnimateHideStep()

    def _AnimateHideStep(self):
        self._controlsAnimating = True

        # Get current y position
        y = self.ControlFrame.winfo_y()
        maxY = self.MainWindow.winfo_height()  # slide completely off the bottom
        width = self.MainWindow.winfo_width()
        self.ControlFrame.place(x=0, y=y, width=width)

        if y < maxY:
            # Move controls down by 5 pixels per step
            y += 5
            self.ControlFrame.place(y=y)

            if self.MainWindow["menu"] != "":
                self.MainWindow.config(menu="")

            self.MainWindow.after(10, self._AnimateHideStep)
        else:
            # Fully hidden
            self.ControlFrame.place_forget()
            self._controlsAnimating = False

    def _AnimateShowStep(self):
        self._controlsAnimating = True

        y = self.ControlFrame.winfo_y()
        targetY = self.MainWindow.winfo_height() - self.ControlFrame.winfo_height() - 10
        x = 0
        width = self.MainWindow.winfo_width()

        if y > targetY:
            y -= 5
            self.ControlFrame.place(x=x, y=y, width=width)

            if self.MainWindow["menu"] == "":
                self.MainWindow.config(menu=self.MenuBar)

            self.MainWindow.after(10, self._AnimateShowStep)
        else:
            # Ensure exact final position
            self.ControlFrame.place(x=x, y=targetY, width=width)
            self._controlsAnimating = False

    def _OnResize(self, event):
        if hasattr(self, "ControlFrame") and not self._controlsAnimating:
            # Keep the frame at the bottom, filling the width
            frameHeight = self.ControlFrame.winfo_height()
            self.ControlFrame.place(
                x=0,
                y=self.MainWindow.winfo_height() - frameHeight - 10,  # bottom + padding
                width=self.MainWindow.winfo_width()
            )

    def _ToggleFullscreen(self, event=None):
        self.FullScreen = not self.FullScreen
        self.MainWindow.attributes("-fullscreen", self.FullScreen)

    def _ExitFullscreen(self, event=None):
        self.FullScreen = False
        self.MainWindow.attributes("-fullscreen", False)

    def OnPrevious(self):
        # TODO: hook into playlist
        self.AudioController.Stop()

    def OnNext(self):
        # TODO: hook into playlist
        self.AudioController.Stop()

    def _OnSeekClick(self, event):
        # Get total width of the Scale widget
        scaleWidth = self.SeekBar.winfo_width()

        # Clicked x position
        clickX = event.x

        # Calculate corresponding value (0-100)
        newValue = (clickX / scaleWidth) * 100

        # Update the variable
        self.SeekVar.set(newValue)

        # Perform actual seek in audio
        if self.AudioController.Samples is not None:
            totalSamples = len(self.AudioController.Samples)
            newIndex = int(totalSamples * (newValue / 100))
            self.AudioController.Seek(newIndex)

    def _OnSeekRelease(self, event):
        if self.AudioController.Samples is None:
            return

        # Get current slider value
        percent = self.SeekVar.get() / 100
        total_samples = len(self.AudioController.Samples)
        new_index = int(total_samples * percent)

        self.AudioController.Seek(new_index)

    def UpdateSeekBar(self):
        if self.AudioController.Samples is None:
            return

        totalSamples = len(self.AudioController.Samples)
        percent = (self.AudioController._position / totalSamples) * 100
        self.SeekVar.set(percent)
        
        # Schedule next update
        self.MainWindow.after(100, self.UpdateSeekBar)

    def Shutdown(self):
        self.AudioController.Stop()
        self.MainWindow.quit()