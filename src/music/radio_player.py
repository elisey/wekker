import time

from .file_player import FilePlayer
from .media_storage import MediaStorage
from .player_utility import PlayerUtility
from .radio_storage import RadioStorage


class RadioPlayer:
    def __init__(self, player_utility: PlayerUtility) -> None:
        self.player_utility = player_utility
        self.status: bool = False
        self.radio_storage = RadioStorage()

    def play(self, go_to_next_station: bool = False) -> bool:
        if self.status:
            return True

        for _ in range(10):
            if go_to_next_station:
                url = self.radio_storage.get_next_radio()
            else:
                url = self.radio_storage.get_current_radio()
                go_to_next_station = True
            result = self.__start(url)
            if result:
                return True

        print("Error start radio")
        return False

    def __start(self, url: str) -> bool:
        print(f"RADIO TRY START {url}")

        if not self.player_utility.start(url):
            self.status = False
            return False

        try:
            start_time = time.time()
            timeout = 1.5

            while time.time() - start_time < timeout:
                if not self.player_utility.is_running():
                    print("Player exited early")
                    self.status = False
                    return False
                time.sleep(0.1)  # check every 100ms

            self.status = True
            return True
        except Exception as e:
            print(f"Failed to play {url}: {e}")
            self.status = False
            return False

    def change(self) -> None:
        if not self.status:
            return

        media_storage = MediaStorage()
        music_player = FilePlayer()

        static_noice_file = media_storage.get_radio_static_noise()
        print(f"static_noice_file: {static_noice_file}")
        music_player.play(static_noice_file)
        time.sleep(0.5)
        self.stop()
        time.sleep(0.5)
        self.play(go_to_next_station=True)
        time.sleep(0.5)
        music_player.stop()

    def stop(self) -> None:
        print("RADIO STOP")
        self.status = False
        self.player_utility.stop()
