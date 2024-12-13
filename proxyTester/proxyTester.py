import sys
import requests
import time
from random import shuffle
import http.client
import json
import argparse
import pandas as pd
from alive_progress import alive_bar
from concurrent.futures import ProcessPoolExecutor, as_completed


SILENT = True


class Proxy:
    def __init__(self, ip, address, port, protocol):
        self.ip = ip
        self.address = address
        self.port = port
        self.protocol = protocol
        self.tested = False
        self.anonymous = False
        self.latency = None

    def set_latency(self, latency):
        self.latency = latency

    def set_tested(self):
        self.tested = True

    def csv_repr(self):
        return f"{self.ip},{self.address},{self.protocol},{self.latency},{"Yes" if self.anonymous else "No"}"

    def __str__(self):
        return self.address


def get_args():
    parser = argparse.ArgumentParser(description="Test a list of proxies")
    parser.add_argument("-f", "--file", help="File containing list of proxies")
    parser.add_argument("-t", "--threads", help="Number of threads to use (default is 20)", type=int, default=20)
    parser.add_argument("-T", "--testing", help="Testing mode, no multithreading", default=False, action="store_true")
    return parser.parse_args()


def send_request_through_proxy(proxy_host, proxy_port, target_url):
    # Extract the target host and path from the URL
    from urllib.parse import urlparse
    parsed_url = urlparse(target_url)
    target_host = parsed_url.netloc
    target_path = parsed_url.path or "/"
    if parsed_url.query:
        target_path += f"?{parsed_url.query}"
    conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=10)
    response_json = None
    try:
        if not SILENT:
            print(f"Connecting to proxy {proxy_host}:{proxy_port}")
        conn.request("GET", f"{target_url}")  # Use full URL for proxy GET
        response = conn.getresponse()
        if not SILENT:
            print(f"Proxy response status: {response.status}")
        if response.status != 200:
            if not SILENT:
                print(f"Failed to connect to proxy. Response: {response.status} {response.reason}")
            return None
        response_data = response.read()
        response_json = json.loads(response_data)
    except Exception as e:
        if not SILENT:
            print(f"Error using proxy: {e}")
    finally:
        conn.close()
    return response_json


def test_proxy(proxy, origin_ip):
    timeout = 10
    latency = -1
    try:
        time_start = time.time()
        response_json = send_request_through_proxy(proxy.ip, proxy.port, "http://httpbin.org/ip")
        if response_json is None:
            proxy.set_latency(-1)
            proxy.set_tested()
            return proxy
    except Exception as e:
        if not SILENT:
            print(f"Error testing proxy: {e}")
        proxy.set_latency(-1)
        proxy.set_tested()
        return proxy
    returned_ip = response_json["origin"]
    if returned_ip == origin_ip:
        if not SILENT:
            print(f"Proxy {proxy} did not return the expected IP address. Expected {proxy.ip}, got {returned_ip}")
        proxy.set_latency(-1)
        proxy.set_tested()
        return proxy
    time_end = time.time()
    latency = time_end - time_start
    proxy.set_latency(latency)
    proxy.set_tested()
    if len(returned_ip.split(",")) > 1:
        proxy.anonymous = False
    else:
        proxy.anonymous = True
    return proxy


def start_processes(proxies, threads, origin_ip):
    with alive_bar(len(proxies)) as bar:
        with ProcessPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(test_proxy, proxy, origin_ip): proxy for proxy in proxies}
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    if not SILENT:
                        print(f"Error processing proxy: {e}")
                bar()
    return results


def export_valid_proxies(proxies):
    with open("valid_proxies.csv", "w") as f:
        f.write("ip,proxy,protocol,latency,anonymous\n")
        for proxy in proxies:
            f.write(proxy.csv_repr() + "\n")


def main():
    args = get_args()
    if not args.file:
        print("Please provide a file containing a list of proxies")
        sys.exit(1)
    print(f"Reading proxies from {args.file}")
    data = pd.read_csv(args.file)
    proxies = [Proxy(row["ip"], row["address"], row["port"], row["protocol"]) for index, row in data.iterrows()]
    origin_ip = requests.get("http://httpbin.org/ip").json()["origin"]
    print(f"Testing {len(proxies)} proxies")
    shuffle(proxies)
    if args.testing:
        results = [test_proxy(proxy, origin_ip) for proxy in proxies]
        SILENT = False
    else:
        SILENT = True
        results = start_processes(proxies, args.threads, origin_ip)
    valid_proxies = [result for result in results if result.latency != -1]
    print(f"{len(valid_proxies)} proxies are valid")
    export_valid_proxies(valid_proxies)


if __name__ == "__main__":
    main()
