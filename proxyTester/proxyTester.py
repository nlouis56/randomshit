import requests
import sys
from concurrent.futures import ThreadPoolExecutor

def writeValid(ip, protocol, latency):
    with open("valid.csv", "a") as f:
        f.write(f"{ip};{protocol};{latency}\n")


def latencyTest(ip, protocol):
    try:
        response = requests.get("208.67.222.222", proxies={protocol: ip}, timeout=2)
        if response.status_code == 200:
            return int(response.elapsed.microseconds / 1000)
        else:
            return -1
    except requests.exceptions.RequestException:
        return -2


def http_proxy(ip):
    try:
        response = requests.get("http://www.example.com", proxies={"http": ip}, timeout=2)
        if response.status_code == 200:
            print(f"{ip} is valid using HTTP.")
            writeValid(ip, "HTTP", latencyTest(ip, "http"))
        else:
            return
    except requests.exceptions.RequestException:
        return


def socks4_proxy(ip):
    try:
        response = requests.get("http://www.example.com", proxies={"socks4": ip}, timeout=2)
        if response.status_code == 200:
            print(f"{ip} is valid using SOCKS4.")
            writeValid(ip, "SOCKS4", latencyTest(ip, "socks4"))
        else:
            return
    except requests.exceptions.RequestException:
        return


def socks5_proxy(ip):
    try:
        response = requests.get("http://www.example.com", proxies={"socks5": ip}, timeout=2)
        if response.status_code == 200:
            print(f"{ip} is valid using SOCKS5.")
            writeValid(ip, "SOCKS5", latencyTest(ip, "socks5"))
        else:
            return
    except requests.exceptions.RequestException:
        return


def https_proxy(ip):
    try:
        response = requests.get("https://www.example.com", proxies={"https": ip}, timeout=2)
        if response.status_code == 200:
            print(f"{ip} is valid using HTTPS.")
            writeValid(ip, "HTTPS", latencyTest(ip, "https"))
        else:
            return
    except requests.exceptions.RequestException:
        return


def checkProxy(ip):
    http_proxy(ip)
    socks4_proxy(ip)
    socks5_proxy(ip)
    https_proxy(ip)


def launchWithFile(file):
    ips = []
    threads = []
    try:
        with open(file, "r") as f:
            for line in f:
                ips.append(line.strip())
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    print (f"File successfully parsed, checking {len(ips)} proxies...")
    with ThreadPoolExecutor(max_workers=128) as executor:
        for ip in ips:
            threads.append(executor.submit(checkProxy, ip))
        for thread in threads:
            thread.result()


def usageMessage():
    print("USAGE: python main.py <flag> <args>")
    print("Flags:")
    print("--file <file> - Checks proxies from a file.")
    print("--proxy <proxy> - Checks a single proxy.")
    print("Example: python main.py --file proxies.txt\n")
    print("All valid proxies will be written to valid.txt in the format <ip>;<protocol>;<latency>. The latency is in milliseconds.")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usageMessage()
        sys.exit(1)
    elif len(sys.argv) == 3:
        if (sys.argv[1] == "--file"):
            launchWithFile(sys.argv[2])
        elif (sys.argv[1] == "--proxy"):
            print(f"Checking {sys.argv[2]}...")
            checkProxy(sys.argv[2])
        else:
            usageMessage()
            sys.exit(1)
    else:
        usageMessage()
        sys.exit(1)
