import requests
import re
import sys

def crawler(url, counter):
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        sys.exit("Something went wrong, check URL")

    for a in response.text.split("\n"):
        print(url)
        search = re.search(r'<a href="([^"]*)"', a)
        if search and not search.groups()[0] in ["../", "README"]:
            counter += 1
            crawler(url + search.groups()[0], counter)
        elif search and search.groups()[0] == "README":
            response = requests.get(url + "README")
            if response.text not in collector:
                collector.append(response.text)

    return collector

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 crawler.py <URL>")
    else:
        url = f"{sys.argv[1]}/.hidden/"
        collector = list()
        collector = crawler(url, 0)
        for e in collector:
            print("README ->", e)
