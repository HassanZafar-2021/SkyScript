# SkyScript 🌤️

## Description

SkyScript is a desktop weather application built in Python that delivers real-time weather data and 5-day forecasts for any city in the world — all inside a clean, themeable GUI.

- **Motivation:** Weather apps online are cluttered with ads and noise. I wanted something minimal, fast, and local — an app that just tells you what you need to know.
- **Why I built it:** To push beyond terminal-based Python and explore how to build real graphical applications that interact with live external APIs.
- **What problem does it solve?** It gives users an instant, distraction-free snapshot of current conditions and the week ahead — humidity, wind, feels-like temperature, pressure, and a 5-day forecast — all from one window.
- **What I learned:** How to structure a tkinter OOP application, consume and parse REST API responses, handle errors gracefully, manage environment variables securely with `.env`, and design a dynamic theming system entirely in Python.

---

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)
- [Badges](#badges)
- [Features](#features)
- [How to Contribute](#how-to-contribute)
- [Tests](#tests)

---

## Installation

**Prerequisites:** Python 3.8 or higher

**1. Clone the repository**
```bash
git clone https://github.com/your-username/SkyScript.git
cd SkyScript
```

**2. Install dependencies**
```bash
pip install requests python-dotenv
```

**3. Get a free API key**

Sign up at [openweathermap.org](https://openweathermap.org/api) and copy your API key from the **API keys** tab. Note: new keys can take up to 2 hours to activate.

**4. Create your `.env` file**

In the root project folder, create a file named `.env` and add:
```
OPENWEATHER_API_KEY=your_actual_key_here
```

**5. Run the app**
```bash
python WeatherApp.py
```

---

## Usage

1. Launch the app — it opens maximized by default.
2. Type any city name into the search bar and press **Enter** or click **Search**.
3. Current conditions load instantly: temperature, description, humidity, wind speed & direction, feels-like, and pressure.
4. The **5-Day Forecast** strip updates below with daily high/low and weather icons.
5. Use the **Theme** dropdown in the top-right to switch between 6 color themes.
6. Use the **Maximize / Restore** button to toggle window size at any time.

```md
![SkyScript Screenshot](assets/images/screenshot.png)
```

---

## Credits

**Developer:** Hassan — [GitHub](https://github.com/HassanZafar-2021)

---

## License

No license

---

## Badges

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat)
![OpenWeatherMap](https://img.shields.io/badge/API-OpenWeatherMap-orange?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

---

## Features

- 🌡️ **Real-time weather** — temperature, description, humidity, wind, feels-like, and pressure
- 📅 **5-Day forecast** — daily high/low with weather emoji icons
- 🎨 **6 color themes** — Sky Blue, Sunset, Forest, Midnight, Rose, Slate
- ⛶ **Maximize / Restore toggle** — built into the app header
- ⌨️ **Keyboard support** — press Enter to search, no mouse required
- 🔒 **Secure API key handling** — loaded from `.env`, never hardcoded
- ⚠️ **Graceful error handling** — network failures, timeouts, and bad city names all surface a clear message in the status bar

---

## How to Contribute

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

---

## Tests

Currently there is no automated test suite. To manually verify the app is working:

**Happy path**
```bash
python WeatherApp.py
# Enter "New York" → expect current weather and 5-day forecast to load
```

**Error handling**
- Enter a fake city name (e.g. `xyzabc`) → expect `❌ Error: city not found`
- Remove your API key from `.env` → expect `⚠️ No API key set` message
- Disconnect from the internet and search → expect `❌ No internet connection`