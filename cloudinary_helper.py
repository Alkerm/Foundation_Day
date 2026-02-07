"""
Cloudinary Helper Module
Handles temporary image uploads for AI processing with automatic cleanup.
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import os
import uuid
import time
from typing import Optional, Dict

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)


def upload_temp_image(image_bytes: bytes) -> Optional[Dict[str, str]]:
    """
    Upload an image to Cloudinary for temporary storage.
    
    Args:
        image_bytes: Image data as bytes
        
    Returns:
        Dict with 'url' and 'public_id' if successful, None if failed
    """
    try:
        # Generate unique public_id with timestamp
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        public_id = f"temp_face_{timestamp}_{unique_id}"
        
        print(f"[Cloudinary] Uploading image with ID: {public_id}", flush=True)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            image_bytes,
            public_id=public_id,
            folder="temp_faces",  # Organize in folder
            tags=["temp", "face_swap"],  # Tag for cleanup
            resource_type="image",
            overwrite=True
        )
        
        secure_url = result.get('secure_url')
        print(f"[Cloudinary] Upload successful: {secure_url}", flush=True)
        
        return {
            'url': secure_url,
            'public_id': result.get('public_id')
        }
        
    except Exception as e:
        print(f"[Cloudinary] Upload failed: {str(e)}", flush=True)
        return None


def delete_temp_image(public_id: str) -> bool:
    """
    Delete a temporary image from Cloudinary.
    
    Args:
        public_id: The public_id returned from upload_temp_image
        
    Returns:
        True if deletion successful, False otherwise
    """
    try:
        print(f"[Cloudinary] Deleting image: {public_id}", flush=True)
        result = cloudinary.uploader.destroy(public_id)
        
        if result.get('result') == 'ok':
            print(f"[Cloudinary] Deletion successful", flush=True)
            return True
        else:
            print(f"[Cloudinary] Deletion failed: {result}", flush=True)
            return False
            
    except Exception as e:
        print(f"[Cloudinary] Deletion error: {str(e)}", flush=True)
        return False


def cleanup_old_temp_images(hours_old: int = 24) -> int:
    """
    Cleanup temporary images older than specified hours.
    This is a fallback cleanup in case immediate deletion fails.
    
    Args:
        hours_old: Delete images older than this many hours (default: 24)
        
    Returns:
        Number of images deleted
    """
    try:
        print(f"[Cloudinary] Running cleanup for images older than {hours_old} hours", flush=True)
        
        # Calculate timestamp for cutoff
        cutoff_timestamp = int(time.time()) - (hours_old * 3600)
        
        # Search for old temp images
        # Note: This requires Admin API access
        result = cloudinary.api.resources(
            type="upload",
            prefix="temp_faces/",
            tags=True,
            max_results=500
        )
        
        deleted_count = 0
        for resource in result.get('resources', []):
            # Extract timestamp from public_id (format: temp_faces/temp_face_{timestamp}_{uuid})
            public_id = resource.get('public_id', '')
            try:
                # Parse timestamp from public_id
                parts = public_id.split('_')
                if len(parts) >= 3:
                    timestamp = int(parts[2])
                    if timestamp < cutoff_timestamp:
                        if delete_temp_image(public_id):
                            deleted_count += 1
            except (ValueError, IndexError):
                continue
        
        print(f"[Cloudinary] Cleanup complete: {deleted_count} images deleted", flush=True)
        return deleted_count
        
    except Exception as e:
        print(f"[Cloudinary] Cleanup error: {str(e)}", flush=True)
        return 0


def test_connection() -> bool:
    """
    Test Cloudinary connection and credentials.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        # Try to get account info
        result = cloudinary.api.ping()
        print("[Cloudinary] Connection successful!", flush=True)
        print(f"[Cloudinary] Status: {result.get('status')}", flush=True)
        return True
    except Exception as e:
        print(f"[Cloudinary] Connection failed: {str(e)}", flush=True)
        print("[Cloudinary] Please check your credentials in .env file", flush=True)
        return False


if __name__ == "__main__":
    # Test the connection
    print("Testing Cloudinary connection...")
    test_connection()
