import requests
import pandas as pd
import os

def fetch_weather(city: str, latitude: float, longitude: float, start_date: str, end_date:str) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }

    print(f"Fetching weather data for {city}...")
    response = requests.get(url, params=params)

    #Response check
    if response.status_code != 200:
        print(response.json())
        raise Exception(f"API request failed with status {response.status_code}")
    
    #Parse JSON response
    data = response.json()
    daily = data["daily"]

    #convert to DataFrame
    df = pd.DataFrame({
        "date": daily["time"],
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "precipitation": daily["precipitation_sum"]
    })

    df["date"] = pd.to_datetime(df["date"])
    df["city"] = city

    return df

if __name__=="__main__":
    df = fetch_weather(
        city="Milan",
        latitude=45.46,
        longitude=9.19,
        start_date="2020-01-01",
        end_date="2024-12-31"
    )

    #Save raw data
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/milan_weather.csv", index=False)

    print(f" Saved {len(df)} rows to data/raw/milan_weather.csv")
    print(df.head())