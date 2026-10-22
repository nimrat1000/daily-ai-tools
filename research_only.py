"""Research-only discovery. No AI writing, image creation or Blogger publishing.

Sources: Google News RSS with search queries, collected as external leads.
Findings are candidates, not validated Google search volumes or rankings.
"""
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "research_reports"
SEEDS = ROOT / "research_seeds.json"
HEADERS = {"User-Agent": "DailyAIToolsResearch/1.0 (+public research)"}


def fetch_news(query, limit=5):
    url = "https://news.google.com/rss/search?q=" + quote(query) + "&hl=en-CA&gl=CA&ceid=CA:en"
    with urlopen(Request(url, headers=HEADERS), timeout=20) as response:
        xml_data = response.read(2_000_000)
    root = ElementTree.fromstring(xml_data)
    items = []
    for item in root.findall(".//channel/item")[:limit]:
        source = item.find("source")
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "url": (item.findtext("link") or "").strip(),
            "published": (item.findtext("pubDate") or "").strip(),
            "publisher": source.text.strip() if source is not None and source.text else "",
        })
    return items


def main():
    config = json.loads(SEEDS.read_text(encoding="utf-8"))
    OUTPUT.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report = {"generated_utc": datetime.now(timezone.utc).isoformat(),
              "method": "Google News RSS; topic leads only, not keyword volume or difficulty",
              "brands": {}, "errors": []}
    for brand, queries in config["brands"].items():
        report["brands"][brand] = []
        for query in queries:
            try:
                results = fetch_news(query)
                report["brands"][brand].append({
                    "query": query, "results": results,
                    "interpretation": "Research leads requiring independent fact and keyword validation"
                })
            except Exception as exc:
                report["errors"].append({"brand": brand, "query": query,
                                         "error_type": type(exc).__name__,
                                         "message": str(exc)[:250]})
    (OUTPUT / "latest.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Research leads | " + today, "",
             "Research only. Headlines are third-party leads, not verified claims. No writing or publishing performed.",
             "No search volume, keyword difficulty or demand estimate is inferred.", ""]
    for brand, blocks in report["brands"].items():
        lines += ["## " + brand, ""]
        for block in blocks:
            lines += ["### " + block["query"], ""]
            if not block["results"]:
                lines += ["No results found.", ""]
            for item in block["results"]:
                title = item["title"].replace("[", "").replace("]", "")
                lines += [f"- [{title}]({item['url']}) | {item['publisher']} | {item['published']}"]
            lines.append("")
    if report["errors"]:
        lines += ["## Fetch errors", "", "Some sources failed and must not be treated as complete."]
        for error in report["errors"]:
            lines += [f"- {error['brand']}: {error['query']} ({error['error_type']})"]
    (OUTPUT / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Collected {sum(len(b['results']) for v in report['brands'].values() for b in v)} source leads; {len(report['errors'])} failed queries")
    if report["errors"]:
        raise SystemExit("Incomplete research: see research_reports/latest.json")


if __name__ == "__main__":
    main()
