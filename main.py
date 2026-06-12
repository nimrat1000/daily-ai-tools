from tool_research import get_ai_tool_topic
from article_writer import write_article
from image_creator import create_pin_image
from cloudinary_uploader import upload_image
from blogger_publisher import publish_blog_post
from buffer_publisher import send_to_buffer
from telegram_sender import send_telegram_message


def main():
    try:
        tool_data = get_ai_tool_topic()

        title = tool_data["title"]
        keyword = tool_data["keyword"]

        article_html = write_article(tool_data)

        image_path = create_pin_image(
            title=title,
            keyword=keyword
        )

        image_url = upload_image(image_path)

        blog_url = publish_blog_post(
            title=title,
            article_html=article_html,
            image_url=image_url
        )

        send_to_buffer(
            title=title,
            blog_url=blog_url,
            image_url=image_url
        )

        send_telegram_message(
            f"✅ AI Tools post published successfully!\n\nTitle: {title}\n\nBlog URL:\n{blog_url}"
        )

    except Exception as error:
        send_telegram_message(
            f"❌ AI Tools automation failed:\n\n{error}"
        )
        raise


if __name__ == "__main__":
    main()
