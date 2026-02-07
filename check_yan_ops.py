"""
Get detailed schema for yan-ops/face_swap model
"""
import replicate
import os
from dotenv import load_dotenv
import json

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

print("Checking yan-ops/face_swap model schema...")
print("="*60)

try:
    model = replicate.models.get("yan-ops/face_swap")
    version = model.latest_version
    
    print(f"Model: {model.name}")
    print(f"Version: {version.id}\n")
    
    # Get the input schema
    schema = version.openapi_schema
    
    # Save to file
    with open('yan_ops_schema.json', 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("Schema saved to yan_ops_schema.json\n")
    
    # Print input properties
    if 'components' in schema and 'schemas' in schema['components']:
        for schema_name, schema_def in schema['components']['schemas'].items():
            if 'Input' in schema_name:
                print(f"Input Schema: {schema_name}")
                if 'properties' in schema_def:
                    print("\nParameters:")
                    for prop_name, prop_def in schema_def['properties'].items():
                        prop_type = prop_def.get('type', 'unknown')
                        required = prop_name in schema_def.get('required', [])
                        default = prop_def.get('default', 'N/A')
                        desc = prop_def.get('description', '')
                        
                        print(f"\n  {prop_name}:")
                        print(f"    Type: {prop_type}")
                        print(f"    Required: {required}")
                        if default != 'N/A':
                            print(f"    Default: {default}")
                        if desc:
                            print(f"    Description: {desc}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
