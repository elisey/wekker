import sys
import time

from hal import WekkerHardwareAbstract, get_hal, BinaryInput, AnalogInput
from music import FilePlayer, RadioPlayer, MediaStorage, Media


class Application:
    def __init__(self):
        self.hw: WekkerHardwareAbstract = get_hal("gpiozero")

        self.file_player = FilePlayer()
        self.radio_player = RadioPlayer()
        self.radio_change_debounce = time.time()

    def run(self):
        self.hw.register_binary_input_change_handler(BinaryInput.ALARM, self.__on_binary_input_change)
        self.hw.register_binary_input_change_handler(BinaryInput.RADIO, self.__on_binary_input_change)
        self.hw.register_binary_input_change_handler(BinaryInput.BAND, self.__on_binary_input_change)

        self.__reset_radio_change_debounce()
        self.hw.register_analog_input_change_handler(AnalogInput.TUNE, self.__on_tune_change)

        while True:
            time.sleep(1)

    def __on_binary_input_change(self, binary_input: BinaryInput, state: bool):
        print(f"Callback __on_binary_input_change called for input={binary_input.name}, state={state} ")
        if state:
            self.file_player.stop()
            self.radio_player.stop()
            return

        if binary_input == BinaryInput.ALARM:
            file = MediaStorage().get_media(Media.GROUNDHOG)
            self.file_player.play(file)
        elif binary_input == BinaryInput.RADIO or binary_input == BinaryInput.BAND:
            result = self.radio_player.play()
            if not result:
                file = MediaStorage().get_media(Media.KRIK)
                self.file_player.play(file)

        else:
            assert False

    def __can_change_radio(self) -> bool:
        current_time = time.time()

        if (current_time - self.radio_change_debounce) > 5:
            self.radio_change_debounce = current_time
            return True

    def __reset_radio_change_debounce(self) -> None:
        self.radio_change_debounce = time.time()

    def __on_tune_change(self, input: AnalogInput, value: int):
        if self.__can_change_radio():
            self.radio_player.change()

    def stop(self, signum, frame) -> None:
        print("Stopping application")
        self.hw.close()
        print("HW stop done")
        self.radio_player.stop()
        print("radio player stop done")
        self.file_player.stop()
        print("file player stop done")
        sys.exit(0)
