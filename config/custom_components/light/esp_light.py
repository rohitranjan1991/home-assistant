"""
homeassistant.components.light.esp_light
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ESPLight platform that implements lights.

"""
from homeassistant.components import mqtt
import json
from homeassistant.components.light import (
    Light, ATTR_BRIGHTNESS, ATTR_XY_COLOR)

DEPENDENCIES = ['mqtt']

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return esp lights. """

    lights = config.get('lights', {})
    devices = []

    for dev_name, properties in lights.items():
        devices.append(
            ESPLight(
                hass,
                properties.get('light_id', dev_name),
                properties.get('light_name', 'esp_light'),
                properties.get('light_state', False),
                properties.get('command_topic', ''),
                properties.get('state_topic', ''),
                properties.get('switch_number', '')
            )
        )

    add_devices_callback(devices)



class ESPLight(Light):

    """ Provides a espLight switch. """
    def __init__(self,hass, id, name, state,command_topic,state_topic,switch_number):
        self._hass = hass
        self._id = id
        self._name = name
        self._state = state
        self._switch_number = switch_number
        self._command_topic = command_topic
        self._state_topic = state_topic


        def message_received(topic, payload, qos):
            """ A new MQTT message has been received. """
            data = json.loads(payload)
            if  self._switch_number == int(data["switch"]):
                self._state = True if int(data["state"]) == 1 else False
                self.update_ha_state()

        if self._state_topic is not None:
            # subscribe the state_topic
            mqtt.subscribe(hass, self._state_topic, message_received,1)

    @property
    def should_poll(self):
        """ No polling needed for a demo light. """
        return False

    @property
    def name(self):
        """ Returns the name of the device if any. """
        return self._name

    @property
    def is_on(self):
        """ True if device is on. """
        return self._state

    def turn_on(self, **kwargs):
        """ Turn the device on. """
        self._state = True
        #mqtt.publish(self._hass,self._command_topic,"{'device':'"+self._name+"','state':'"+str(self._state)+"'}",0)
        msg = {}
        msg["cmd"] = "set"
        msg["switch"] = self._switch_number
        msg["state"] = 1 if self._state else 0
        mqtt.publish(self.hass,self._command_topic,json.dumps(msg))
        self.update_ha_state()

    def turn_off(self, **kwargs):
        """ Turn the device off. """
        self._state = False
        msg = {}
        msg["cmd"] = "set"
        msg["switch"] = self._switch_number
        msg["state"] = 1 if self._state else 0
        mqtt.publish(self.hass,self._command_topic,json.dumps(msg))
        #mqtt.publish(self._hass,self._command_topic,"{\"cmd\"":"\"set\""++self._name+"','state':'"+str(self._state)+"'}",0)
        self.update_ha_state()
