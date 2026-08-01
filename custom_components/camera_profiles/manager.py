from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORE_KEY, STORE_VERSION


class CameraProfileManager:
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.store = Store(hass, STORE_VERSION, STORE_KEY)
        self.profiles: dict[str, list[str]] = {}
        self.selected = ""
        self.name = ""
        self.entities = []

    async def load(self) -> None:
        data = await self.store.async_load() or {}
        self.profiles = data.get("profiles", {})
        self.selected = data.get("selected", "")

    async def save_data(self) -> None:
        await self.store.async_save({"profiles": self.profiles, "selected": self.selected})
        self.update_entities()

    def update_entities(self) -> None:
        for entity in self.entities:
            entity.async_write_ha_state()

    def visible_cameras(self) -> list[str]:
        result = []
        prefix = "input_boolean.kamera_anzeigen_"
        for state in self.hass.states.async_all("input_boolean"):
            if state.entity_id.startswith(prefix) and state.state == "on":
                result.append("camera." + state.entity_id[len(prefix):])
        return sorted(result)

    async def apply(self, name: str) -> None:
        wanted = set(self.profiles.get(name, []))
        prefix = "input_boolean.kamera_anzeigen_"
        for state in self.hass.states.async_all("input_boolean"):
            if not state.entity_id.startswith(prefix):
                continue
            camera = "camera." + state.entity_id[len(prefix):]
            service = "turn_on" if camera in wanted else "turn_off"
            await self.hass.services.async_call("input_boolean", service, {"entity_id": state.entity_id}, blocking=True)
        self.selected = name
        await self.save_data()

