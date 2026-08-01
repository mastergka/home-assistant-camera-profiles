from homeassistant.components.button import ButtonEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    manager = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SaveButton(manager), LoadButton(manager), DeleteButton(manager)])


class BaseProfileButton(ButtonEntity):
    _attr_has_entity_name = False

    def __init__(self, manager):
        self.manager = manager


class SaveButton(BaseProfileButton):
    _attr_name = "Kameraprofil speichern"
    _attr_unique_id = "camera_profiles_save"
    _attr_icon = "mdi:content-save"

    async def async_press(self):
        if self.manager.name:
            self.manager.profiles[self.manager.name] = self.manager.visible_cameras()
            self.manager.selected = self.manager.name
            await self.manager.save_data()


class LoadButton(BaseProfileButton):
    _attr_name = "Kameraprofil laden"
    _attr_unique_id = "camera_profiles_load"
    _attr_icon = "mdi:folder-open"

    async def async_press(self):
        if self.manager.selected:
            await self.manager.apply(self.manager.selected)


class DeleteButton(BaseProfileButton):
    _attr_name = "Kameraprofil löschen"
    _attr_unique_id = "camera_profiles_delete"
    _attr_icon = "mdi:delete"

    async def async_press(self):
        if self.manager.selected:
            self.manager.profiles.pop(self.manager.selected, None)
            self.manager.selected = ""
            await self.manager.save_data()

