# -*- coding: utf-8 -*-
"""
Audit the generated site. Run after build.py:  python scripts/check_site.py

Checks links/anchors, images and alt text, heading structure, titles and meta
descriptions, duplicate ids, repeated copy, British spelling and common
punctuation slips. Exits with status 1 if anything needs fixing.
"""
import glob
import html
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

US_SPELLINGS = re.compile(
    r"\b(colors?|colored|coloring|centers?|centered|behaviors?|favorites?|catalogs?|"
    r"analy[z]\w*|defense|theater|gray|fulfill|enrollment|paraly[z]\w*)\b", re.I)
# -ise words that are fine in British English are not listed; "-ize" forms are flagged above
IZE = re.compile(r"\b(?!size|sizes|prize|seize|resize|capsize)\w{3,}iz(e|es|ed|ing|ation|ations)\b", re.I)
AMERICAN_OK = {"organization"}  # schema.org type name inside JSON-LD is not visible text


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.canonical = None
        self.links = []
        self.images = []
        self.headings = []
        self.ids = []
        self.text = []
        self._skip = 0
        self._in_title = False
        self._head_tag = None
        self.landmarks = set()
        self.main_text = []
        self._main = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        elif tag == "img":
            self.images.append(a)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._head_tag = tag
            self.headings.append([int(tag[1]), ""])
        elif tag in ("main", "nav", "header", "footer"):
            self.landmarks.add(tag)
        if tag == "main":
            self._main += 1

    def handle_endtag(self, tag):
        if tag == "main":
            self._main -= 1
        if tag in ("script", "style"):
            self._skip -= 1
        elif tag == "title":
            self._in_title = False
        elif tag == self._head_tag:
            self._head_tag = None
        elif tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "section", "summary", "td", "ul", "nav"):
            self.text.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._skip:
            return
        if self._head_tag and self.headings:
            self.headings[-1][1] += data
        self.text.append(data)
        if self._main:
            self.main_text.append(data)


def parse(path):
    p = Page()
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    p.feed(raw)
    p.raw = raw
    return p


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    pages = {os.path.basename(f): parse(f) for f in files}
    problems, warnings = [], []
    titles, descs = {}, {}

    def bad(name, msg):
        problems.append("%s: %s" % (name, msg))

    def warn(name, msg):
        warnings.append("%s: %s" % (name, msg))

    ids_by_page = {n: set(p.ids) for n, p in pages.items()}

    for name, p in pages.items():
        # --- links / anchors -------------------------------------------------
        for href in p.links:
            if re.match(r"^(mailto:|tel:|https?://|#$)", href):
                continue
            if href.startswith("#"):
                if href[1:] not in ids_by_page[name]:
                    bad(name, "missing in-page anchor %s" % href)
                continue
            target, _, frag = href.partition("#")
            target = target.partition("?")[0]
            if target not in pages and not os.path.exists(os.path.join(ROOT, target)):
                bad(name, "broken link %s" % href)
            elif frag and target in ids_by_page and frag not in ids_by_page[target]:
                bad(name, "anchor #%s missing on %s" % (frag, target))
        # --- images ----------------------------------------------------------
        for im in p.images:
            src = im.get("src", "")
            if src and not src.startswith("http") and not os.path.exists(os.path.join(ROOT, src)):
                bad(name, "missing image %s" % src)
            if "alt" not in im:
                bad(name, "image without alt: %s" % src)
            if not (im.get("width") and im.get("height")):
                warn(name, "image without width/height: %s" % src)
        # --- headings --------------------------------------------------------
        levels = [h[0] for h in p.headings]
        if levels.count(1) != 1:
            bad(name, "expected one h1, found %d" % levels.count(1))
        for a, b in zip(levels, levels[1:]):
            if b > a + 1:
                bad(name, "heading level jumps h%d -> h%d (%s)" % (a, b, p.headings[levels.index(b)][1][:40]))
                break
        for h in p.headings:
            if not h[1].strip():
                bad(name, "empty h%d" % h[0])
        # --- head ------------------------------------------------------------
        t = p.title.strip()
        d = p.meta.get("description", "")
        if not t:
            bad(name, "no <title>")
        elif len(t) > 65:
            warn(name, "title is %d chars (aim for 60 or fewer): %s" % (len(t), t))
        if not d:
            bad(name, "no meta description")
        elif not 70 <= len(d) <= 165:
            warn(name, "meta description is %d chars" % len(d))
        titles.setdefault(t, []).append(name)
        descs.setdefault(d, []).append(name)
        if not p.canonical:
            bad(name, "no canonical")
        if "main" not in p.landmarks:
            bad(name, "no <main> landmark")
        dup = [i for i in set(p.ids) if p.ids.count(i) > 1]
        if dup:
            bad(name, "duplicate ids %s" % dup)

        # --- copy ------------------------------------------------------------
        text = html.unescape("".join(p.text))
        text = re.sub(r"[ \t\r\f]+", " ", text)
        n_nut = text.count("In a nutshell")
        if n_nut > 1:
            bad(name, "'In a nutshell' used %d times" % n_nut)
        for m in US_SPELLINGS.finditer(text):
            w = m.group(0)
            if w.lower() not in AMERICAN_OK:
                bad(name, "possible American spelling: %s" % w)
        for m in IZE.finditer(text):
            bad(name, "possible -ize spelling: %s" % m.group(0))
        for m in re.finditer(r"\b(\w+)[ ]+\1\b", text, re.I):
            if m.group(1).lower() not in ("that", "had") and not m.group(1).isdigit():
                bad(name, "repeated word: %s" % m.group(0))
        for pat, msg in ((r"\s[,.;:!?](?!\w)", "space before punctuation"), (r"\.\.(?!\.)", "double full stop"),
                         (r",,", "double comma")):
            for m in re.finditer(pat, text):
                ctx = text[max(0, m.start() - 20):m.end() + 10].replace("\n", " ")
                bad(name, "%s near %r" % (msg, ctx))
        for m in re.finditer(r"\b([Aa]) ([aeiou]\w*)", text):
            if m.group(2).lower() not in ("user", "users", "unique", "one", "once", "useful", "usual", "utility", "uniform",
                                            "university", "european", "usb", "url", "unit", "uk", "us", "ui", "ux"):
                bad(name, "article: %r (use 'an' before a vowel sound)" % m.group(0))
        for m in re.finditer(r"\b[Aa] (AEO|AI|SEO|FAQ|HTML|MP|LLC|NHS|MVP|RSS|SSL|SMS|SQL|HR)\b", text):
            bad(name, "article: %r (use 'an' before this acronym)" % m.group(0))
        for m in re.finditer(r"\b[Aa]n ([^aeiouAEIOU\W]\w*)", text):
            w = m.group(1)
            if not (w.isupper() or w.lower().startswith(("hour", "honest", "honour", "heir"))):
                bad(name, "article: %r (use 'a' before a consonant sound)" % m.group(0))
        if " - " in text:
            bad(name, "spaced hyphen used as a dash")
        if re.search(r"\w'\w", text):
            warn(name, "straight apostrophe in text")

    # unique titles / descriptions
    for t, names in titles.items():
        if len(names) > 1 and t:
            bad(",".join(names[:3]), "duplicate title %r (%d pages)" % (t, len(names)))
    for d, names in descs.items():
        if len(names) > 1 and d:
            bad(",".join(names[:3]), "duplicate meta description (%d pages)" % len(names))

    # how distinct are the location pages from each other? (body copy only, city name normalised)
    from collections import Counter
    for prefix in ("website-design-", "seo-services-"):
        group = [n for n in pages if n.startswith(prefix) and n not in ("website-design.html", "seo-services.html")]
        if not group:
            continue
        sents = {}
        for n in group:
            city = n[len(prefix):-5].replace("-", " ")
            txt = re.sub(re.escape(city), "CITY", html.unescape("".join(pages[n].main_text)), flags=re.I)
            sents[n] = [x.strip() for x in re.split(r"(?<=[.!?])\s+|\n+", txt) if len(x.strip().split()) >= 6]
        c = Counter(x for v in sents.values() for x in set(v))
        total = sum(len(x.split()) for v in sents.values() for x in v)
        unique = sum(len(x.split()) for v in sents.values() for x in v if c[x] == 1)
        print("%s* pages: %d pages, %.0f%% of body words are unique to the page" % (prefix, len(group), 100.0 * unique / max(total, 1)))

    print("\n%d pages checked" % len(pages))
    for w in warnings[:40]:
        print("WARN ", w)
    if len(warnings) > 40:
        print("... and %d more warnings" % (len(warnings) - 40))
    for pr in problems[:80]:
        print("FIX  ", pr)
    if len(problems) > 80:
        print("... and %d more problems" % (len(problems) - 80))
    print("\n%d problems, %d warnings" % (len(problems), len(warnings)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
