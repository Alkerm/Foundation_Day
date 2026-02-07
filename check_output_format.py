"""
Check the actual output format from yan-ops/face_swap
"""
import replicate
import os
from dotenv import load_dotenv
import json

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Checking yan-ops/face_swap output format...")
print("="*60)

# Use test URLs
child_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"
template_url = "https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png"

try:
    model = replicate.models.get("yan-ops/face_swap")
    version = model.latest_version
    
    prediction = replicate.predictions.create(
        version=version.id,
        input={
            "source_image": child_url,
            "target_image": template_url,
            "weight": 1.0
        }
    )
    
    print(f"Prediction created: {prediction.id}")
    print("Waiting for completion...")
    
    import time
    for i in range(30):
        time.sleep(2)
        prediction = replicate.predictions.get(prediction.id)
        
        if prediction.status == "succeeded":
            print(f"\n✓ Succeeded!")
            print(f"\nOutput type: {type(prediction.output)}")
            print(f"Output value: {prediction.output}")
            
            if isinstance(prediction.output, dict):
                print(f"\nOutput is a dictionary with keys: {list(prediction.output.keys())}")
                print(f"\nFull output:")
                print(json.dumps(prediction.output, indent=2))
            elif isinstance(prediction.output, list):
                print(f"\nOutput is a list with {len(prediction.output)} items")
                for idx, item in enumerate(prediction.output):
                    print(f"  [{idx}]: {item}")
            else:
                print(f"\nOutput is a string: {prediction.output}")
            
            break
        elif prediction.status == "failed":
            print(f"\n✗ Failed: {prediction.error}")
            break
        
        print(f"  [{i*2}s] Status: {prediction.status}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
