import enum
import random


class Media(enum.Enum):
    GROUNDHOG = "/home/wekker/surok.mp3"
    KRIK = "/home/wekker/krik.mp3"


radio_static_noise = [
    "/home/wekker/radio1.mp3",
    "/home/wekker/radio2.mp3",
    # "/home/wekker/radio3.mp3",
    # "/home/wekker/radio4.mp3",
    "/home/wekker/radio5.mp3",
    "/home/wekker/radio6.mp3",
]


class MediaStorage:

    def get_media(self, media: Media) -> str:
        return media.value

    def get_radio_static_noise(self) -> str:
        return random.choice(radio_static_noise)
