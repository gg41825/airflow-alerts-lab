import re
import os
import json
import requests
import config as config
from datetime import date

def get_eur_twd_rate(**kwargs):
    today = date.today()
    file_path = f"/data/currency_rate_raw_{today}.txt"
    raw_text = ""
    if os.path.exists(file_path): # for testing, you can comment this part and call the url directly
       raw_text = open(file_path, "r", encoding="utf-8").read()
    else:
      url = config.config["currency"]["currency.rate.url"]
      raw_text = requests.get(url).text
      open(file_path, "w", encoding="utf-8").write(raw_text)
      print(f"saved currency rate to {file_path}.txt")

    json_text = re.search(r'genREMITResult\((\[.*\])\);', raw_text, re.DOTALL).group(1)
    data = json.loads(json_text)

    eur_data = next((item for item in data[0]["SubInfo"] if item["DataValue4"] == "EUR"), None)
    code = eur_data["DataValue4"]
    buy_rate = eur_data["DataValue2"]
    sell_rate = eur_data["DataValue3"]
    obj = {
        "code": code,
        "buy_rate": buy_rate,
        "sell_rate": sell_rate
    }
    kwargs["ti"].xcom_push(key="rate_info", value=obj)
    return "Fetched EUR/TWD rate successfully"