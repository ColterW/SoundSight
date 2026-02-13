import numpy as np
from AudioController import AudioController

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
