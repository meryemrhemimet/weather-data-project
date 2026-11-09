
import requests

def fetch_data():
    print("Fetching hourly weather data for Rabat...")

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 34.025,
        "longitude": -6.836,
        "hourly": "temperature_2m,weather_code,wind_speed_10m",
        "forecast_hours": 24,
        "timezone": "Africa/Casablanca"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()

        if data.get("error"):
            raise RuntimeError(data.get("reason", "Open-Meteo API error"))

        print("Hourly weather data fetched successfully.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise
