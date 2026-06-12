import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


BLOG_ID = os.getenv("BLOG_ID")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")


def get_blogger_service():
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/blogger"]
    )

    return build("blogger", "v3", credentials=creds)


def publish_blog_post(title, article_html, image_url):
    service = get_blogger_service()

    content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.7;">

        <img src="{image_url}" alt="{title}" style="max-width:100%; height:auto; border-radius:12px;" />

        <hr>

        {article_html}

        <hr>

        <h2>Disclosure</h2>
        <p>
        This article may contain affiliate links. We may earn a commission at no extra cost to you.
        </p>

        <h2>Disclaimer</h2>
        <p>
        This content is for educational and informational purposes only.
        It should not be considered professional, financial, legal, or business advice.
        </p>

    </div>
    """

    post_body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": [
            "AI Tools",
            "Artificial Intelligence",
            "Productivity",
            "Automation",
            "Online Business"
        ]
    }

    post = service.posts().insert(
        blogId=BLOG_ID,
        body=post_body,
        isDraft=False
    ).execute()

    return post.get("url")
