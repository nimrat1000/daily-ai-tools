import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SECOND_BLOG_ID = os.getenv("SECOND_BLOG_ID")
SECOND_GOOGLE_CLIENT_ID = os.getenv("SECOND_GOOGLE_CLIENT_ID")
SECOND_GOOGLE_CLIENT_SECRET = os.getenv("SECOND_GOOGLE_CLIENT_SECRET")
SECOND_GOOGLE_REFRESH_TOKEN = os.getenv("SECOND_GOOGLE_REFRESH_TOKEN")


def get_second_blogger_service():
    creds = Credentials(
        token=None,
        refresh_token=SECOND_GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=SECOND_GOOGLE_CLIENT_ID,
        client_secret=SECOND_GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/blogger"]
    )

    return build("blogger", "v3", credentials=creds)


def publish_to_second_blog(title, article_html, image_url):
    service = get_second_blogger_service()

    content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.7;">

        <img src="{image_url}" alt="{title}" style="max-width:100%; height:auto; border-radius:12px;" />

        <hr>

        {article_html}

        <hr>

        <p><strong>Disclosure:</strong> This article may contain affiliate links.</p>
        <p><strong>Disclaimer:</strong> This content is for educational and informational purposes only.</p>

    </div>
    """

    post_body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": [
            "AI Tools",
            "Automation",
            "Productivity",
            "AI Agents"
        ]
    }

    post = service.posts().insert(
        blogId=SECOND_BLOG_ID,
        body=post_body,
        isDraft=False
    ).execute()

    return post.get("url")
