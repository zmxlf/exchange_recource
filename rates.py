import os
from dotenv import load_dotenv
import requests
import json
from datetime import date

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
cash_file = os.path.join(base_dir, "cash_rates.json")

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

    
def rates_in_cash():
    a = get_rates()
    if a is None:
        print("Не удалось обновить кэш из-за ошибки API")
        return None

    
    a["date"] = str(date.today())
    
    with open(cash_file,'w',encoding="utf-8") as f:
        json.dump(a,f)
        


def get_from_cash():
    with open(cash_file,'r',encoding="utf-8") as f:
        a = json.load(f)
    if str(date.today()) == a.get("date"):
        return {
                "RUB": 1.0,
                "USD" : a.get("USD"),
                "EUR" : a.get("EUR"),
                "CNY" : a.get("CNY")    
        }
    else:
        rates_in_cash()
        return get_from_cash()


    
if __name__ == "__main__":
    rates = get_from_cash()
    print(rates)