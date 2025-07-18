import time
import threading
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from collections import deque

class CapacitorMeter:
    def __init__(self, on_change_callback, pin: int = 23, interval: float = 0.3, buffer_size: int = 10):
        self.on_change_callback = on_change_callback
        self.pin = pin
        self.interval = interval
        self._running = False
        self._thread = None
        self._buffer_size = buffer_size
        self._measurements = deque(maxlen=buffer_size)
        self._prev_mean_measurement = 0

    def _measure_once(self):
        # Разрядка
        pin_out = DigitalOutputDevice(self.pin)
        pin_out.off()
        time.sleep(0.1)
        pin_out.close()

        # Зарядка
        pin_in = DigitalInputDevice(self.pin, pull_up=True)
        start = time.monotonic()
        timeout = 1.0  # 1 секунда максимум на заряд

        while not pin_in.value:
            if time.monotonic() - start > timeout:
                print("ОШИБКА: превышено время зарядки")
                pin_in.close()
                return None

        elapsed = time.monotonic() - start
        pin_in.close()
        return elapsed

    def _run(self):
        while self._running:
            result = self._measure_once()
            if result is None:
                print("⚠️  Таймаут: конденсатор не зарядился")
            else:
                self._measurements.append(result)

                current_mean_measurement = self.get_value()
                if current_mean_measurement != self._prev_mean_measurement:
                    self._prev_mean_measurement = current_mean_measurement
                    if self.on_change_callback is not None:
                        self.on_change_callback(current_mean_measurement)
                print(f"⏱️  Время зарядки: {result:.3f} мс")
            time.sleep(self.interval)

    def get_value(self):
        if not self._measurements:
            return None
        return sum(self._measurements) / len(self._measurements)  # среднее по буферу

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print("🔄 Измерение запущено")

    def stop(self):
        if self._running:
            self._running = False
            self._thread.join()
            print("🛑 Измерение остановлено")


# Пример использования
if __name__ == "__main__":
    try:
        meter = CapacitorMeter(pin=23)
        meter.start()
        while True:
            time.sleep(1)
            val = meter.get_value()
            print(f"Среднее значение за последние измерения: {val}")
    except KeyboardInterrupt:
        print("\n🚪 Выход по Ctrl+C")
        meter.stop()
