"""Diagnostics support for Thermex integration."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .api import ThermexAPI

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    api: ThermexAPI = hass.data[DOMAIN][entry.entry_id]

    try:
        data = await api.async_get_data()
    except Exception as err:
        data = {"error": str(err)}

    return {
        "host": entry.data.get("host"),
        "fan_data": data.get("Fan", {}),
        "light_data": data.get("Light", {}),
    }

import logging
from homeassistant.components.sensor import SensorEntity
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
    """Set up Thermex diagnostics sensor."""
    api: ThermexAPI = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ThermexDiagnosticSensor(api)], True)

class ThermexDiagnosticSensor(CoordinatorEntity, SensorEntity):
    """Sensor to show last update status."""

    def __init__(self, api: ThermexAPI):
        super().__init__(api.coordinator)
        self._attr_name = "Thermex Anslutningsstatus"
        self._attr_unique_id = "thermex_diagnostics"
        self._attr_icon = "mdi:lan-connect"

    @property
    def native_value(self) -> str:
        return "Online" if self.coordinator.last_update_success else "Fel"
