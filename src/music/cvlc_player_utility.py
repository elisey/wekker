# ABOUTME: CVLC implementation of PlayerUtility for streaming audio playback
# ABOUTME: Handles starting and stopping CVLC processes for radio streaming

import os
import signal
import subprocess


class CVLCPlayerUtility:
    """CVLC implementation of the PlayerUtility protocol."""

    PLAYER_UTILITY = "cvlc"
    PLAYER_UTILITY_CMD = [PLAYER_UTILITY, "--aout=alsa", "--intf", "dummy", "--quiet"]

    def __init__(self) -> None:
        self.process: subprocess.Popen | None = None

    def start(self, url: str) -> bool:
        """Start playing the given URL using CVLC."""
        try:
            self.process = subprocess.Popen(
                self.PLAYER_UTILITY_CMD + [url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except Exception as e:
            print(f"Failed to start CVLC for {url}: {e}")
            self.process = None
            return False

    def stop(self) -> None:
        """Stop the currently playing CVLC process."""
        if self.process and self.process.poll() is None:
            try:
                os.killpg(self.process.pid, signal.SIGTERM)
                self.process.wait(timeout=2)
            except Exception as e:
                print(f"Failed to stop CVLC process: {e}")

        # Fallback to kill all CVLC processes
        subprocess.Popen(["killall", self.PLAYER_UTILITY])
        self.process = None

    def is_running(self) -> bool:
        """Check if the CVLC player is currently running."""
        return self.process is not None and self.process.poll() is None
