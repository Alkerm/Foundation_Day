"""
Add Two New Characters to Website
This script will help upload and configure the new characters
"""
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

def upload_character(image_path, character_id, character_name):
    """Upload a character to Cloudinary"""
    print(f"\n{'='*60}")
    print(f"Uploading {character_name}")
    print(f"{'='*60}")
    
    try:
        result = cloudinary.uploader.upload(
            image_path,
            public_id=character_id,
            folder="templates",
            overwrite=True
        )
        
        url = result['secure_url']
        print(f"✅ Upload successful!")
        print(f"URL: {url}")
        return url
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

# Character 1: Updated Jeddah Male
print("\n" + "="*60)
print("UPLOADING NEW CHARACTERS")
print("="*60)

jeddah_path = input("\nEnter path to Jeddah male character image: ").strip('"').strip("'")
northern_path = input("Enter path to Northern female character image: ").strip('"').strip("'")

if os.path.exists(jeddah_path):
    jeddah_url = upload_character(jeddah_path, "jeddah_updated_v2", "Jeddah Male Character")
else:
    print(f"❌ Jeddah image not found: {jeddah_path}")

if os.path.exists(northern_path):
    northern_url = upload_character(northern_path, "northern_female_v1", "Northern Female Character")
else:
    print(f"❌ Northern image not found: {northern_path}")

print("\n" + "="*60)
print("NEXT STEPS:")
print("="*60)
print("1. Update replicate_helper.py with new character configurations")
print("2. Update index.html to add character cards")
print("3. Copy images to static/characters/")
