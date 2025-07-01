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
