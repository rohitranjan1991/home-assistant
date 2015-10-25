"""
components.switch.demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RaspAsSwitch platform
"""
from homeassistant.components.switch import SwitchDevice
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.components import mqtt


DEPENDENCIES = ['mqtt']

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return demo switches. """
    switches = config.get('switches', {})
    devices = []


    for dev_name, properties in switches.items():
        devices.append(
            RaspAsSwitch(
                hass,
                properties.get('switch_id', dev_name),
                properties.get('switch_name', 'rasp_switch'),
                properties.get('switch_state', 'false'),
                properties.get('command_topic', ''),
                properties.get('state_topic', '')
            )
        )
        add_devices_callback(devices)


class RaspAsSwitch(SwitchDevice):

    """ Provides a demo switch. """
    def __init__(self, hass, id, name, state,command_topic,state_topic):
        self._hass = hass
        self._name = name or DEVICE_DEFAULT_NAME
        self._id = id
        self._state = False
        self._command_topic = command_topic
        self._state_topic = state_topic


    @property
    def should_poll(self):
        """ No polling needed for a demo switch. """
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
        mqtt.publish(self._hass,self._command_topic,"{'device':'"+self._name+"','state':'"+str(self._state)+"'}",0)
        self.update_ha_state()

    def turn_off(self, **kwargs):
        """ Turn the device off. """
        self._state = False
        mqtt.publish(self._hass,self._command_topic,"{'device':'"+self._name+"','state':'"+str(self._state)+"'}",0)
        self.update_ha_state()
