"""Check generated pages, local links, and URLs retained from the old website."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import json


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1_count = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


root = Path("site").resolve()
pages = {path: Page(path) for path in root.rglob("*.html")}
errors = []
expected = [
    "index.html", "about/index.html", "research/index.html",
    "publications/index.html", "photography/index.html", "reading/index.html",
    "contact/index.html", "license/index.html", "404.html",
    "assets/saeed_MScThesis_2012.pdf", "public/favicon.ico",
    "CNAME", "robots.txt", "atom.xml", "sitemap.xml", "search.json",
]
for route in expected:
    if not (root / route).is_file():
        errors.append(f"Missing existing route or build asset: {route}")

for path, page in pages.items():
    relative = path.relative_to(root)
    if page.h1_count != 1:
        errors.append(f"{relative}: expected one H1, got {page.h1_count}")
    for link in page.links:
        url = urlsplit(urljoin("https://saeed.im/" + str(relative), link))
        if url.scheme not in ("http", "https") or url.netloc != "saeed.im":
            continue
        target = root / unquote(url.path).lstrip("/")
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            errors.append(f"{relative}: missing local link {link}")
        elif url.fragment and target in pages:
            if unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{relative}: missing anchor {link}")

if (root / "CNAME").read_text().strip() != "saeed.im":
    errors.append("Custom domain must remain saeed.im")
for anchor in ("about", "profiles"):
    if anchor not in pages[root / "index.html"].ids:
        errors.append(f"Missing homepage anchor #{anchor}")
json.loads((root / "search.json").read_text())

if errors:
    raise SystemExit("\n".join(errors))
print(f"Checked {len(pages)} pages, local links, anchors, search data, and legacy routes.")
