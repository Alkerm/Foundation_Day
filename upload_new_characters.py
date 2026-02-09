"""
Upload New Characters to Cloudinary
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

print("="*60)
print("UPLOADING NEW CHARACTERS TO CLOUDINARY")
print("="*60)

# Upload Jeddah character
print("\n1. Uploading Jeddah character...")
jeddah_result = cloudinary.uploader.upload(
    "static/characters/jeddah_character_updated_1770660835227.jpg",
    public_id="jeddah_updated_v2",
    folder="templates",
    overwrite=True
)
print(f"✅ Jeddah uploaded: {jeddah_result['secure_url']}")

# Upload Northern female character
print("\n2. Uploading Northern female character...")
northern_result = cloudinary.uploader.upload(
    "static/characters/northern_woman_v1_1770658383334.jpg",
    public_id="northern_woman_v1",
    folder="templates",
    overwrite=True
)
print(f"✅ Northern female uploaded: {northern_result['secure_url']}")

print("\n" + "="*60)
print("UPLOAD COMPLETE!")
print("="*60)
print(f"\nJeddah URL: {jeddah_result['secure_url']}")
print(f"Northern URL: {northern_result['secure_url']}")
