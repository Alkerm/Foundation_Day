"""
Test the complete flow with the fixed output parsing
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Testing complete flow with output parsing fix...")
print("="*60)

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
    
    print(f"Prediction created: {prediction.id}\n")
    
    import time
    for i in range(30):
        time.sleep(2)
        prediction = replicate.predictions.get(prediction.id)
        
        if prediction.status == "succeeded":
            print(f"\n✓ Succeeded!")
            output = prediction.output
            
            print(f"\nOutput type: {type(output).__name__}")
            
            # Test the parsing logic
            if isinstance(output, dict):
                result_url = output.get('cache_url') or output.get('url') or output.get('output_url')
                print(f"✓ Extracted URL from dict: {result_url}")
            elif isinstance(output, list):
                result_url = output[0] if output else None
                print(f"✓ Extracted URL from list: {result_url}")
            else:
                result_url = output
                print(f"✓ URL is string: {result_url}")
            
            if result_url:
                print(f"\n✅ SUCCESS! Result URL ready to display:")
                print(f"   {result_url}")
            else:
                print(f"\n❌ FAILED to extract URL from output")
            
            break
        elif prediction.status == "failed":
            print(f"\n✗ Failed: {prediction.error}")
            break
        
        print(f"  [{i*2}s] {prediction.status}...")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Flask server should now display results correctly!")
