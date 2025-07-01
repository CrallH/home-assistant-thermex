import logging
from homeassistant.components.switch import SwitchEntity
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
    """Set up Thermex fan switch from config entry."""
    api: ThermexAPI = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ThermexFanSwitch(api)], True)

class ThermexFanSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of Thermex fan switch."""

    def __init__(self, api: ThermexAPI):
        """Initialize the switch."""
        super().__init__(api.coordinator)
        self._api = api
        self._attr_name = "Thermex Fläktströmställare"
        self._attr_unique_id = "thermex_fan_switch"

    @property
    def is_on(self) -> bool:
        """Return true if the fan is on."""
        fan_data = (self.coordinator.data or {}).get("Fan", {})
        return fan_data.get("fanonoff") == 1

    async def async_turn_on(self, **kwargs):
        """Turn the fan on."""
        await self._api.update_fan(fanonoff=1, fanspeed=2)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        await self._api.update_fan(fanonoff=0, fanspeed=2)
        await self.coordinator.async_request_refresh()