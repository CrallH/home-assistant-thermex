import logging
from homeassistant.components.light import (
    LightEntity,
    ColorMode,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .api import ThermexAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Thermex light from a config entry."""
    api: ThermexAPI = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ThermexLight(api)], True)

class ThermexLight(CoordinatorEntity, LightEntity):
    """Representation of Thermex light."""

    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_color_mode = ColorMode.BRIGHTNESS

    def __init__(self, api: ThermexAPI):
        """Initialize the light."""
        super().__init__(api.coordinator)
        self._api = api
        self._attr_name = "Thermex Belysning"
        self._attr_unique_id = "thermex_light"

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        light_data = (self.coordinator.data or {}).get("Light", {})
        return light_data.get("lightonoff") == 1

    @property
    def brightness(self) -> int | None:
        """Return brightness level (0-255)."""
        light_data = (self.coordinator.data or {}).get("Light", {})
        value = light_data.get("lightbrightness")
        return int(value * 2.55) if value is not None else None

    async def async_turn_on(self, **kwargs):
        """Turn on light with optional brightness."""
        brightness = kwargs.get("brightness")
        value = int(brightness / 2.55) if brightness is not None else 100
        await self._api.update_light(lightonoff=1, brightness=value)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        await self._api.update_light(lightonoff=0)
        await self.coordinator.async_request_refresh()