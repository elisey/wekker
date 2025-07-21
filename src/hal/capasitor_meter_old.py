import time
import threading
import RPi.GPIO as GPIO
from collections import deque

class CapacitorMeter:
    def __init__(self, on_change_callback=None, pin: int = 23, interval: float = 0.1, buffer_size: int = 3):
        self.on_change_callback = on_change_callback
        self.pin = pin
        self.interval = interval
        self._running = False
        self._thread = None
        self._buffer_size = buffer_size
        self._measurements = deque(maxlen=buffer_size)
        self._prev_mean_measurement = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def _measure_once(self):
        # Разрядка
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.1)

        # Зарядка
        GPIO.setup(self.pin, GPIO.IN)
        counter = 0
        max_count = 100
        start_time = time.monotonic()
        while GPIO.input(self.pin) == GPIO.LOW:
            # time.sleep(0.01)
            counter += 1
            # if counter >= max_count:
            #     print("ОШИБКА ЗАРЯДКИ")
            #     return None
        elapsed_time = int((time.monotonic() - start_time) * 1000000)
        #print(f"Время зарядки: {elapsed_time}")
        return elapsed_time

    def _run(self):
        while self._running:
            result = self._measure_once()
            if result is None:
                print("⚠️  Таймаут: конденсатор не зарядился")
            else:
                self._measurements.append(result)

                current_mean_measurement = self.get_value() // 25
                if self._prev_mean_measurement is None:
                    self._prev_mean_measurement = current_mean_measurement
                if abs(current_mean_measurement - self._prev_mean_measurement) > 10:
                    self._prev_mean_measurement = current_mean_measurement
                    if self.on_change_callback is not None:
                        self.on_change_callback(current_mean_measurement)

                #print(f"⏱️  Время зарядки (в условных единицах): {current_mean_measurement}")
            time.sleep(self.interval)

    def get_value(self):
        if not self._measurements:
            return None
        return sum(self._measurements) / len(self._measurements)

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
            GPIO.cleanup(self.pin)
            print("🛑 Измерение остановлено")
