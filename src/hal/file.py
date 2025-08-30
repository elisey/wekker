import configparser
from pathlib import Path

from .interface import AnalogInput, BinaryInput, WekkerHardwareAbstract


class WekkerHardwareFile(WekkerHardwareAbstract):
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        print(self.config)

    def get_input_state(self, binary_input: BinaryInput) -> bool:
        try:
            value = self.config.getboolean("BinaryInput", binary_input.name)
            return value
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ValueError(f"Missing binary input: {binary_input.name}") from e

    def get_analog_state(self, analog_input: AnalogInput) -> int:
        try:
            value = self.config.getint("AnalogInput", analog_input.name)
            return value
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ValueError(f"Missing analog input: {analog_input.name}") from e

    def register_binary_input_change_handler(self, binary_input: BinaryInput, handler) -> None:
        raise NotImplementedError
