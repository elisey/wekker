import enum
import json
from paho.mqtt.client import Client

from settings import Settings

class DeviceEvent(enum.Enum):
    ALARM_ON = "ALARM_ON"
    ALARM_OFF = "ALARM_OFF"
    RADIO_ON = "RADIO_ON"
    RADIO_OFF = "RADIO_OFF"

    @classmethod
    def events_as_str(cls):
        return [event.value for event in cls]

class SmarthomeDevice:
    def __init__(self, settings: Settings):
        self.device_id = settings.device_id
        self.event_topic = f"{self.device_id}/event/alarm"
        self.discovery_topic = f"homeassistant/event/{self.device_id}/alarm/config"

        self.client = Client(client_id=self.device_id)
        self.client.username_pw_set(settings.mqtt_user, settings.mqtt_password)
        self.client.on_connect = self._on_connect

        self.host = settings.mqtt_host
        self.port = settings.mqtt_port

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code", rc)
        self.publish_discovery()

    def __get_device_payload(self) -> dict:
        return {
                "identifiers": [self.device_id],
                "name": "Wekker",
                "manufacturer": "Enot Labs",
                "model": "Wekker 1.0",
                "sw_version": "0.1.0"
            }

    def publish_discovery(self):
        event_payload = {
            "unique_id": f"{self.device_id}_alarm_event",
            "name": "Wekker Alarm Event",
            "object_id": "wekker_alarm_event",
            "icon": "mdi:alarm-bell",
            "enabled_by_default": True,
            "entity_category": "diagnostic",
            "state_topic": self.event_topic,
            "event_types": DeviceEvent.events_as_str(),
            "device": self.__get_device_payload()
        }
        self.client.publish(self.discovery_topic, json.dumps(event_payload), retain=True)
        print("Discovery config published.")

    def connect(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def trigger_alarm_event(self, event: DeviceEvent):
        event_payload = {
            "event_type": event.value
        }
        print("Triggering alarm event!")
        self.client.publish(self.event_topic, json.dumps(event_payload))

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
