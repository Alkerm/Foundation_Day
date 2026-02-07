"""
Test yan-ops/face_swap model with weight=1.0 for complete face swap
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Testing yan-ops/face_swap with weight=1.0...")
print("="*60)

# Test URLs (using Superman template)
child_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"
template_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"

print(f"Source (child): {child_url[:50]}...")
print(f"Target (template): {template_url[:50]}...")
print()

try:
    # Get the model
    print("[Step 1] Getting model...")
    model = replicate.models.get("yan-ops/face_swap")
    version = model.latest_version
    print(f"✓ Model: {model.name}")
    print(f"✓ Version: {version.id[:20]}...")
    
    # Create prediction with weight=1.0 for complete swap
    print("\n[Step 2] Creating prediction with weight=1.0...")
    input_params = {
        "source_image": child_url,
        "target_image": template_url,
        "weight": 1.0  # Complete swap, no blending
    }
    
    print(f"Parameters: {input_params}")
    
    prediction = replicate.predictions.create(
        version=version.id,
        input=input_params
    )
    
    print(f"\n✓ Prediction created!")
    print(f"  ID: {prediction.id}")
    print(f"  Status: {prediction.status}")
    
    # Wait for result
    print("\n[Step 3] Waiting for result...")
    import time
    max_wait = 60
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        prediction = replicate.predictions.get(prediction.id)
        elapsed = int(time.time() - start_time)
        print(f"  [{elapsed}s] Status: {prediction.status}")
        
        if prediction.status == "succeeded":
            print(f"\n✓ SUCCESS!")
            print(f"  Result URL: {prediction.output}")
            print(f"\nThe face swap completed successfully with weight=1.0 (complete swap)")
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
print("Test complete - Flask server should auto-reload with changes")
print("Test the app at: http://localhost:5000")
