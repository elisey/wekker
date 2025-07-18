from .interface import AnalogInput, BinaryInput, WekkerHardwareAbstract

try:
    import RPi.GPIO as GPIO
except:
    pass

class WekkerHardwarePhilips(WekkerHardwareAbstract):
    PIN_ALARM_INPUT = 22
    PIN_RADIO_INPUT = 27
    PIN_BAND_INPUT = 24
    PIN_TUNE_INPUT = 23
    BINARY_INPUT_DEBOUNCE = 150

    INPUT_TO_PIN = {
        BinaryInput.ALARM: PIN_ALARM_INPUT,
        BinaryInput.RADIO: PIN_RADIO_INPUT,
        BinaryInput.BAND: PIN_BAND_INPUT,
    }
    PIN_TO_INPUT = {pin: input_ for input_, pin in INPUT_TO_PIN.items()}

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.PIN_ALARM_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN_ALARM_INPUT, GPIO.BOTH, callback=self.__on_binary_input_change, bouncetime=self.BINARY_INPUT_DEBOUNCE)

        GPIO.setup(self.PIN_RADIO_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN_RADIO_INPUT, GPIO.BOTH, callback=self.__on_binary_input_change, bouncetime=self.BINARY_INPUT_DEBOUNCE)

        GPIO.setup(self.PIN_BAND_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN_BAND_INPUT, GPIO.BOTH, callback=self.__on_binary_input_change, bouncetime=self.BINARY_INPUT_DEBOUNCE)


        GPIO.setup(self.PIN_TUNE_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        self.input_to_event_handler = {}



        #create task to scan volume and tune

    def register_binary_input_change_handler(self, binary_input: BinaryInput, handler) -> None:
        # todo add checking keyerror
        self.input_to_event_handler[binary_input] = handler

    def get_input_state(self, binary_input: BinaryInput) -> bool:
        # todo add checking keyerror
        pin = self.INPUT_TO_PIN[binary_input]
        return GPIO.input(pin) == GPIO.HIGH

    def __on_binary_input_change(self, pin: int) -> None:
        # todo add checking keyerror
        binary_input = self.PIN_TO_INPUT[pin]
        state = GPIO.input(pin) == GPIO.HIGH

        try:
            handler = self.input_to_event_handler[binary_input]
        except KeyError:
            print(f"No handler registered for {binary_input.name}")
            return
        handler(binary_input, state)

    def get_analog_state(self, analog_input: AnalogInput) -> int:
        pass
