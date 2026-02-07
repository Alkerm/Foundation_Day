"""
Check the model's input schema and save to file
"""
import replicate
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configure API token
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

try:
    model = replicate.models.get("codeplugtech/face-swap")
    version = model.latest_version
    
    # Get the input schema
    schema = version.openapi_schema
    
    # Save to file
    with open('model_schema.json', 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("Schema saved to model_schema.json")
    
    # Also print the input properties if available
    if 'components' in schema and 'schemas' in schema['components']:
        for schema_name, schema_def in schema['components']['schemas'].items():
            if 'Input' in schema_name:
                print(f"\nFound Input Schema: {schema_name}")
                if 'properties' in schema_def:
                    print("Properties:")
                    for prop_name, prop_def in schema_def['properties'].items():
                        print(f"  - {prop_name}: {prop_def.get('type', 'unknown')}")
                        if 'description' in prop_def:
                            print(f"    Description: {prop_def['description']}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
