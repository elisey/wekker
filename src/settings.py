import configparser
from dataclasses import dataclass, field
from pathlib import Path


class SettingsLoadError(Exception):
    """Custom exception for errors loading settings."""


@dataclass
class Settings:
    mqtt_host: str = field(default="")
    mqtt_port: int = field(default=1883)
    mqtt_user: str = field(default="")
    mqtt_password: str = field(default="")
    serial_number: str = "1"
    device_name: str = "wekker"
    device_id: str = f"{device_name}_{serial_number}"

    def load(self):
        config_path = Path.home() / ".config" / "wekker" / "settings.ini"

        if not config_path.exists():
            raise SettingsLoadError(f"Settings file not found: {config_path}")

        config = configparser.ConfigParser()
        config.read(config_path)

        if "mqtt" not in config:
            raise SettingsLoadError("Missing [mqtt] section in settings file.")

        self.mqtt_host = config["mqtt"].get("host", "localhost")
        self.mqtt_port = config["mqtt"].getint("port", 1883)
        self.mqtt_user = config["mqtt"].get("username", "")
        self.mqtt_password = config["mqtt"].get("password", "")
