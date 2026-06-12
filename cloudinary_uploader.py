import os
import cloudinary
import cloudinary.uploader


def upload_image(image_path):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

    upload_result = cloudinary.uploader.upload(
        image_path,
        folder="daily-ai-tools",
        resource_type="image",
        format="png"
    )

    return upload_result["secure_url"]
