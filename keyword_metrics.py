"""Analyze measured keyword exports, without inventing search metrics.

Input: data/keyword_metrics.csv exported from Google Keyword Planner.
Optional column: organic_keyword_difficulty, from an explicitly sourced SEO provider.
Output: research_reports/keyword_opportunities.csv and .md

Run: python keyword_metrics.py --input data/keyword_metrics.csv
"""
import argparse
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def number(raw):
    s = str(raw or "").strip().replace(",", "").replace("$", "")
    if not s or s in {"--", "-", "N/A", "null"}:
        return None
    # Google may provide ranges on restricted accounts: do not convert to exact volumes.
    if any(x in s for x in ("<", ">", "–", " - ", "+")):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_export(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    # Keyword Planner may prepend "Keyword Stats ...", date lines etc.
    keys = ("keyword", "avg. monthly searches", "average monthly searches")
    header_index = next((i for i, line in enumerate(lines)
                         if "keyword" in line.lower() and
                         any(k in line.lower() for k in keys[1:])), None)
    if header_index is None:
        header_index = next((i for i, line in enumerate(lines)
                             if line.lower().startswith(("keyword,", "keyword\\t"))), None)
    if header_index is None:
        raise ValueError("Cannot find keyword CSV header. Supply a Google Keyword Planner CSV.")
    content = "\n".join(lines[header_index:])
    dialect = csv.excel_tab if "\t" in lines[header_index] and "," not in lines[header_index] else csv.excel
    return list(csv.DictReader(io.StringIO(content), dialect=dialect))


def col(record, *names):
    lookup = {k.lower().strip().replace("_", " "): v for k, v in record.items() if k}
    for name in names:
        if name.lower().replace("_", " ") in lookup:
            return lookup[name.lower().replace("_", " ")]
    return ""


def analyze(rows):
    findings = []
    for row in rows:
        keyword = col(row, "Keyword", "Search term").strip()
        if not keyword:
            continue
        volume_raw = col(row, "Avg. monthly searches", "Average monthly searches", "Avg monthly searches")
        volume = number(volume_raw)
        ads_comp = col(row, "Competition", "Paid competition")
        ads_index = number(col(row, "Competition (indexed value)", "Competition index", "competition_index"))
        kd = number(col(row, "Organic keyword difficulty", "keyword_difficulty", "Organic difficulty"))
        if kd is not None and not 0 <= kd <= 100:
            kd = None
        low_bid = number(col(row, "Top of page bid (low range)", "Low top of page bid"))
        high_bid = number(col(row, "Top of page bid (high range)", "High top of page bid"))
        # Only describe a potential opportunity when organic difficulty was actually supplied.
        verdict = "needs organic difficulty data"
        if volume is not None and kd is not None:
            if volume >= 100 and kd <= 25:
                verdict = "review: measurable demand and relatively low reported organic difficulty"
            else:
                verdict = "review: check SERP relevance and site fit"
        findings.append({
            "keyword": keyword,
            "avg_monthly_searches": "" if volume is None else int(volume),
            "volume_as_reported": volume_raw,
            "ads_competition": ads_comp,
            "ads_competition_index": "" if ads_index is None else int(ads_index),
            "organic_keyword_difficulty": "" if kd is None else int(kd),
            "top_page_bid_low": "" if low_bid is None else low_bid,
            "top_page_bid_high": "" if high_bid is None else high_bid,
            "assessment": verdict,
        })
    findings.sort(key=lambda r: (
        r["organic_keyword_difficulty"] == "",
        r["organic_keyword_difficulty"] if r["organic_keyword_difficulty"] != "" else 101,
        -(r["avg_monthly_searches"] if r["avg_monthly_searches"] != "" else -1)))
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    rows = read_export(args.input)
    results = analyze(rows)
    out = ROOT / "research_reports"
    out.mkdir(exist_ok=True)
    columns = ["keyword", "avg_monthly_searches", "volume_as_reported", "ads_competition",
               "ads_competition_index", "organic_keyword_difficulty", "top_page_bid_low",
               "top_page_bid_high", "assessment"]
    with (out / "keyword_opportunities.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(results)
    lines = ["# Measured keyword opportunities", "",
             f"Analyzed {len(results)} keywords from supplied CSV.",
             "Google Ads Competition is paid advertising competition, NOT difficulty ranking organically.",
             "Organic difficulty is only shown when an external provider's score exists in the input.",
             "Search volume may be approximate, grouped by close variants, or shown as ranges.",
             "Do not treat the assessments as ranking guarantees.", "",
             "| Keyword | Monthly searches | Ads competition | Organic difficulty | Assessment |",
             "|---|---:|---|---:|---|"]
    for r in results[:50]:
        safe = lambda s: str(s).replace("|", "/")
        lines.append(f"| {safe(r['keyword'])} | {r['avg_monthly_searches'] if r['avg_monthly_searches'] != '' else safe(r['volume_as_reported'])} | {safe(r['ads_competition'])} | {r['organic_keyword_difficulty']} | {safe(r['assessment'])} |")
    (out / "keyword_opportunities.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote keyword reports:", len(results), "rows")


if __name__ == "__main__":
    main()
