import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

covered_topics = []

def write_article(tool_data):
    avoid_section = ""
    if covered_topics:
        avoid_section = f"""
Already covered in previous articles (DO NOT repeat or re-explain these):
{chr(10).join(f'- {t}' for t in covered_topics)}
If any of these tools are mentioned, just briefly reference them — do not give full explanations again.
"""

    prompt = f"""
You are a real person who blogs about AI tools in your spare time.
You write like you actually use these tools — casually, honestly, and helpfully.
You are NOT a marketing writer. You don't hype things up.

Write a blog article with these requirements:
- 1200 to 1800 words
- Written in first person ("I tried this...", "In my experience...", "I was surprised by...")
- Conversational and beginner-friendly — like explaining to a friend
- Naturally SEO optimized (don't stuff keywords, just use them where they fit)
- Use H2 and H3 headings
- Include a real practical example (step by step, specific)
- Include honest pros and cons (not just positives)
- Include a short conclusion with your personal recommendation
- Include 4-5 FAQ questions that real beginners would actually ask
- No fake claims or exaggerated results
- No phrases like "In today's fast-paced world" or "Look no further"
- Sound like a human, not a robot or marketer

Topic: {tool_data['title']}
Target Keyword: {tool_data['keyword']}
Audience: {tool_data['audience']}
Problem this article solves: {tool_data['problem']}
Tone: {tool_data.get('tone', 'friendly and honest')}

{avoid_section}

Return clean HTML only. Use proper tags: <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em>.
Do not include <html>, <head>, or <body> tags.
Do not wrap in markdown code blocks.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    article_html = response.content[0].text
    article_html = article_html.replace("```html", "").replace("```", "").strip()

    disclaimer = """
<hr>
<p><small><strong>Disclosure:</strong> This article may contain affiliate links. 
We may earn a small commission at no extra cost to you if you purchase through our links. 
We only recommend tools we've genuinely reviewed.</small></p>
"""

    meta_suggestion = f"""
<!-- 
SEO TITLE: {tool_data['title']} | Honest Review 2026
META DESCRIPTION: {tool_data['keyword']} — honest beginner-friendly guide covering pros, cons, and real examples.
-->
"""

    covered_topics.append(tool_data['title'])

    return meta_suggestion + article_html + disclaimer
