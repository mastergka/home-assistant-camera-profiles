from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN
from .manager import CameraProfileManager

PLATFORMS = ["select", "text", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    manager = CameraProfileManager(hass)
    await manager.load()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = manager

    async def save_profile(call: ServiceCall) -> None:
        name = call.data["name"].strip()
        manager.profiles[name] = manager.visible_cameras()
        manager.selected = name
        await manager.save_data()

    async def load_profile(call: ServiceCall) -> None:
        await manager.apply(call.data["name"])

    async def delete_profile(call: ServiceCall) -> None:
        name = call.data["name"]
        manager.profiles.pop(name, None)
        if manager.selected == name:
            manager.selected = ""
        await manager.save_data()

    schema = vol.Schema({vol.Required("name"): cv.string})
    hass.services.async_register(DOMAIN, "save", save_profile, schema=schema)
    hass.services.async_register(DOMAIN, "load", load_profile, schema=schema)
    hass.services.async_register(DOMAIN, "delete", delete_profile, schema=schema)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return ok

