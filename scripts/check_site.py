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
        self.gallery_images = []
        self.gallery_links = []
        self.h1_count = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "on-glb" in attrs.get("class", "").split():
            self.gallery_images.append(attrs)
        if tag == "a" and attrs.get("data-gallery") == "photography":
            self.gallery_links.append(attrs.get("href", ""))
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


root = Path("site").resolve()
pages = {path: Page(path) for path in root.rglob("*.html")}
errors = []
# These paths are separate GitHub Pages projects sharing the custom domain.
external_project_paths = ("/quiz_games", "/distribution_playground", "/vazhe")
expected = [
    "index.html", "about/index.html", "research/index.html",
    "publications/index.html", "photography/index.html", "reading/index.html",
    "contact/index.html", "profiles/index.html", "projects/index.html",
    "license/index.html", "404.html",
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
        if any(url.path == path or url.path.startswith(path + "/") for path in external_project_paths):
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
json.loads((root / "search.json").read_text())

gallery = pages[root / "photography/index.html"]
display_files = {p.name for p in (root / "assets/photography/display").glob("*.webp")}
image_names = [Path(img.get("src", "")).name for img in gallery.gallery_images]
link_names = [Path(urlsplit(link).path).name for link in gallery.gallery_links]
if not display_files or set(image_names) != display_files or set(link_names) != display_files:
    errors.append("Photography: every display image must have a thumbnail and lightbox link")
if len(image_names) != len(display_files) or len(link_names) != len(display_files):
    errors.append("Photography: duplicate or missing gallery entries")
for img in gallery.gallery_images:
    if not img.get("alt") or not img.get("width") or not img.get("height"):
        errors.append(f"Photography: missing image description or dimensions: {img.get('src')}")
    if img.get("loading") != "lazy" or "/thumbnails/" not in img.get("src", ""):
        errors.append(f"Photography: gallery must use lazy-loaded thumbnails: {img.get('src')}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Checked {len(pages)} pages, local links, anchors, search data, and legacy routes.")
print(f"Checked {len(display_files)} gallery images and lightbox links.")
