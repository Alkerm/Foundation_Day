
import cloudinary
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

print("Listing templates...")
result = cloudinary.api.resources(
    type="upload",
    prefix="templates/",
    max_results=10
)

for resource in result.get('resources', []):
    print(f"ID: {resource['public_id']}")
    print(f"URL: {resource['secure_url']}")
