# proxyTester

A simple proxy tester written in python.

## Usage

```python3.11 proxyTester.py <flag> <args>```

The program uses a thread pool to test the proxies, so it will be faster than testing them one by one. The default workers count is 8, but you can change it by editing the ```threadCount``` variable in the code.

## Flags

| Flag | Description | Arguments |
| ---- | ----------- | --------- |
| --file | Specify a file to read proxies from | File path |
| --proxy | Specify a single proxy to test | Proxy address |

## Examples

```python3.11 proxyTester.py --file proxies.txt```

```python3.11 proxyTester.py --proxy 192.168.1.1:8080```

If the port is not specified, the default port will be 80 (or whatever the default is using python's "requests" module).

## Output

The program will output the ip and the protocol of the proxy if it is working.
The output will be in the following format:

```<ip[:port]>;<protocol>``` inside a file called ```valid.txt```

The program currently supports the following protocols:
- HTTP
- HTTPS
- SOCKS4
- SOCKS5

## Requirements

- Python 3.11
- requests module
- concurrent.futures module

## Installation

```pip3.11 install requests futures```