"""
Replicate API Helper Module - IP-Adapter Face Inpaint
Handles face blending using lucataco/ip_adapter-face-inpaint model.
"""

import replicate
import os
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Replicate API
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
if REPLICATE_API_TOKEN:
    os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN


# Character style mapping for SDXL IP-Adapter FaceID
CHARACTER_STYLES = {
    'superman': {
        'prompt': '''Preserve the superhero's original head shape, jawline, skull structure,
hair, hairstyle, costume, pose, and lighting exactly as in the base image.

Subtly blend the child's facial characteristics into the face,
including eyes, eyebrows, nose, mouth, and expression.

Child face, young facial proportions, soft facial features.

No face swap. No replacement of head shape. Maintain superhero identity.

Photorealistic. Cinematic lighting. Clean studio background. High detail.''',
        
        'negative_prompt': '''face swap, different jawline, different hair, adult face, aging,
distorted face, cartoon, anime, exaggerated features, deformed,
brown costume, gray costume, desaturated colors, muted colors''',
        
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1768395277/templates/superman_template_vibrant_v4.png'
    },
    'batman': {
        'prompt': '''Preserve the superhero's original head shape, jawline, skull structure,
hair, hairstyle, costume, pose, and lighting exactly as in the base image.

Subtly blend the child's facial characteristics into the face,
including eyes, eyebrows, nose, mouth, and expression.

Child face, young facial proportions, soft facial features.

No face swap. No replacement of head shape. Maintain superhero identity.

Photorealistic. Cinematic lighting. Clean studio background. High detail.''',
        
        'negative_prompt': '''face swap, different jawline, different hair, adult face, aging,
distorted face, cartoon, anime, exaggerated features, deformed''',
        
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1768659434/templates/batman_template_backend.jpg'
    },
    'spiderman': {
        'prompt': '''Preserve the superhero's original head shape, jawline, skull structure,
hair, hairstyle, costume, pose, and lighting exactly as in the base image.

Subtly blend the child's facial characteristics into the face,
including eyes, eyebrows, nose, mouth, and expression.

Child face, young facial proportions, soft facial features.

No face swap. No replacement of head shape. Maintain superhero identity.

Photorealistic. Cinematic lighting. Clean studio background. High detail.''',
        
        'negative_prompt': '''face swap, different jawline, different hair, adult face, aging,
distorted face, cartoon, anime, exaggerated features, deformed''',
        
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1768659435/templates/spiderman_template_backend.jpg'
    },
    'wonderwoman': {
        'prompt': '''Preserve the superhero's original head shape, jawline, skull structure,
hair, hairstyle, costume, pose, and lighting exactly as in the base image.

Subtly blend the child's facial characteristics into the face,
including eyes, eyebrows, nose, mouth, and expression.

Child face, young facial proportions, soft facial features.

No face swap. No replacement of head shape. Maintain superhero identity.

Photorealistic. Cinematic lighting. Clean studio background. High detail.''',
        
        'negative_prompt': '''face swap, different jawline, different hair, adult face, aging,
distorted face, cartoon, anime, exaggerated features, deformed''',
        
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1768659435/templates/wonderwoman_template_backend.jpg'
    },
    'ironman': {
        'prompt': '''Preserve the superhero's original head shape, jawline, skull structure,
hair, hairstyle, costume, pose, and lighting exactly as in the base image.

Subtly blend the child's facial characteristics into the face,
including eyes, eyebrows, nose, mouth, and expression.

Child face, young facial proportions, soft facial features.

No face swap. No replacement of head shape. Maintain superhero identity.

Photorealistic. Cinematic lighting. Clean studio background. High detail.''',
        
        'negative_prompt': '''face swap, different jawline, different hair, adult face, aging,
distorted face, cartoon, anime, exaggerated features, deformed''',
        
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1768659436/templates/ironman_template_backend.jpg'
    },
    'captainamerica': {
        'prompt': '''Preserve the superhero's original head shape, jawline, skull structure,
hair, hairstyle, costume, pose, and lighting exactly as in the base image.

Subtly blend the child's facial characteristics into the face,
including eyes, eyebrows, nose, mouth, and expression.

Child face, young facial proportions, soft facial features.

No face swap. No replacement of head shape. Maintain superhero identity.

Photorealistic. Cinematic lighting. Clean studio background. High detail.''',
        
        'negative_prompt': '''face swap, different jawline, different hair, adult face, aging,
distorted face, cartoon, anime, exaggerated features, deformed''',
        
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1768659437/templates/captainamerica_template_backend.jpg'
    },
    'saudi_central_male': {
        'prompt': 'Saudi man wearing traditional bisht and thobe, photorealistic, cinematic lighting',
        'negative_prompt': 'cartoon, drawing, anime, low quality',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/templates/saudi_central_male_v7.png'
    },
    'saudi_traditional_daglah': {
        'prompt': 'Saudi man wearing traditional daglah with golden embroidered patterns and black bandolier, white shemagh with black agal, photorealistic, cinematic lighting, traditional Saudi heritage setting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1770104351/templates/saudi_traditional_daglah.jpg'
    },
    'jeddah_young_character_1770485845273': {
        'prompt': 'Young Saudi man wearing white bisht over black thobe, white shemagh with gold-striped agal, black goatee, Jeddah cityscape background, photorealistic, professional photography, natural lighting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing, old man, elderly',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1770486929/templates/jeddah_young_white_bisht.jpg'
    },
    'jeddah_character_updated_1770487272655': {
        'prompt': 'Young Saudi man wearing white bisht over black thobe, white shemagh with gold-striped agal, clean-shaven face with very light mustache, Jeddah cityscape background, photorealistic, professional photography, natural lighting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing, old man, elderly, goatee, beard, heavy mustache',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1770487272/templates/jeddah_character_updated.jpg'
    },
    'daglah_child_character_1770488439465': {
        'prompt': 'Saudi Arabian boy child aged 8-12 years old wearing traditional daglah with golden embroidery and black bandolier, white shemagh with black agal, child face, young boy, photorealistic, professional photography, natural lighting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing, adult, teenager, facial hair, beard, mustache',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1770488439/templates/daglah_child_character.jpg'
    },
    'sharqawi_dress_character_1770578762613': {
        'prompt': 'Saudi Arabian woman wearing traditional Eastern Province (Sharqiyah) black dress with intricate gold embroidery, black hijab with gold trim, elegant appearance, photorealistic, professional photography, natural lighting, traditional Saudi heritage setting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing, niqab',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/v1770578762/templates/sharqawi_dress_character.jpg'
    },
    'jeddah_character_updated_1770660835227': {
        'prompt': 'Fit athletic Saudi Arabian man wearing traditional white bisht over black thobe, white shemagh with gold-striped agal, well-groomed full light beard with mustache, natural neutral expression, historical Saudi heritage architecture background (old Jeddah Al-Balad style), photorealistic, professional photography, natural lighting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing, smile, goatee only, clean shaven',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/templates/jeddah_updated_v2.jpg'
    },
    'northern_woman_v1_1770658383334': {
        'prompt': 'Saudi Arabian woman wearing traditional Northern Saudi dress with burgundy/maroon embroidered vest featuring vertical striped patterns and gold coin necklace decorations, black hijab with burgundy and gold coin headband, black waist sash, elegant appearance, photorealistic, professional photography, natural lighting, traditional Saudi heritage setting',
        'negative_prompt': 'cartoon, drawing, anime, low quality, modern clothing, western clothing, niqab',
        'template_image': 'https://res.cloudinary.com/dfcqp8igu/image/upload/templates/northern_woman_v1.jpg'
    },
}


def start_face_generation(
    child_image_url: str,
    mask_image_url: str,
    character: str = 'superman'
) -> Optional[Dict[str, Any]]:
    """
    Start face swap using yan-ops/face_swap model.
    
    Args:
        child_image_url: URL of child's photo (source face)
        mask_image_url: URL of face mask image (not used by this model)
        character: Character name
        
    Returns:
        Dict with prediction_id and status, or None if failed
    """
    try:
        print(f"[Replicate] Starting Face Swap for character: {character}", flush=True)
        print(f"[Replicate] Child/Source image: {child_image_url[:50]}...", flush=True)
        
        # Get character-specific settings
        style_config = CHARACTER_STYLES.get(character.lower(), CHARACTER_STYLES['superman'])
        
        # Get template image URL (target face)
        template_url = style_config.get('template_image')
        if not template_url:
            print(f"[Replicate] ERROR: No template image for character: {character}", flush=True)
            return None
        
        print(f"[Replicate] Template/Target: {template_url[:50]}...", flush=True)
        
        # Use yan-ops/face_swap - true face swapping with weight control
        # Model expects: source_image (face to swap FROM) and target_image (image to swap TO)
        input_params = {
            "source_image": child_image_url,    # The user's face to swap FROM
            "target_image": template_url,       # The character template to swap TO
            "weight": 1.0                       # Complete swap (1.0 = 100%, 0.5 = blend)
        }
        
        print(f"[Replicate] Using yan-ops/face_swap model", flush=True)
        print(f"  Source (child): {child_image_url[:50]}...", flush=True)
        print(f"  Target (template): {template_url[:50]}...", flush=True)
        print(f"  Weight: 1.0 (complete swap, no blending)", flush=True)
        
        # Use yan-ops/face_swap model (true face swapping)
        model_name = "yan-ops/face_swap"
        
        print(f"[Replicate] Getting model version...", flush=True)
        model = replicate.models.get(model_name)
        version = model.latest_version
        
        print(f"[Replicate] Sending request to {model_name} (version: {version.id[:12]}...)", flush=True)
        
        # Create prediction using VERSION (not model name)
        prediction = replicate.predictions.create(
            version=version.id,
            input=input_params
        )
        
        prediction_id = prediction.id
        print(f"[Replicate] Prediction started: {prediction_id}", flush=True)
        
        return {
            'prediction_id': prediction_id,
            'status': prediction.status,
            'created_at': time.time()
        }
        
    except Exception as e:
        print(f"[Replicate] Failed to start prediction: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        return None


def check_prediction_status(prediction_id: str) -> Optional[Dict[str, Any]]:
    """
    Check the status of a face generation prediction.
    
    Args:
        prediction_id: The prediction ID from start_face_generation
        
    Returns:
        Dict with status and result URL if complete, None if failed
    """
    try:
        # Check status via API
        prediction = replicate.predictions.get(prediction_id)
        
        status = prediction.status
        
        result = {
            'prediction_id': prediction_id,
            'status': status,
        }
        
        if status == 'succeeded':
            output = prediction.output
            print(f"[Replicate] Raw output type: {type(output).__name__}", flush=True)
            print(f"[Replicate] Raw output value: {output}", flush=True)
            
            if output:
                # yan-ops/face_swap returns a dictionary with 'cache_url' and 'msg'
                # Other models might return a URL string or list of URLs
                if isinstance(output, dict):
                    # Dictionary format: {'cache_url': 'https://...', 'msg': 'succeed'}
                    # Try multiple possible key names
                    result_url = (output.get('cache_url') or 
                                output.get('url') or 
                                output.get('output_url') or
                                output.get('image') or
                                output.get('result'))
                    if not result_url:
                        print(f"[Replicate] ERROR: No URL found in output dict. Keys: {list(output.keys())}", flush=True)
                        print(f"[Replicate] Full output: {output}", flush=True)
                        result_url = None
                    else:
                        print(f"[Replicate] Extracted URL from dict: {result_url}", flush=True)
                elif isinstance(output, list):
                    # List format: ['https://...']
                    result_url = output[0] if output else None
                    print(f"[Replicate] Extracted URL from list: {result_url}", flush=True)
                else:
                    # String format: 'https://...'
                    result_url = output
                    print(f"[Replicate] URL is string: {result_url}", flush=True)
                
                if result_url:
                    result['result_url'] = result_url
                    print(f"[Replicate] ✓ Result URL ready: {result_url[:50]}...", flush=True)
                else:
                    print(f"[Replicate] ✗ ERROR: Could not extract URL from output", flush=True)
                
        elif status == 'failed':
            result['error'] = prediction.error
            print(f"[Replicate] Prediction failed: {prediction.error}", flush=True)
            
        return result
        
    except Exception as e:
        print(f"[Replicate] Failed to check status: {str(e)}", flush=True)
        return None


def test_connection() -> bool:
    """
    Test Replicate API connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        # Try to list models (requires valid API token)
        models = replicate.models.list()
        print("[Replicate] Connection successful!", flush=True)
        return True
    except Exception as e:
        print(f"[Replicate] Connection failed: {str(e)}", flush=True)
        print("[Replicate] Please check REPLICATE_API_TOKEN in .env file", flush=True)
        return False


if __name__ == "__main__":
    # Test the connection
    print("Testing Replicate connection...")
    test_connection()
