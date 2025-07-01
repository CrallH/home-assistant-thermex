import aiohttp
import json
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
DEFAULT_BRIGHTNESS = 50

class ThermexAPI:
    def __init__(self, hass, host, code):
        self._hass = hass
        self._host = host
        self._password = code
        self._coordinator = None

    @property
    def coordinator(self):
        return self._coordinator

    async def async_setup_coordinator(self):
        self._coordinator = DataUpdateCoordinator(
            hass=self._hass,
            logger=_LOGGER,
            name="thermex_data",
            update_method=self.async_get_data,
            update_interval=timedelta(seconds=10),
        )
        await self._coordinator.async_refresh()

    async def authenticate(self, websocket):
        auth_message = {
            "Request": "Authenticate",
            "Data": {"Code": self._password}
        }
        _LOGGER.debug("Authentication started")
        _LOGGER.debug("Sending auth message: %s", auth_message)
        await websocket.send_json(auth_message)
        response = await websocket.receive()
        response_data = json.loads(response.data)
        _LOGGER.warning("Authentication response: %s", response_data)
        if response_data.get("Status") == 200:
            _LOGGER.info("Authentication successful")
            return True
        else:
            _LOGGER.error("Authentication failed")
            return False

    async def fetch_status(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f'ws://{self._host}:9999/api') as websocket:
                await self.authenticate(websocket)

                # Kontrollera protokollversion
                await websocket.send_json({"Request": "ProtocolVersion"})
                version_response = await websocket.receive()
                _LOGGER.info("ProtocolVersion response: %s", version_response.data)

                await websocket.send_json({"Request": "STATUS"})
                _LOGGER.debug("Sent STATUS request")
                response = await websocket.receive()
                _LOGGER.debug("Received STATUS response raw: %s", response.data)
                response = json.loads(response.data)
                if response.get("Response") == "Status":
                    return response.get("Data")
                else:
                    _LOGGER.error("Unexpected status response: %s", response)
                    raise Exception("Unexpected STATUS response")

    async def async_get_data(self):
        try:
            return await self.fetch_status()
        except Exception as err:
            _LOGGER.error("Failed to fetch Thermex data: %s", err)
            return {}

    async def update_light(self, lightonoff: int, brightness: int = DEFAULT_BRIGHTNESS):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f'ws://{self._host}:9999/api') as websocket:
                await self.authenticate(websocket)
                await websocket.send_json({
                    "Request": "Update",
                    "Data": {
                        "light": {
                            "lightonoff": lightonoff,
                            "lightbrightness": brightness
                        }
                    }
                })
                await websocket.receive()

    async def update_fan(self, fanonoff: int, fanspeed: int):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f'ws://{self._host}:9999/api') as websocket:
                await self.authenticate(websocket)
                await websocket.send_json({
                    "Request": "Update",
                    "Data": {
                        "fan": {
                            "fanonoff": fanonoff,
                            "fanspeed": fanspeed
                        }
                    }
                })
                await websocket.receive()

    async def update_decolight(self, decolightonoff: int, decolightbrightness: int = DEFAULT_BRIGHTNESS):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f'ws://{self._host}:9999/api') as websocket:
                await self.authenticate(websocket)
                await websocket.send_json({
                    "Request": "Update",
                    "Data": {
                        "decolight": {
                            "decolightonoff": decolightonoff,
                            "decolightbrightness": decolightbrightness
                        }
                    }
                })
                await websocket.receive()
