from homeassistant.components.select import SelectEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    entity = CameraProfileSelect(hass.data[DOMAIN][entry.entry_id])
    async_add_entities([entity])


class CameraProfileSelect(SelectEntity):
    _attr_name = "Kameraprofil"
    _attr_unique_id = "camera_profiles_selected"
    _attr_icon = "mdi:camera-account"

    def __init__(self, manager):
        self.manager = manager
        manager.entities.append(self)

    @property
    def options(self):
        return sorted(self.manager.profiles)

    @property
    def current_option(self):
        return self.manager.selected or None

    async def async_select_option(self, option):
        await self.manager.apply(option)

