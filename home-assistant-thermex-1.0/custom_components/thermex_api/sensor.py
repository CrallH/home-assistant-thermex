import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .api import ThermexAPI

_LOGGER = logging.getLogger(__name__)

FAN_SPEEDS = {
    0: "Av",
    1: "Låg",
    2: "Mellan",
    3: "Hög",
    4: "Boost"
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Thermex fan sensor and diagnostics sensor."""
    api: ThermexAPI = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ThermexFanSensor(api),
        ThermexDiagnosticSensor(api)
    ], True)

class ThermexFanSensor(CoordinatorEntity, SensorEntity):
    """Representation of a fan speed sensor."""

    def __init__(self, api: ThermexAPI):
        """Initialize the sensor."""
        super().__init__(api.coordinator)
        self._api = api
        self._attr_name = "Thermex Fläkthastighet"
        self._attr_unique_id = "thermex_fan_speed"
        self._attr_icon = "mdi:fan"

    @property
    def native_value(self):
        """Return current fan speed label."""
        data = (self.coordinator.data or {}).get("Fan", {})
        return FAN_SPEEDS.get(data.get("fanspeed", 0), "Okänd")

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