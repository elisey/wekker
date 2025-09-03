import time

import smbus


class PCF8591:
    def __init__(self, address=0x48, channel=0, bus=1):
        if not (0 <= channel <= 3):
            raise ValueError("Channel must be 0–3")

        self.address = address
        self.channel = channel
        self.bus = smbus.SMBus(bus)

    def read_value(self) -> int:
        """
        Read raw analog value from selected channel.

        Returns:
            int: Raw ADC reading from the input channel. Range 0-255
        """
        control_byte = 0x40 | self.channel  # Analog input, no auto-increment

        self.bus.write_byte(self.address, control_byte)
        self.bus.read_byte(self.address)  # Dummy read
        time.sleep(0.01)
        return self.bus.read_byte(self.address)
