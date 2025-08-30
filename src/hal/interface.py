import abc
import enum


class BinaryInput(enum.Enum):
    ALARM = 1
    RADIO = 2
    BAND = 3


class AnalogInput(enum.Enum):
    VOLUME = 1
    TUNE = 2


class WekkerHardwareAbstract(abc.ABC):
    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def register_binary_input_change_handler(self, binary_input: BinaryInput, handler) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def register_analog_input_change_handler(self, binary_input: AnalogInput, handler) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_input_state(self, binary_input: BinaryInput) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_analog_state(self, analog_input: AnalogInput) -> int:
        raise NotImplementedError
