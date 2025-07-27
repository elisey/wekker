import threading
import time
import subprocess

from volume_control.kalman_filter import KalmanFilter


class VolumeControl(threading.Thread):
    """
    A threaded class that reads analog input from an ADC (0–255)
    and maps it to system-wide ALSA volume (0–100).
    Runs in the background and updates volume periodically.
    """
    # todo add interface for adc

    def __init__(self, adc, poll_interval=0.5, min_change=2):
        """
        Args:
            adc: An object with a read_value() -> int method returning values from 0 to 255.
            poll_interval (float): Time between polls in seconds.
            min_change (int): Minimum change in volume (%) to trigger ALSA update.
        """
        super().__init__(daemon=True)
        self.adc = adc
        self.poll_interval = poll_interval
        self.min_change = min_change
        self.running = True
        self.last_volume = -1
        self.filter = KalmanFilter(process_variance=1335.0, measurement_variance=154.0)

    def run(self):
        while self.running:
            raw_value = self.adc.read_value()
            if raw_value <= 1:
                volume = 0
            else:
                smoothed = self.filter.update(raw_value)
                volume = int(smoothed)
                #volume = self._map_adc_to_volume(smoothed)

            if abs(volume - self.last_volume) >= self.min_change:
                self.set_system_volume(volume)
                self.last_volume = volume
            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False

    def _map_adc_to_volume(self, adc_value: float) -> int:
        return max(0, min(100, int(adc_value / 255 * 100)))

    def set_system_volume(self, volume: int):
        try:
            subprocess.run(
                ["amixer", "sset", "PCM", f"{volume}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as e:
            print(f"[VolumeControl] Failed to set volume: {e}")
