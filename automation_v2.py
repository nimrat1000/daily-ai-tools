"""Safe offline staging layer. Does not publish or call paid APIs."""
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


def validate_topic(topic, settings):
    errors = []
    brand = settings["brands"].get(topic.get("brand"))
    if not brand:
        errors.append("Unknown brand")
    for field in ("title", "keyword", "reader_question"):
        if not str(topic.get(field, "")).strip():
            errors.append(f"Missing {field}")
    if brand:
        dest = topic.get("destination", "")
        if dest and dest not in brand["destinations"]:
            errors.append("Unapproved destination URL")
    if settings.get("publishing_enabled") or settings.get("mode") != "draft_only":
        errors.append("Staging tool requires draft_only mode")
    if topic.get("sources") is None:
        errors.append("Provide sources list, even if empty")
    if not isinstance(topic.get("sources"), list):
        errors.append("Sources must be a list")
    return errors


def stage_topic(topic):
    settings = json.loads((ROOT / "automation_config.json").read_text(encoding="utf-8"))
    errors = validate_topic(topic, settings)
    if errors:
        raise ValueError("; ".join(errors))
    brief = {
        "topic": topic,
        "state": "needs_research" if not topic["sources"] else "needs_source_verification",
        "publishable": False,
        "editorial_instructions": settings["voice"],
        "image_brief": f"Realistic, occasionally witty, relevant to '{topic['keyword']}'. No fabricated chart or screenshot.",
        "next_checks": ["verify sources", "write article", "check facts and figures",
                        "obtain and validate visuals", "approve manually"],
    }
    outbox = ROOT / "outbox"
    outbox.mkdir(exist_ok=True)
    target = outbox / "staged-topic.json"
    target.write_text(json.dumps(brief, indent=2), encoding="utf-8")
    return target


if __name__ == "__main__":
    topic = {
        "brand": "totalyields",
        "title": "Dividend Yield vs Total Return: What's Different?",
        "keyword": "dividend yield vs total return",
        "reader_question": "Does receiving ETF distributions mean my investment gained?",
        "destination": "https://countyield.base44.app",
        "sources": [],
    }
    print("Staged (not published):", stage_topic(topic))
