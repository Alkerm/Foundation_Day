"""
Simple Cloudinary Upload Script
"""
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

print("Uploading northern_character_v1...")
result = cloudinary.uploader.upload(
    "static/characters/northern_character_v1_1770658524617.jpg",
    public_id="northern_character_v1",
    folder="templates",
    overwrite=True
)

print(f"URL: {result['secure_url']}")
print(f"Public ID: {result['public_id']}")
