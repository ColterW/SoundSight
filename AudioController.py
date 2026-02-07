from pydub import AudioSegment
import numpy as np
import sounddevice as sd

class AudioController:
    def __init__(self):
        self.Samples = None
        self.SampleRate = None
        self.Volume = 0.1 # 10% volume by default; trust me, it's necessary

    def LoadFile(self, path):
        audio = AudioSegment.from_file(path)
        self.SampleRate = audio.frame_rate

        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))
        self.Samples = samples.astype(np.float32) / (2 ** 15)

    def Play(self):
        if self.Samples is None:
            return

        scaledSamples = self.Samples * self.Volume
        sd.play(scaledSamples, self.SampleRate)

    def Stop(self):
        sd.stop()

    def SetVolume(self, value):
        self.Volume = max(0.0, min(1.0, value))