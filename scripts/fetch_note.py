"""noteのRSSを取得し、最新記事5件を blog.json に書き出す（GitHub Actionsから1日1回実行）。"""
import json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://note.com/tanakak_lab/rss"
OUT = "blog.json"

req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (tanakak.github.io feed fetcher)"})
with urllib.request.urlopen(req, timeout=30) as r:
    root = ET.fromstring(r.read())

items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    if not title or not link:
        continue
    d = parsedate_to_datetime(it.findtext("pubDate"))
    desc = re.sub(r"<[^>]+>", "", it.findtext("description") or "")
    desc = re.sub(r"\s+", " ", desc).strip()
    items.append({
        "title": title,
        "link": link,
        "date": f"{d.year}年{d.month}月{d.day}日",
        "desc": desc[:60] + ("…" if len(desc) > 60 else ""),
    })
    if len(items) == 5:
        break

if not items:
    sys.exit("記事を取得できませんでした（blog.jsonは更新しません）")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(f"{len(items)} 件を書き出しました")
