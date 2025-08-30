# ABOUTME: ALSA amixer implementation of volume control
# ABOUTME: Controls system volume using the amixer command-line tool

import subprocess

from volume_control.volume_controller import VolumeController


class AmixerVolumeController:
    """Volume controller implementation using ALSA amixer."""
    
    def set_volume(self, volume: int) -> None:
        """
        Set the system volume using amixer.
        
        Args:
            volume: Volume level (0-100)
        """
        try:
            subprocess.run(
                ["amixer", "sset", "PCM", f"{volume}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as e:
            print(f"[AmixerVolumeController] Failed to set volume: {e}")