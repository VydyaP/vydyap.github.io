"""Checks the site before it is deployed (run in CI and locally: python scripts/check_site.py).

* every local file an HTML page references (images, CSS, icons) exists
* every image has non-empty alt text and width/height (prevents layout shift)
* in-page links (#projects) point at an element that exists
* no page links over plain http://
Standard library only, so CI needs no installs.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[tuple[str, str]] = []  # (attribute, value)
        self.images: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"] or "")
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append((key, a[key] or ""))
        if tag == "img":
            self.images.append(a)


def check(path: Path) -> list[str]:
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    errors = []
    for _, ref in page.refs:
        if ref.startswith("http://"):
            errors.append(f"insecure link {ref}")
        elif ref.startswith("#"):
            if len(ref) > 1 and ref[1:] not in page.ids:
                errors.append(f"in-page link {ref} has no matching id")
        elif not ref.startswith(("https://", "mailto:")) and ref != "/":
            target = ROOT / ref.lstrip("/").split("#")[0]
            if not target.exists():
                errors.append(f"missing file {ref}")
    for img in page.images:
        if not (img.get("alt") or "").strip():
            errors.append(f"image without alt text: {img.get('src')}")
        if not (img.get("width") and img.get("height")):
            errors.append(f"image without width/height: {img.get('src')}")
    return [f"{path.name}: {e}" for e in errors]


def main() -> int:
    errors = [e for page in sorted(ROOT.glob("*.html")) for e in check(page)]
    for e in errors:
        print("ERROR", e)
    print(f"checked {len(list(ROOT.glob('*.html')))} page(s): {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
