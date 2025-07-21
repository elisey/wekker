import subprocess
import os
import signal
import time

from .media_storage import MediaStorage
from .file_player import FilePlayer
from .radio_storage import RadioStorage


class RadioPlayer:
    def __init__(self) -> None:
        self.process: subprocess.Popen | None = None
        self.status: bool = False
        self.radio_storage = RadioStorage()

    def play(self, go_to_next_station: bool = False) -> bool:
        if self.status:
            return True

        for i in range(10):
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
        try:
            self.process = subprocess.Popen(
                ["mpg123", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print(f"PID: {self.process.pid}")

            start_time = time.time()
            timeout = 1.5

            while time.time() - start_time < timeout:
                if self.process.poll() is not None:
                    print(f"mpg123 exited early with code {self.process.returncode}")
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
        print(f"Process: {self.process}")

        self.status = False
        if self.process and self.process.poll() is None:
            try:
                os.killpg(self.process.pid, signal.SIGTERM)
                self.process.wait(timeout=2)
            except Exception as e:
                print(f"Failed to stop process: {e}")
            finally:
                self.process = None
        subprocess.Popen(["killall", "mpg123"])