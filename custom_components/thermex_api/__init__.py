from .const import DOMAIN
from .api import ThermexAPI

PLATFORMS = ["sensor", "light", "switch"]

async def async_setup_entry(hass, entry):
    host = entry.data["host"]
    password = entry.data["password"]
    api = ThermexAPI(hass, host, password)
    await api.async_setup_coordinator()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = api
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_update_fan(call):
        api = hass.data[DOMAIN][entry.entry_id]
        fanonoff = call.data.get("fanonoff", 1)
        fanspeed = call.data.get("fanspeed", 1)
        await api.update_fan(fanonoff, fanspeed)

    async def handle_update_light(call):
        api = hass.data[DOMAIN][entry.entry_id]
        lightonoff = call.data.get("lightonoff", 1)
        brightness = call.data.get("brightness", 50)
        await api.update_light(lightonoff, brightness)

    async def handle_update_decolight(call):
        api = hass.data[DOMAIN][entry.entry_id]
        decolightonoff = call.data.get("decolightonoff", 1)
        decolightbrightness = call.data.get("decolightbrightness", 50)
        await api.update_decolight(decolightonoff, decolightbrightness)

    hass.services.async_register(DOMAIN, "update_fan", handle_update_fan)
    hass.services.async_register(DOMAIN, "update_light", handle_update_light)
    hass.services.async_register(DOMAIN, "update_decolight", handle_update_decolight)

    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
