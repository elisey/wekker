import enum
import threading
import time

from .adc_reader import ADCReader
from .volume_controller import VolumeController


class FadeState(enum.Enum):
    NORMAL = 1
    FADE_IN = 2


class VolumeControl(threading.Thread):
    """
    A threaded class that reads analog input from an ADC (0–255)
    and maps it to system-wide ALSA volume (0–100).
    Runs in the background and updates volume periodically.
    """

    # Class constants
    FADE_IN_DURATION_MS = 15000
    POLL_INTERVAL_MS = 300
    POLL_INTERVAL_S = 0.3

    def __init__(self, adc: ADCReader, volume_controller: VolumeController):
        """
        Args:
            adc: ADCReader implementation for reading analog values from 0 to 255.
            volume_controller: Implementation of VolumeController protocol for setting system volume.
        """
        super().__init__(daemon=True)
        self.adc = adc
        self.volume_controller = volume_controller
        self.running = True
        self.fade_state = FadeState.NORMAL
        self.fade_position = 0
        self._stop_event = threading.Event()
        self.current_value = None

    def run(self):
        while self.running:
            loop_start = time.time()

            current_volume = self.__read_volume_control()
            fade_coefficient = self.__process_fade_state()
            adjusted_volume = int(current_volume * fade_coefficient)
            self.__set_volume(adjusted_volume)

            processing_time = time.time() - loop_start
            sleep_time = max(0, self.POLL_INTERVAL_S - processing_time)
            if self._stop_event.wait(sleep_time):
                break

    def __set_volume(self, volume: int) -> None:
        # print(f"set volume called to {volume}")
        if self.current_value is None or volume != self.current_value:
            start_time = time.time()
            self.volume_controller.set_volume(volume)
            execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            print(f"set_volume {volume} execution time: {execution_time:.2f}ms")
            self.current_value = volume

    def __read_volume_control(self) -> int:
        raw_value = self.adc.read_value()
        if raw_value <= 1:
            volume = 0
        else:
            volume = int(raw_value)
        return volume

    def stop(self):
        self.running = False
        self._stop_event.set()

    def __process_fade_state(self) -> float:
        """Calculate volume fade coefficient based on current state."""
        if self.fade_state == FadeState.NORMAL:
            return 1.0
        elif self.fade_state == FadeState.FADE_IN:
            if self.fade_position >= self.FADE_IN_DURATION_MS:
                self.fade_state = FadeState.NORMAL
                print("[VolumeControl] Fade-in complete")
                return 1.0

            coefficient = self.fade_position / self.FADE_IN_DURATION_MS
            self.fade_position += self.POLL_INTERVAL_MS

            # progress_percent = int(coefficient * 100)
            # print(f"[VolumeControl] Fade-in progress: {progress_percent}%")

            return coefficient

        return 1.0

    def start_fade_in(self) -> None:
        """Start fade-in effect from current position."""
        self.fade_state = FadeState.FADE_IN
        self.fade_position = 0
        print("[VolumeControl] Starting fade-in")
