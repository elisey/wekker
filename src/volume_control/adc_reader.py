# ABOUTME: Protocol interface for ADC (Analog-to-Digital Converter) implementations
# ABOUTME: Defines abstract contract for reading analog values from hardware

from typing import Protocol


class ADCReader(Protocol):
    """Protocol for ADC reader implementations."""

    def read_value(self) -> int:
        """
        Read analog value from the ADC.

        Returns:
            int: Analog value typically in range 0-255
        """
        ...
