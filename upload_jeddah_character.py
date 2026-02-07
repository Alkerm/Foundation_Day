"""
Upload Jeddah character to Cloudinary
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

# Upload the image
image_path = 'static/characters/jeddah_character_updated_1770487272655.jpg'

try:
    print(f"Uploading {image_path} to Cloudinary...")
    result = cloudinary.uploader.upload(
        image_path,
        folder='templates',
        public_id='jeddah_character_updated',
        overwrite=True,
        resource_type='image'
    )
    
    print(f"\n✓ Upload successful!")
    print(f"URL: {result['secure_url']}")
    print(f"\nAdd this URL to replicate_helper.py:")
    print(f"'template_image': '{result['secure_url']}'")
    
except Exception as e:
    print(f"✗ Upload failed: {e}")
