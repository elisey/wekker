# ABOUTME: Protocol interface for volume control implementations
# ABOUTME: Defines abstract contract for setting system volume levels

from typing import Protocol


class VolumeController(Protocol):
    """Protocol for volume control implementations."""

    def set_volume(self, volume: int) -> None:
        """
        Set the system volume to the specified level.

        Args:
            volume: Volume level (0-100)
        """
        ...
