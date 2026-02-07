"""
Test alternative face swap models on Replicate
"""
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Testing alternative face swap models...")
print("="*60)

# List of known face swap models to try
models_to_test = [
    "yan-ops/face_swap",
    "lucataco/faceswap",
    "omniedgeio/face-swap",
    "lucataco/face-swap",
    "xiankgx/face-swap",
    "cjwbw/roop",
    "pollinations/face-swap",
]

print("\nChecking which models are available:\n")

available_models = []

for model_name in models_to_test:
    try:
        model = replicate.models.get(model_name)
        version = model.latest_version
        print(f"✓ {model_name}")
        print(f"  Version: {version.id[:20]}...")
        
        # Try to get schema
        try:
            schema = version.openapi_schema
            if 'components' in schema and 'schemas' in schema['components']:
                for schema_name, schema_def in schema['components']['schemas'].items():
                    if 'Input' in schema_name and 'properties' in schema_def:
                        print(f"  Parameters: {list(schema_def['properties'].keys())}")
                        break
        except:
            pass
        
        available_models.append(model_name)
        print()
        
    except Exception as e:
        print(f"✗ {model_name} - Not available")

print("\n" + "="*60)
print(f"\nFound {len(available_models)} available models:")
for m in available_models:
    print(f"  - {m}")
