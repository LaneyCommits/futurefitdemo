"""
Fetch campus images from Wikipedia and school websites.
Shared logic for management command and on-demand API.
"""
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser


class OGImageParser(HTMLParser):
    """Extract og:image from HTML meta tags."""

    def __init__(self):
        super().__init__()
        self.og_image = None

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attrs_d = dict(attrs)
        if attrs_d.get("property") == "og:image" or attrs_d.get("name") == "og:image":
            content = attrs_d.get("content") or attrs_d.get("value")
            if content and content.startswith("http"):
                self.og_image = content


def fetch_wikipedia_image(name, city="", state=""):
    """Search Wikipedia for the college and return the main image URL, or None."""
    search_term = f"{name}"
    if city or state:
        search_term += f" {city} {state}"
    search_term = search_term.strip()

    url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query"
        "&list=search"
        f"&srsearch={urllib.parse.quote(search_term)}"
        "&srlimit=3"
        "&format=json"
        "&origin=*"
    )

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "ExploringU/1.0 (campus finder)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode()
    except Exception:
        return None

    try:
        j = json.loads(data)
        hits = j.get("query", {}).get("search", [])
        if not hits:
            return None

        page_ids = [str(h["pageid"]) for h in hits[:3]]
        page_ids_param = "|".join(page_ids)

        img_url = (
            "https://en.wikipedia.org/w/api.php"
            "?action=query"
            f"&pageids={page_ids_param}"
            "&prop=pageimages"
            "&format=json"
            "&pithumbsize=640"
            "&pilimit=1"
            "&origin=*"
        )

        req2 = urllib.request.Request(
            img_url, headers={"User-Agent": "ExploringU/1.0 (campus finder)"}
        )
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            data2 = resp2.read().decode()

        j2 = json.loads(data2)
        pages = j2.get("query", {}).get("pages", {})

        for pid in page_ids:
            p = pages.get(pid, {})
            thumbs = p.get("thumbnail") or p.get("original") or {}
            src = thumbs.get("source")
            if src and "upload.wikimedia.org" in src:
                return src

        return None
    except Exception:
        return None


def fetch_website_image(website_url):
    """Fetch school homepage and extract og:image or campus image. Returns URL or None."""
    if not website_url or not website_url.startswith("http"):
        return None

    try:
        req = urllib.request.Request(
            website_url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; ExploringU/1.0; +https://exploringu.edu)",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return None

    parser = OGImageParser()
    try:
        parser.feed(html[:100000])
    except Exception:
        pass

    if parser.og_image:
        return parser.og_image

    img_match = re.search(
        r'<img[^>]+src=["\']([^"\']+(?:campus|building|main|aerial|overview)[^"\']*\.(?:jpg|jpeg|png|webp))["\']',
        html[:150000],
        re.I,
    )
    if img_match:
        src = img_match.group(1)
        if src.startswith("//"):
            return "https:" + src
        if src.startswith("/"):
            parsed = urllib.parse.urlparse(website_url)
            return f"{parsed.scheme}://{parsed.netloc}{src}"
        if src.startswith("http"):
            return src

    return None


def fetch_image_for_college(college):
    """Try Wikipedia then school website. Returns image URL or None."""
    url = fetch_wikipedia_image(college.name, college.city or "", college.state or "")
    if not url and college.website_url:
        url = fetch_website_image(college.website_url)
    return url
