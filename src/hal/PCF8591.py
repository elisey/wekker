import smbus
import time


class PCF8591:
    def __init__(self, address=0x48, channel=0, bus=1):
        if not (0 <= channel <= 3):
            raise ValueError("Channel must be 0–3")

        self.address = address
        self.channel = channel
        self.bus = smbus.SMBus(bus)

    def read_value(self) -> int:
        """
        Read a stable ADC value from the PCF8591.

        The PCF8591 may return a spurious or invalid value (commonly 128) on initial or unstable reads.
        This method reads up to 4 times and returns the first value that is not equal to 128,
        helping to filter out transient or uninitialized readings.

        Returns:
            int: A stable ADC reading from the input channel. int 0–255
        """
        value = 0
        for i in range(4):
            value = self.__read_value_raw()
            if value != 128:
                break
            time.sleep(0.01)
        return value

    def __read_value_raw(self) -> int:

        """
        Read analog value from selected channel.

        :return: raw_value: int 0–255
        """
        control_byte = 0x40 | self.channel  # Analog input, no auto-increment

        self.bus.write_byte(self.address, control_byte)
        self.bus.read_byte(self.address)  # Dummy read
        time.sleep(0.01)
        return self.bus.read_byte(self.address)
