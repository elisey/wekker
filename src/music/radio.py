import subprocess
import os
import signal
import time

from radio_picker import RadioStorage
from music.player import Player

class Radio:
    def __init__(self) -> None:
        self.process: subprocess.Popen | None = None
        self.status: bool = False
        self.radio_storage = RadioStorage()
        self.music_player = Player()

    def play(self) -> bool:
        if self.status:
            return True
        for i in range(10):
            url = self.radio_storage.get_next_radio()
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
            self.status = True
            return True
        except Exception as e:
            print(f"Failed to play {url}: {e}")

            return False

    def change(self) -> None:
        if not self.status:
            return
        static_file = self.radio_storage.get_next_static()
        print(f"stati file: {static_file}")
        self.music_player.play(static_file)
        time.sleep(0.5)
        self.stop()
        time.sleep(0.5)
        self.play()
        time.sleep(0.5)
        self.music_player.stop()

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