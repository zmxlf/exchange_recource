import os
from dotenv import load_dotenv
import requests


load_dotenv()

key=os.getenv("RATES_API_KEY")


def get_rates():
    url = f"https://v6.exchangerate-api.com/v6/{key}/latest/RUB"
    response = requests.get(url, timeout=10)
    if response.status_code==200:
        data=response.json()
        conversion_rates=data["conversion_rates"]
        return {
            "RUB": 1.0,
            "USD" : round(1/conversion_rates["USD"],6),
            "EUR" : round(1/conversion_rates["EUR"],6),
            "CNY" : round(1/conversion_rates["CNY"],6)
        }
    else:
        print("ERROR",response.status_code)
        return None

if __name__ == "__main__":
    print(get_rates())