import sys
import time

from hal import PCF8591, AnalogInput, BinaryInput, WekkerHardwareAbstract, get_hal
from music import FilePlayer, Media, MediaStorage, RadioPlayer
from settings import Settings
from smarthome import DeviceEvent, SmarthomeDevice
from volume_control import VolumeControl
from volume_control.amixer_volume_controller import AmixerVolumeController


class Application:
    def __init__(self):
        self.hw: WekkerHardwareAbstract = get_hal("gpiozero")

        self.file_player = FilePlayer()
        self.radio_player = RadioPlayer()
        self.radio_change_debounce = time.time()
        self.settings = Settings()
        self.settings.load()
        self.smarthome_device = SmarthomeDevice(self.settings)
        self.smarthome_device.connect()
        adc = PCF8591()
        volume_controller = AmixerVolumeController()
        self.volume_control = VolumeControl(adc, volume_controller)
        self.volume_control.start()

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
            if binary_input == BinaryInput.ALARM or binary_input.RADIO:
                self.smarthome_device.trigger_alarm_event(DeviceEvent.ALARM_OFF)
            else:
                self.smarthome_device.trigger_alarm_event(DeviceEvent.RADIO_OFF)
            return

        if binary_input == BinaryInput.ALARM:
            file = MediaStorage().get_media(Media.GROUNDHOG)
            self.file_player.play(file)
            self.smarthome_device.trigger_alarm_event(DeviceEvent.ALARM_ON)
        elif binary_input == BinaryInput.RADIO or binary_input == BinaryInput.BAND:
            result = self.radio_player.play()
            if not result:
                file = MediaStorage().get_media(Media.KRIK)
                self.file_player.play(file)
            if binary_input == BinaryInput.BAND:
                self.smarthome_device.trigger_alarm_event(DeviceEvent.RADIO_ON)
            else:
                self.smarthome_device.trigger_alarm_event(DeviceEvent.ALARM_ON)
        else:
            raise AssertionError("Invalid alarm type")

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
        self.smarthome_device.disconnect()
        print("smarthome_device disconnect done")
        self.volume_control.stop()
        print("volume_control stop done")
        sys.exit(0)
