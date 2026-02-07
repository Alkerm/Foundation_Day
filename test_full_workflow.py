"""
Test the full face swap workflow
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API token
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Testing full face swap workflow...")
print("="*60)

# Test URLs (using Superman template from the code)
child_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"
template_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"

print(f"Source (child): {child_url[:50]}...")
print(f"Target (template): {template_url[:50]}...")
print()

try:
    # Step 1: Get the model
    print("[Step 1] Getting model...")
    model = replicate.models.get("codeplugtech/face-swap")
    print(f"✓ Model: {model.name}")
    
    # Step 2: Get latest version
    print("\n[Step 2] Getting latest version...")
    version = model.latest_version
    print(f"✓ Version: {version.id[:20]}...")
    
    # Step 3: Create prediction
    print("\n[Step 3] Creating prediction...")
    input_params = {
        "SourceImage": child_url,
        "TargetImage": template_url,
    }
    
    print(f"Input params: {input_params}")
    
    prediction = replicate.predictions.create(
        version=version.id,
        input=input_params
    )
    
    print(f"✓ Prediction created!")
    print(f"  ID: {prediction.id}")
    print(f"  Status: {prediction.status}")
    
    # Step 4: Wait for result (with timeout)
    print("\n[Step 4] Waiting for result...")
    import time
    max_wait = 60  # 60 seconds max
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        prediction = replicate.predictions.get(prediction.id)
        print(f"  Status: {prediction.status}")
        
        if prediction.status == "succeeded":
            print(f"\n✓ SUCCESS!")
            print(f"  Output: {prediction.output}")
            break
        elif prediction.status == "failed":
            print(f"\n✗ FAILED!")
            print(f"  Error: {prediction.error}")
            break
        
        time.sleep(2)
    
    if time.time() - start_time >= max_wait:
        print("\n⏱ Timeout reached")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Test complete")
