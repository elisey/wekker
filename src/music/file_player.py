import pygame as pg


class FilePlayer:
    def __init__(self) -> None:
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 2048  # number of samples (experiment to get right sound)
        pg.mixer.init(freq, bitsize, channels, buffer)

    def play(self, filename: str) -> bool:
        pg.mixer.music.load(filename)
        pg.mixer.music.play()
        return True

    def stop(self) -> None:
        pg.mixer.music.fadeout(1000)
        pg.mixer.music.stop()
