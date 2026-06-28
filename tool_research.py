import csv

TOPICS_FILE = "data/topics.csv"


def get_ai_tool_topic():
    with open(TOPICS_FILE, newline="", encoding="utf-8") as file:
        topics = list(csv.DictReader(file))

    unused_topics = [
        topic for topic in topics
        if topic.get("status", "").lower() == "unused"
    ]

    if not unused_topics:
        raise Exception("No unused topics left in topics.csv")

    selected = sorted(
        unused_topics,
        key=lambda x: int(x.get("priority", 0)),
        reverse=True
    )[0]

    return {
        "id": selected["id"],
        "title": selected["title"],
        "keyword": selected["keyword"],
        "tool_name": selected["tool_name"],
        "audience": selected.get("audience", "AI tool users"),
        "problem": selected["title"],
        "category": selected["category"],
        "cluster": selected.get("cluster", ""),
        "search_intent": selected.get("search_intent", ""),
        "difficulty": selected.get("difficulty", ""),
        "search_volume": selected.get("search_volume", ""),
        "affiliate_program": selected.get("affiliate_program", ""),
        "source": selected.get("source", "")
    }
