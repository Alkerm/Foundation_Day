"""
Upload both child characters to Cloudinary
"""
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Upload both images
images = [
    {
        'path': 'static/characters/jeddah_child_character_1770488423422.jpg',
        'public_id': 'jeddah_child_character'
    },
    {
        'path': 'static/characters/daglah_child_character_1770488439465.jpg',
        'public_id': 'daglah_child_character'
    }
]

for img in images:
    try:
        print(f"\nUploading {img['path']} to Cloudinary...")
        result = cloudinary.uploader.upload(
            img['path'],
            folder='templates',
            public_id=img['public_id'],
            overwrite=True,
            resource_type='image'
        )
        
        print(f"✓ Upload successful!")
        print(f"URL: {result['secure_url']}")
        
    except Exception as e:
        print(f"✗ Upload failed for {img['path']}: {e}")

print("\n✓ All uploads complete!")
