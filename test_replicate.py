"""
Test script to diagnose Replicate API issues
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API token
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
if REPLICATE_API_TOKEN:
    os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN
    print(f"✓ API Token configured: {REPLICATE_API_TOKEN[:10]}...")
else:
    print("✗ No API token found!")
    exit(1)

print("\n" + "="*60)
print("Testing Replicate API Connection")
print("="*60)

# Test 1: Basic connection
try:
    print("\n[Test 1] Testing basic connection...")
    models = list(replicate.models.list())[:3]
    print("✓ Connection successful!")
    print(f"  Sample models: {[m.name for m in models]}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Test 2: Check if codeplugtech/face-swap model exists
print("\n[Test 2] Checking codeplugtech/face-swap model...")
try:
    model = replicate.models.get("codeplugtech/face-swap")
    print(f"✓ Model found: {model.name}")
    print(f"  Latest version: {model.latest_version.id[:12]}...")
except Exception as e:
    print(f"✗ Model not found or error: {e}")
    print("\n[INFO] Trying alternative models...")
    
    # Try to find available face swap models
    try:
        print("\n[Test 3] Searching for alternative face swap models...")
        # Try some known face swap models
        alternatives = [
            "lucataco/faceswap",
            "omniedgeio/face-swap",
            "yan-ops/face_swap",
            "lucataco/ip_adapter-face-inpaint"
        ]
        
        for alt in alternatives:
            try:
                alt_model = replicate.models.get(alt)
                print(f"✓ Found alternative: {alt}")
                print(f"  Version: {alt_model.latest_version.id[:12]}...")
            except:
                print(f"✗ Not available: {alt}")
                
    except Exception as e2:
        print(f"✗ Search failed: {e2}")

# Test 3: Try to create a prediction with the model
print("\n[Test 4] Testing prediction creation...")
try:
    model = replicate.models.get("codeplugtech/face-swap")
    version = model.latest_version
    
    # Use dummy URLs for testing
    test_input = {
        "SourceImage": "https://replicate.delivery/pbxt/KpcCJMqvLQzBJ0bJnWLO7DxOqOGQIjzPGlqWOLlqzLlKLLQE/output.png",
        "TargetImage": "https://replicate.delivery/pbxt/KpcCJMqvLQzBJ0bJnWLO7DxOqOGQIjzPGlqWOLlqzLlKLLQE/output.png"
    }
    
    prediction = replicate.predictions.create(
        version=version.id,
        input=test_input
    )
    
    print(f"✓ Prediction created: {prediction.id}")
    print(f"  Status: {prediction.status}")
    
except Exception as e:
    print(f"✗ Prediction creation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Test Complete")
print("="*60)
