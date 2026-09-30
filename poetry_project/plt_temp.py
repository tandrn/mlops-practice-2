import requests
import matplotlib.pyplot as plt
import pandas as pd


URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {"latitude": 55.75, "longitude": 37.61, "hourly": "temperature_2m"}
TIMEOUT = 10


def fetch_weather(url, params, timeout):
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def build_dataframe(hours, temps):
    df = pd.DataFrame({"time": pd.to_datetime(hours), "temperature_c": temps})
    df = df.sort_values("time").reset_index(drop=True)
    return df


def main():
    data = fetch_weather(URL, PARAMS, TIMEOUT)
    hours = data["hourly"]["time"][:24]
    temps = data["hourly"]["temperature_2m"][:24]

    df = build_dataframe(hours, temps)
    df.to_csv("temperature_24h.csv", index=False)
    print("Сохранено в temperature_24h.csv")

    plt.plot(df["time"], df["temperature_c"], marker="o")
    plt.xticks(rotation=45)
    plt.title("Температура в Москве (24 часа)")
    plt.xlabel("Время")
    plt.ylabel("°C")
    plt.tight_layout()
    plt.savefig("temperature_24h.png")
    plt.show()


if __name__ == "__main__":
    main()