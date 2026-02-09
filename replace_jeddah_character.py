"""
Replace Jeddah Character Image
Downloads the new image from the user's message and replaces the old one
"""
import requests
import shutil
import os
from datetime import datetime

# The new image URL (you'll need to save the image first)
# For now, let's create a timestamp-based filename
timestamp = int(datetime.now().timestamp())
new_filename = f"jeddah_character_updated_{timestamp}.jpg"

print(f"New character filename: {new_filename}")
print("\nPlease save the new character image as:")
print(f"static/characters/{new_filename}")
print("\nThen we'll:")
print("1. Upload to Cloudinary")
print("2. Update replicate_helper.py")
print("3. Update index.html")
