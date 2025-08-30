import threading
import time

from volume_control.kalman_filter import KalmanFilter
from volume_control.volume_controller import VolumeController


class VolumeControl(threading.Thread):
    """
    A threaded class that reads analog input from an ADC (0–255)
    and maps it to system-wide ALSA volume (0–100).
    Runs in the background and updates volume periodically.
    """
    # todo add interface for adc

    def __init__(self, adc, volume_controller: VolumeController, poll_interval=0.2, min_change=2):
        """
        Args:
            adc: An object with a read_value() -> int method returning values from 0 to 255.
            volume_controller: Implementation of VolumeController protocol for setting system volume.
            poll_interval (float): Time between polls in seconds.
            min_change (int): Minimum change in volume (%) to trigger volume update.
        """
        super().__init__(daemon=True)
        self.adc = adc
        self.volume_controller = volume_controller
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
                #smoothed = self.filter.update(raw_value)
                volume = int(raw_value)
                #volume = self._map_adc_to_volume(smoothed)

            if abs(volume - self.last_volume) >= self.min_change:
                print(f"volume change to {volume}")
                self.volume_controller.set_volume(volume)
                self.last_volume = volume
            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False

    def _map_adc_to_volume(self, adc_value: float) -> int:
        return max(0, min(100, int(adc_value / 255 * 100)))

