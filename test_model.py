"""
Simple test to check Replicate model availability
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API token
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Testing codeplugtech/face-swap model...")

try:
    model = replicate.models.get("codeplugtech/face-swap")
    print(f"✓ Model found: {model.name}")
    version = model.latest_version
    print(f"✓ Latest version: {version.id}")
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nThis model may not exist or may have been removed.")
    print("Checking alternative models...")
    
    alternatives = [
        "lucataco/faceswap",
        "omniedgeio/face-swap", 
        "yan-ops/face_swap"
    ]
    
    for alt in alternatives:
        try:
            m = replicate.models.get(alt)
            print(f"✓ Available: {alt}")
        except:
            print(f"✗ Not available: {alt}")
