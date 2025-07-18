from .file import WekkerHardwareFile
from .gpiozero import WekkerHardwareGpioZero
from .interface import WekkerHardwareAbstract
from .philips import WekkerHardwarePhilips


def get_hal(implementation: str) -> WekkerHardwareAbstract:
    if implementation == "file":
        from pathlib import Path
        return WekkerHardwareFile(Path.cwd() / "hardware.ini")
    elif implementation == "gpiozero":
        return WekkerHardwareGpioZero()
    else:
        return WekkerHardwarePhilips()