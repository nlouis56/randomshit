import requests
import json
import pandas as pd

def make_df(proxies):
    proxy_rows = []
    for proxy in proxies:
        ip = proxy["ip"]
        port = proxy["port"]
        protocol = proxy["protocols"][0]
        address = f"{protocol}://{ip}:{port}"
        new_row = {"IP": ip, "address": address, "port": port, "protocol": protocol}
        proxy_rows.append(new_row)
    proxy_dataframe = pd.DataFrame(proxy_rows)
    return proxy_dataframe

def grab_json(url):
    return requests.get(url).json()

def main():
    pages_amount = 10
    biglist = pd.DataFrame()
    for i in range(1, pages_amount + 1):
        url = f"https://proxylist.geonode.com/api/proxy-list?limit=500&page={i}&sort_by=lastChecked&sort_type=desc"
        json_data = grab_json(url)
        proxies = json_data["data"]
        df = make_df(proxies)
        biglist = pd.concat([biglist, df], ignore_index=True)
    biglist.drop_duplicates(subset=["address"], inplace=True)
    biglist.to_csv("proxies.csv", index=False)

if __name__ == "__main__":
    main()
