import csv
from datetime import datetime

TOPICS_FILE = "data/topics.csv"


def get_related_posts(current_topic, limit=5):
    related_posts = []

    try:
        with open(TOPICS_FILE, newline="", encoding="utf-8") as file:
            topics = list(csv.DictReader(file))
    except FileNotFoundError:
        return []

    for topic in topics:
        same_category = topic.get("category") == current_topic.get("category")
        same_cluster = topic.get("cluster") == current_topic.get("cluster")
        has_url = topic.get("published_url")

        if topic.get("status") == "published" and has_url and (same_category or same_cluster):
            related_posts.append({
                "title": topic.get("title"),
                "url": topic.get("published_url")
            })

    return related_posts[:limit]


def mark_topic_as_published(topic_id, blog_url):
    today = datetime.now().strftime("%Y-%m-%d")

    with open(TOPICS_FILE, newline="", encoding="utf-8") as file:
        topics = list(csv.DictReader(file))
        fieldnames = list(topics[0].keys())

    if "published_url" not in fieldnames:
        fieldnames.append("published_url")

    for topic in topics:
        if str(topic.get("id")) == str(topic_id):
            topic["status"] = "published"
            topic["last_published"] = today
            topic["times_published"] = str(int(topic.get("times_published", 0)) + 1)
            topic["published_url"] = blog_url

    with open(TOPICS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics)
