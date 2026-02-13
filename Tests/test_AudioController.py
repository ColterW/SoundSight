import numpy as np
from AudioController import AudioController
from unittest.mock import MagicMock, Mock, patch

def test_LoadFileSetsSamples():
    fake_audio = MagicMock()
    fake_audio.frame_rate = 44100
    fake_audio.channels = 1
    fake_audio.get_array_of_samples.return_value = [0, 1, -1]

    ac = AudioController()

    with patch("AudioController.AudioSegment.from_file", return_value=fake_audio):
        ac.LoadFile("test.wav")

    assert ac.SampleRate == 44100
    assert ac.Samples is not None


def test_SetVolumeClampsLow():
    ac = AudioController()
    ac.SetVolume(-1)
    assert ac.Volume == 0.0


def test_SetVolumeClampsHigh():
    ac = AudioController()
    ac.SetVolume(2)
    assert ac.Volume == 1.0


def test_SetVolumeValid():
    ac = AudioController()
    ac.SetVolume(0.5)
    assert ac.Volume == 0.5

def test_PlayWithoutSamplesDoesNothing():
    ac = AudioController()
    ac.Play() # Shouldn't crash

def test_PlayCreatesAndStartsStream():
    ac = AudioController()
    ac.Samples = np.zeros(1000, dtype=np.float32)
    ac.SampleRate = 44100

    mock_stream = Mock()

    with patch("AudioController.sd.OutputStream", return_value=mock_stream):
        ac.Play()

    mock_stream.start.assert_called_once()