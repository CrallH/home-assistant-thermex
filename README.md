# Thermex API Integration for Home Assistant

![Thermex Logo](./icon.png)

Custom integration to control Thermex fans and lights over WebSocket API.

---

## 🔧 Features

- Control **Fan**: on/off and speed (0–4)
- Control **Light**: on/off and brightness (0–100)
- Control **Decolight**: on/off and brightness (0–100)
- UI-based setup (via config flow)
- Sensor showing fan speed
- Diagnostic status sensor
- Custom icon
- English and Swedish translation support
- Built-in services
- Includes ready-made **Blueprint**

---


## 🧩 HACS Installation

You can install this integration via [HACS](https://hacs.xyz/):

1. Go to **HACS → Integrations → ⋮ → Custom Repositories**
2. Add repository: `https://github.com/CrallH/home-assistant-thermex`
3. Set category to **Integration**
4. Click **Install** and restart Home Assistant

Then search for "Thermex" and configure as normal.

Or

## 📦 Installation

1. Download and extract this into `config/custom_components/thermex_api/`
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration**
4. Search for **Thermex**
5. Provide the **IP address** and **password** for your Thermex fan

---

## ⚙️ Services

This integration registers the following:

### `thermex_api.update_fan`

```yaml
fanonoff: 1    # 1 = on, 0 = off
fanspeed: 2    # 0–4
```

### `thermex_api.update_light`

```yaml
lightonoff: 1     # 1 = on, 0 = off
brightness: 80    # 0–100
```

### `thermex_api.update_decolight`

```yaml
decolightonoff: 1
decolightbrightness: 100
```

These services support UI sliders via `services.yaml`.

---

## 🧩 Included Blueprint

Path: `blueprints/automation/thermex_api/control_fan_light.yaml`

This blueprint lets you schedule or automate fan/light settings using the built-in automation editor.

---

## 🧪 Diagnostics

- `sensor.thermex_anslutningsstatus` shows connection status
- You can download diagnostics from the integration's settings panel

---

## 🧠 Acknowledgements

Based on [@hsk-dk](https://github.com/hsk-dk/home-assistant-thermex)

This version was rebuilt using [ChatGPT](https://openai.com/chatgpt) and extended for modern Home Assistant versions.

---

## 👤 Developer

Developed and maintained by [@CrallH](https://github.com/CrallH)

---

## 📄 License

MIT
