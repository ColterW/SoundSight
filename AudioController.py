from pydub import AudioSegment
import numpy as np
import sounddevice as sd

class AudioController:
    Samples: np.float32
    SampleRate: any
    Volume: float
    IsPlaying: bool
    _position: int
    _stream: sd.OutputStream

    def __init__(self):
        self.Samples = None
        self.SampleRate = None
        self.Volume = 0.1 # 10% volume by default; trust me, it's necessary
        self.IsPlaying = False
        self._position = 0
        self._stream = None

    def _callback(self, outdata, frames, time, status):
        """
        Output stream callback for real-time audio playback.

        This method is called repeatedly by the SoundDevice OutputStream to provide
        audio samples to the audio hardware in chunks. It reads a slice of the
        currently loaded audio buffer (`self.Samples`), applies the current volume
        (`self.Volume`), and writes it into `outdata`.

        Args:
            outdata (numpy.ndarray): Array to be filled with audio samples for playback.
            frames (int): Number of frames requested by the output stream.
            time (CData): Timing information provided by SoundDevice (not used here).
            status (CallbackFlags): Status flags from the audio stream (e.g., underflow).

        Behavior:
            - If `status` contains warnings, they are printed.
            - Fills `outdata` with the next `frames` of audio from `self.Samples`.
            - If the end of the buffer is reached, the remaining portion of `outdata`
            is filled with zeros and the callback signals the stream to stop.
            - Updates `self._position` to keep track of playback progress.

        Raises:
            sd.CallbackStop: Raised when the end of the audio buffer is reached to stop playback.
        """
        if status:
            print(status)

        end = self._position + frames
        chunk = self.Samples[self._position:end]

        if len(chunk) < frames:
            outdata[:len(chunk)] = chunk * self.Volume
            outdata[len(chunk):] = 0
            raise sd.CallbackStop
        else:
            outdata[:] = chunk * self.Volume

        self._position = end

    def LoadFile(self, path: str) -> None:
        """
        Load an audio file from disk.
        
        Args:
            path (str): Path to the audio file.
        """
        audio = AudioSegment.from_file(path)
        self.SampleRate = audio.frame_rate

        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))
        self.Samples = samples.astype(np.float32) / (2 ** 15)

    def Play(self) -> None:
        """
        Play currently loaded audio file.
        """
        if self.Samples is None:
            return

        # If stream exists but stopped, restart
        if self._stream is None:
            self._stream = sd.OutputStream(
                samplerate=self.SampleRate,
                channels=self.Samples.shape[1] if self.Samples.ndim > 1 else 1,
                callback=self._callback
            )
            self._stream.start()
        elif not self._stream.active:
            # Stream exists but was paused
            self._stream.start()

        self.IsPlaying = True

    def Pause(self) -> None:
        """
        Pause playback of currently loaded audio file.
        """
        if self._stream:
            self._stream.stop()
            self.IsPlaying = False

    def TogglePlayPause(self):
        """
        Toggle between playing and pausing of the currently loaded audio file.
        """
        if self.IsPlaying:
            self.Pause()
        else:
            self.Play()

    def Stop(self):
        """
        Stop playback of currently loaded audio file.

        This closes the stream.
        """
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self.IsPlaying = False

    def SetVolume(self, value: float) -> None:
        """
        Sets playback volume of currently loaded audio file.

        Caps minimum volume to 0.0 and maximum volume to 1.0.
        
        Args:
            value (float): New value for audio volume.
        """
        self.Volume = max(0.0, min(1.0, float(value)))