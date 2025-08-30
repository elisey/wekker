from gpiozero import Button

from .capasitor_meter_old import CapacitorMeter
from .interface import AnalogInput, BinaryInput, WekkerHardwareAbstract


class WekkerHardwareGpioZero(WekkerHardwareAbstract):
    PIN_ALARM_INPUT = 22
    PIN_RADIO_INPUT = 27
    PIN_BAND_INPUT = 24
    PIN_TUNE_INPUT = 23  # No direct support in gpiozero; handle manually if analog
    BINARY_INPUT_DEBOUNCE = 0.15  # seconds

    INPUT_TO_PIN = {
        BinaryInput.ALARM: PIN_ALARM_INPUT,
        BinaryInput.RADIO: PIN_RADIO_INPUT,
        BinaryInput.BAND: PIN_BAND_INPUT,
    }
    PIN_TO_INPUT = {pin: input_ for input_, pin in INPUT_TO_PIN.items()}

    def __init__(self):
        self.input_to_event_handler = {}
        self.capasitor_meter = CapacitorMeter(on_change_callback=self.__on_capasitor_meter_change)
        self.capasitor_meter.start()
        self._buttons = {
            binary_input: Button(pin, pull_up=True, bounce_time=self.BINARY_INPUT_DEBOUNCE)
            for binary_input, pin in self.INPUT_TO_PIN.items()
        }

        for binary_input, button in self._buttons.items():
            button.when_pressed = lambda bi=binary_input: self.__handle_change(bi, False)
            button.when_released = lambda bi=binary_input: self.__handle_change(bi, True)

    def close(self):
        self.capasitor_meter.stop()
        for button in self._buttons.values():
            button.close()

    def register_binary_input_change_handler(self, binary_input: BinaryInput, handler) -> None:
        self.input_to_event_handler[binary_input] = handler

    def register_analog_input_change_handler(self, analog_input: AnalogInput, handler) -> None:
        self.input_to_event_handler[analog_input] = handler

    def get_input_state(self, binary_input: BinaryInput) -> bool:
        return self._buttons[binary_input].is_pressed is False  # Active-low with pull-up

    def __handle_change(self, binary_input: BinaryInput, state: bool) -> None:
        handler = self.input_to_event_handler.get(binary_input)
        if handler:
            handler(binary_input, state)
        else:
            print(f"No handler registered for {binary_input.name}")

    def __on_capasitor_meter_change(self, value: int):
        print(f"__on_capasitor_meter_change callback. value {value}")
        handler = self.input_to_event_handler.get(AnalogInput.TUNE)
        if handler:
            handler(AnalogInput.TUNE, value)
        else:
            print(f"No handler registered for {AnalogInput.TUNE}")

    def get_analog_state(self, analog_input: AnalogInput) -> int:
        if analog_input.TUNE:
            return self.capasitor_meter.get_value()
        raise NotImplementedError("Analog input not implemented")
