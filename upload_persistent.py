
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

file_path = "static/characters/saudi_traditional_daglah.png"
public_id = "templates/saudi_traditional_daglah"

print(f"Uploading {file_path} to {public_id}...")

try:
    with open(file_path, "rb") as f:
        result = cloudinary.uploader.upload(
            f,
            public_id=public_id,
            unique_filename=False,
            overwrite=True,
            resource_type="image"
        )
        url = result['secure_url']
        print(f"UPLOAD SUCCESS: {url}")
        with open("final_url.txt", "w") as out:
            out.write(url)
except Exception as e:
    print(f"UPLOAD FAILED: {e}")
