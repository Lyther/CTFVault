import requests
from requests.auth import HTTPDigestAuth


def main() -> None:
    r = requests.get(
        "https://digest.web.cpctf.space/",
        auth=HTTPDigestAuth("cpctf", "37512859"),
        timeout=20,
    )
    print(r.text)


if __name__ == "__main__":
    main()
