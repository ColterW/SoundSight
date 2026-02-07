from pydub import AudioSegment
import numpy as np
import sounddevice as sd

class AudioController:
    def __init__(self):
        self.Samples = None
        self.SampleRate = None
        self.Volume = 0.1 # 10% volume by default; trust me, it's necessary

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

        scaledSamples = self.Samples * self.Volume
        sd.play(scaledSamples, self.SampleRate)

    def Stop(self):
        """
        Stop playback of currently loaded audio file.
        """
        sd.stop()

    def SetVolume(self, value: float) -> None:
        """
        Sets playback volume of currently loaded audio file.
        
        Caps minimum volume to 0.0 and maximum volume to 1.0.
        
        Args:
            value (float): New value for audio volume.
        """
        self.Volume = max(0.0, min(1.0, value))