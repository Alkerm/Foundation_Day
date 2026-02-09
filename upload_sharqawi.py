"""
Upload Sharqawi female character to Cloudinary
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

def upload_sharqawi_character():
    """Upload the Sharqawi character to Cloudinary"""
    local_path = "static/characters/sharqawi_dress_character_1770578762613.jpg"
    
    print(f"📤 Uploading {local_path} to Cloudinary...")
    
    try:
        result = cloudinary.uploader.upload(
            local_path,
            folder="templates",
            public_id="sharqawi_dress_character",
            overwrite=True,
            resource_type="image"
        )
        
        print(f"✅ Upload successful!")
        print(f"📍 URL: {result['secure_url']}")
        print(f"🆔 Public ID: {result['public_id']}")
        
        return result['secure_url']
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("UPLOADING SHARQAWI CHARACTER TO CLOUDINARY")
    print("=" * 60)
    
    url = upload_sharqawi_character()
    
    if url:
        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"\nUpdate replicate_helper.py with this URL:")
        print(f"'{url}'")
    else:
        print("\n❌ Upload failed. Please check your Cloudinary credentials.")
