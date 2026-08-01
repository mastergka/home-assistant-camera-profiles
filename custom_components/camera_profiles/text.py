from homeassistant.components.text import TextEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    entity = CameraProfileName(hass.data[DOMAIN][entry.entry_id])
    async_add_entities([entity])


class CameraProfileName(TextEntity):
    _attr_name = "Neues Kameraprofil"
    _attr_unique_id = "camera_profiles_name"
    _attr_native_min = 1
    _attr_native_max = 64
    _attr_icon = "mdi:form-textbox"

    def __init__(self, manager):
        self.manager = manager
        manager.entities.append(self)

    @property
    def native_value(self):
        return self.manager.name

    async def async_set_value(self, value):
        self.manager.name = value.strip()
        self.async_write_ha_state()

