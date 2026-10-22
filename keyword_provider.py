"""Paid optional keyword enrichment via DataForSEO Keyword Overview.
Never fabricate missing metrics; no credentials means skip without API spend.
"""
import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "research_reports"
URL = "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live"
MAX_KEYWORDS = 12  # deliberately small cost-controlled seed set


def collect():
    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")
    if not (login and password):
        print("DataForSEO credentials absent; paid metrics not fetched.")
        return False
    seeds = json.loads((ROOT / "research_seeds.json").read_text(encoding="utf-8"))["brands"]
    pairs = [(brand, keyword) for brand, keywords in seeds.items() for keyword in keywords][:MAX_KEYWORDS]
    keywords = list(dict.fromkeys(keyword for _, keyword in pairs))
    token = base64.b64encode(f"{login}:{password}".encode()).decode()
    body = json.dumps([{"keywords": keywords, "location_name": "Canada", "language_code": "en"}]).encode()
    req = Request(URL, data=body, headers={"Authorization": "Basic " + token,
                      "Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=45) as resp:
        response = json.load(resp)
    if response.get("status_code") != 20000 or response.get("tasks_error"):
        raise RuntimeError("Keyword provider rejected request: " + str(response.get("status_message")))
    rows = []
    for task in response.get("tasks", []):
        if task.get("status_code") != 20000:
            raise RuntimeError("Keyword provider task failed: " + str(task.get("status_message")))
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                kw = item.get("keyword") or ""
                info = item.get("keyword_info") or {}
                properties = item.get("keyword_properties") or {}
                kd = properties.get("keyword_difficulty")
                if kd is None:
                    kd = item.get("keyword_difficulty")
                rows.append({"keyword": kw, "brands": [b for b,k in pairs if k.lower()==kw.lower()],
                             "monthly_search_volume": info.get("search_volume"),
                             "ads_competition": info.get("competition_level"),
                             "ads_competition_index": info.get("competition"),
                             "organic_difficulty": kd,
                             "keyword_intent": (item.get("search_intent_info") or {}).get("main_intent"),
                             "data_source": "DataForSEO Google Keyword Overview (Google Ads-derived volume)",
                             "measured_utc": datetime.now(timezone.utc).isoformat()})
    OUT.mkdir(exist_ok=True)
    (OUT/"keyword_live.json").write_text(json.dumps({"rows":rows,"count":len(rows)},indent=2)+"\n",encoding="utf-8")
    lines=["# Google Keyword Measurements (Canada, English)", "",
           "Source: DataForSEO Google Keyword Overview (Google Ads-derived search volume); estimated organic difficulty.",
           "Advertiser competition is NOT organic difficulty. Missing data is left blank.",
           "",
           "| Keyword | Avg monthly searches | Ads competition | Organic difficulty |",
           "|---|---:|---|---:|"]
    for r in rows:
        lines.append("| "+str(r["keyword"]).replace("|","/")+" | "+
                     str(r["monthly_search_volume"] if r["monthly_search_volume"] is not None else "N/A")+" | "+
                     str(r["ads_competition"] if r["ads_competition"] is not None else "N/A")+" | "+
                     str(r["organic_difficulty"] if r["organic_difficulty"] is not None else "N/A")+" |")
    (OUT/"keyword_live.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Measured",len(rows),"keywords")
    return True

if __name__ == "__main__":
    collect()
