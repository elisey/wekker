# ABOUTME: Protocol interface for media player utilities used by RadioPlayer
# ABOUTME: Defines the contract for starting and stopping media playback processes

from typing import Protocol


class PlayerUtility(Protocol):
    """Protocol for media player utilities that can play streaming URLs."""

    def start(self, url: str) -> bool:
        """Start playing the given URL. Returns True if successful."""
        ...

    def stop(self) -> None:
        """Stop the currently playing media."""
        ...

    def is_running(self) -> bool:
        """Check if the player is currently running."""
        ...
