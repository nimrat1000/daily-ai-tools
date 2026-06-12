import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def write_article(tool_data):

    prompt = f"""
You are an expert SEO blogger.

Write a detailed blog article.

Requirements:
- 1200 to 1800 words
- Human sounding
- Beginner friendly
- SEO optimized
- Use headings (H2 and H3)
- Include practical examples
- Include pros and cons
- Include conclusion
- Include FAQ section
- No fake claims
- No keyword stuffing

Topic:
{tool_data['title']}

Target Keyword:
{tool_data['keyword']}

Audience:
{tool_data['audience']}

Problem:
{tool_data['problem']}

Return clean HTML only.
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    article_html = response.content[0].text

    disclaimer = """
    <hr>
    <p><strong>Disclosure:</strong>
    This article may contain affiliate links.
    We may earn a commission at no additional cost to you.
    </p>
    """

    return article_html + disclaimer
