# ABOUTME: MPG123 implementation of PlayerUtility for streaming audio playback
# ABOUTME: Handles starting and stopping MPG123 processes for radio streaming

import os
import signal
import subprocess


class MPG123PlayerUtility:
    """MPG123 implementation of the PlayerUtility protocol."""

    PLAYER_UTILITY = "mpg123"

    def __init__(self) -> None:
        self.process: subprocess.Popen | None = None

    def start(self, url: str) -> bool:
        """Start playing the given URL using MPG123."""
        try:
            self.process = subprocess.Popen(
                [self.PLAYER_UTILITY, url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except Exception as e:
            print(f"Failed to start MPG123 for {url}: {e}")
            self.process = None
            return False

    def stop(self) -> None:
        """Stop the currently playing MPG123 process."""
        if self.process and self.process.poll() is None:
            try:
                os.killpg(self.process.pid, signal.SIGTERM)
                self.process.wait(timeout=2)
            except Exception as e:
                print(f"Failed to stop MPG123 process: {e}")

        # Fallback to kill all MPG123 processes
        subprocess.Popen(["killall", self.PLAYER_UTILITY])
        self.process = None

    def is_running(self) -> bool:
        """Check if the MPG123 player is currently running."""
        return self.process is not None and self.process.poll() is None
