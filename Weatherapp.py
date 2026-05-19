import tkinter as tk
from tkinter import ttk, font
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# ── Configuration ────────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
UNITS   = "imperial"   # "imperial" → °F  |  "metric" → °C
UNIT_LABEL = "°F" if UNITS == "imperial" else "°C"

WEATHER_ICONS = {
    "clear sky":          "☀️",
    "few clouds":         "🌤️",
    "scattered clouds":   "⛅",
    "broken clouds":      "☁️",
    "overcast clouds":    "☁️",
    "shower rain":        "🌦️",
    "rain":               "🌧️",
    "light rain":         "🌧️",
    "moderate rain":      "🌧️",
    "heavy intensity rain":"🌧️",
    "thunderstorm":       "⛈️",
    "snow":               "❄️",
    "light snow":         "❄️",
    "mist":               "🌫️",
    "fog":                "🌫️",
    "haze":               "🌫️",
    "smoke":              "🌫️",
    "dust":               "🌫️",
    "sand":               "🌫️",
    "drizzle":            "🌦️",
}

THEMES = {
    "Sky Blue":   {"bg": "#1a6fa3", "panel": "#1258844", "accent": "#4fc3f7", "text": "#e8f4fd", "btn": "#0288d1"},
    "Sunset":     {"bg": "#b34700", "panel": "#8c3600", "accent": "#ffcc80", "text": "#fff3e0", "btn": "#e65100"},
    "Forest":     {"bg": "#1b5e20", "panel": "#154a19", "accent": "#a5d6a7", "text": "#e8f5e9", "btn": "#2e7d32"},
    "Midnight":   {"bg": "#0d0d2b", "panel": "#12122f", "accent": "#7986cb", "text": "#e8eaf6", "btn": "#3949ab"},
    "Rose":       {"bg": "#880e4f", "panel": "#6a0b3d", "accent": "#f48fb1", "text": "#fce4ec", "btn": "#c2185b"},
    "Slate":      {"bg": "#263238", "panel": "#1c252a", "accent": "#90a4ae", "text": "#eceff1", "btn": "#37474f"},
}


# ── Helper ────────────────────────────────────────────────────────────────────
def get_icon(description: str) -> str:
    desc = description.lower()
    return WEATHER_ICONS.get(desc, "🌡️")


def wind_direction(degrees: float) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(degrees / 45) % 8]


# ── Main App ──────────────────────────────────────────────────────────────────
class WeatherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SkyScript — Weather Dashboard")
        self.root.resizable(True, True)
        self.root.state("zoomed")  # launch maximized; remove this line if you prefer a normal start
        self.current_theme = "Midnight"

        self._build_fonts()
        self._build_ui()
        self._apply_theme(self.current_theme)

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.font_title   = font.Font(family="Helvetica", size=18, weight="bold")
        self.font_temp    = font.Font(family="Helvetica", size=42, weight="bold")
        self.font_desc    = font.Font(family="Helvetica", size=13)
        self.font_detail  = font.Font(family="Helvetica", size=11)
        self.font_label   = font.Font(family="Helvetica", size=10)
        self.font_day     = font.Font(family="Helvetica", size=10, weight="bold")

    # ── UI Layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header bar ────────────────────────────────────────────────────────
        self.header = tk.Frame(self.root, pady=12, padx=16)
        self.header.pack(fill="x")

        tk.Label(self.header, text="SkyScript", font=self.font_title).pack(side="left")

        # Theme selector
        theme_frame = tk.Frame(self.header)
        theme_frame.pack(side="right")

        # Maximize / Restore toggle button
        self.btn_maximize = tk.Button(
            self.header, text="⛶  Maximize", font=self.font_label,
            bd=0, relief="flat", padx=10, pady=4, cursor="hand2",
            command=self._toggle_maximize
        )
        self.btn_maximize.pack(side="right", padx=(0, 12))
        tk.Label(theme_frame, text="Theme:", font=self.font_label).pack(side="left", padx=(0, 4))
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_cb = ttk.Combobox(
            theme_frame, textvariable=self.theme_var,
            values=list(THEMES.keys()), state="readonly", width=10
        )
        theme_cb.pack(side="left")
        theme_cb.bind("<<ComboboxSelected>>", lambda e: self._apply_theme(self.theme_var.get()))

        # ── Search bar ────────────────────────────────────────────────────────
        self.search_frame = tk.Frame(self.root, pady=8, padx=16)
        self.search_frame.pack(fill="x")

        self.entry_city = tk.Entry(self.search_frame, font=self.font_desc, width=22, bd=0, relief="flat")
        self.entry_city.pack(side="left", ipady=6, padx=(0, 8))
        self.entry_city.insert(0, "Enter city…")
        self.entry_city.bind("<FocusIn>",  self._clear_placeholder)
        self.entry_city.bind("<FocusOut>", self._restore_placeholder)
        self.entry_city.bind("<Return>",   lambda e: self._fetch_weather())

        self.btn_search = tk.Button(
            self.search_frame, text="Search", font=self.font_label,
            bd=0, relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._fetch_weather
        )
        self.btn_search.pack(side="left")

        # ── Main weather panel ────────────────────────────────────────────────
        self.main_panel = tk.Frame(self.root, padx=20, pady=10)
        self.main_panel.pack(fill="both")

        self.lbl_icon  = tk.Label(self.main_panel, text="", font=font.Font(size=52))
        self.lbl_icon.pack()

        self.lbl_temp  = tk.Label(self.main_panel, text="--", font=self.font_temp)
        self.lbl_temp.pack()

        self.lbl_desc  = tk.Label(self.main_panel, text="No city loaded", font=self.font_desc)
        self.lbl_desc.pack()

        self.lbl_city  = tk.Label(self.main_panel, text="", font=self.font_label)
        self.lbl_city.pack(pady=(0, 10))

        # Detail row
        self.detail_frame = tk.Frame(self.main_panel)
        self.detail_frame.pack(fill="x", pady=(0, 10))

        self.lbl_humidity = self._detail_box(self.detail_frame, "Humidity", "--")
        self.lbl_wind     = self._detail_box(self.detail_frame, "Wind", "--")
        self.lbl_feels    = self._detail_box(self.detail_frame, "Feels Like", "--")
        self.lbl_pressure = self._detail_box(self.detail_frame, "Pressure", "--")

        # ── 5-day forecast strip ───────────────────────────────────────────────
        self.forecast_label = tk.Label(
            self.root, text="5-Day Forecast", font=self.font_day, anchor="w", padx=20
        )
        self.forecast_label.pack(fill="x")

        self.forecast_frame = tk.Frame(self.root, padx=16, pady=8)
        self.forecast_frame.pack(fill="x")
        self.forecast_cards = []
        for _ in range(5):
            card = self._forecast_card(self.forecast_frame)
            self.forecast_cards.append(card)

        # ── Status bar ────────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready — enter a city and press Search.")
        self.status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            font=self.font_label, anchor="w", padx=16, pady=6
        )
        self.status_bar.pack(fill="x")

    def _detail_box(self, parent, label_text, initial):
        box = tk.Frame(parent, padx=10, pady=6)
        box.pack(side="left", expand=True, fill="x")
        tk.Label(box, text=label_text, font=self.font_label).pack()
        val_lbl = tk.Label(box, text=initial, font=self.font_day)
        val_lbl.pack()
        return val_lbl

    def _forecast_card(self, parent):
        card = tk.Frame(parent, padx=8, pady=8, relief="flat", bd=0)
        card.pack(side="left", expand=True, fill="both")
        day_lbl  = tk.Label(card, text="---", font=self.font_day)
        day_lbl.pack()
        icon_lbl = tk.Label(card, text="", font=font.Font(size=18))
        icon_lbl.pack()
        hi_lbl   = tk.Label(card, text="--", font=self.font_label)
        hi_lbl.pack()
        lo_lbl   = tk.Label(card, text="--", font=self.font_label)
        lo_lbl.pack()
        return {"frame": card, "day": day_lbl, "icon": icon_lbl, "hi": hi_lbl, "lo": lo_lbl}

    # ── Theming ───────────────────────────────────────────────────────────────
    def _apply_theme(self, name: str):
        self.current_theme = name
        t = THEMES[name]
        bg, panel, accent, text, btn = t["bg"], t["panel"], t["accent"], t["text"], t["btn"]

        self.root.configure(bg=bg)
        for widget in [self.header, self.search_frame, self.main_panel,
                       self.detail_frame, self.forecast_frame, self.forecast_label,
                       self.status_bar]:
            widget.configure(bg=bg)

        for w in self.root.winfo_children():
            self._recolor(w, bg, text, accent, btn)

        # Entry special styling
        self.entry_city.configure(bg=panel if panel != "#1258844" else "#12588f",
                                  fg=text, insertbackground=text,
                                  highlightbackground=accent, highlightcolor=accent,
                                  highlightthickness=1)

        self.btn_search.configure(bg=btn, fg=text, activebackground=accent, activeforeground=bg)

        # Forecast cards
        for card in self.forecast_cards:
            card["frame"].configure(bg=panel if panel != "#1258844" else "#12588f")
            for key in ("day", "icon", "hi", "lo"):
                card[key].configure(bg=panel if panel != "#1258844" else "#12588f",
                                    fg=text if key != "hi" else accent)

    def _recolor(self, widget, bg, text, accent, btn):
        cls = widget.__class__.__name__
        try:
            if cls == "Label":
                widget.configure(bg=bg, fg=text)
            elif cls == "Frame":
                widget.configure(bg=bg)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._recolor(child, bg, text, accent, btn)

    # ── Window maximize toggle ────────────────────────────────────────────────
    def _toggle_maximize(self):
        if self.root.state() == "zoomed":
            self.root.state("normal")
            self.btn_maximize.configure(text="⛶  Maximize")
        else:
            self.root.state("zoomed")
            self.btn_maximize.configure(text="❐  Restore")

    # ── Placeholder helpers ───────────────────────────────────────────────────
    def _clear_placeholder(self, _event):
        if self.entry_city.get() == "Enter city…":
            self.entry_city.delete(0, "end")

    def _restore_placeholder(self, _event):
        if not self.entry_city.get().strip():
            self.entry_city.insert(0, "Enter city…")

    # ── Weather fetching ──────────────────────────────────────────────────────
    def _fetch_weather(self):
        city = self.entry_city.get().strip()
        if not city or city == "Enter city…":
            self._set_status("⚠️  Please enter a city name first.")
            return

        if not API_KEY:
            self._set_status("⚠️  No API key set — edit API_KEY at the top of the script.")
            return

        self._set_status(f"Fetching weather for {city}…")
        self.root.update_idletasks()

        try:
            # Current weather
            current_url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={API_KEY}&units={UNITS}"
            )
            curr_resp = requests.get(current_url, timeout=8)
            curr_data = curr_resp.json()

            if curr_data.get("cod") != 200:
                msg = curr_data.get("message", "City not found.")
                self._set_status(f"❌  Error: {msg.capitalize()}")
                return

            self._update_current(curr_data)

            # 5-day forecast (every 3 hrs → pick one reading per day at noon)
            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={city}&appid={API_KEY}&units={UNITS}"
            )
            fore_resp = requests.get(forecast_url, timeout=8)
            fore_data = fore_resp.json()

            if fore_data.get("cod") == "200" or fore_data.get("cod") == 200:
                self._update_forecast(fore_data)

            self._set_status(
                f"✅  Updated {datetime.now().strftime('%H:%M:%S')} — "
                f"{curr_data['name']}, {curr_data['sys']['country']}"
            )

        except requests.exceptions.ConnectionError:
            self._set_status("❌  No internet connection.")
        except requests.exceptions.Timeout:
            self._set_status("❌  Request timed out. Try again.")
        except Exception as exc:
            self._set_status(f"❌  Unexpected error: {exc}")

    def _update_current(self, data: dict):
        desc  = data["weather"][0]["description"]
        temp  = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        hum   = data["main"]["humidity"]
        wind_spd = data["wind"]["speed"]
        wind_dir = wind_direction(data["wind"].get("deg", 0))
        pressure = data["main"]["pressure"]
        city_str = f"{data['name']}, {data['sys']['country']}"
        speed_unit = "mph" if UNITS == "imperial" else "m/s"

        self.lbl_icon.configure(text=get_icon(desc))
        self.lbl_temp.configure(text=f"{temp:.0f}{UNIT_LABEL}")
        self.lbl_desc.configure(text=desc.title())
        self.lbl_city.configure(text=city_str)
        self.lbl_humidity.configure(text=f"{hum}%")
        self.lbl_wind.configure(text=f"{wind_spd:.1f} {speed_unit} {wind_dir}")
        self.lbl_feels.configure(text=f"{feels:.0f}{UNIT_LABEL}")
        self.lbl_pressure.configure(text=f"{pressure} hPa")

    def _update_forecast(self, data: dict):
        # Group entries by date, pick the one closest to 12:00
        days: dict[str, list] = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            days.setdefault(date, []).append(entry)

        # Skip today (first key), take up to 5 future days
        future_days = list(days.items())[1:6]

        for i, card in enumerate(self.forecast_cards):
            if i >= len(future_days):
                card["day"].configure(text="---")
                card["icon"].configure(text="")
                card["hi"].configure(text="--")
                card["lo"].configure(text="--")
                continue

            date_str, entries = future_days[i]
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt.strftime("%a %d")

            # Representative entry (closest to noon)
            noon_entry = min(entries, key=lambda e: abs(
                int(e["dt_txt"].split(" ")[1][:2]) - 12
            ))
            desc = noon_entry["weather"][0]["description"]
            hi   = max(e["main"]["temp_max"] for e in entries)
            lo   = min(e["main"]["temp_min"] for e in entries)

            card["day"].configure(text=day_name)
            card["icon"].configure(text=get_icon(desc))
            card["hi"].configure(text=f"↑{hi:.0f}{UNIT_LABEL}")
            card["lo"].configure(text=f"↓{lo:.0f}{UNIT_LABEL}")

    def _set_status(self, msg: str):
        self.status_var.set(msg)
        self.root.update_idletasks()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(520, 480)
    app = WeatherApp(root)
    root.mainloop()