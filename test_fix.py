"""
Test the fix with correct parameter names
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API token
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Testing with CORRECT parameter names...")
print("="*60)

# Test URLs
child_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"
template_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"

try:
    model = replicate.models.get("codeplugtech/face-swap")
    version = model.latest_version
    
    # CORRECT parameter names (snake_case)
    input_params = {
        "swap_image": child_url,      # Source face
        "input_image": template_url,  # Target template
    }
    
    print(f"Creating prediction with correct params:")
    print(f"  swap_image: {child_url[:50]}...")
    print(f"  input_image: {template_url[:50]}...")
    
    prediction = replicate.predictions.create(
        version=version.id,
        input=input_params
    )
    
    print(f"\n✓ SUCCESS! Prediction created!")
    print(f"  ID: {prediction.id}")
    print(f"  Status: {prediction.status}")
    
    # Wait briefly for result
    import time
    print("\nWaiting for result...")
    for i in range(15):
        time.sleep(2)
        prediction = replicate.predictions.get(prediction.id)
        print(f"  [{i*2}s] Status: {prediction.status}")
        
        if prediction.status == "succeeded":
            print(f"\n✓ COMPLETED!")
            print(f"  Result: {prediction.output}")
            break
        elif prediction.status == "failed":
            print(f"\n✗ FAILED!")
            print(f"  Error: {prediction.error}")
            break
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
