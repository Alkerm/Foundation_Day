"""
Generate Female Saudi Character Images using Replicate SDXL
"""
import os
import replicate
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Replicate API
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
if REPLICATE_API_TOKEN:
    os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

def generate_character(prompt, filename):
    """Generate image using Replicate SDXL"""
    print(f"\n🎨 Generating: {filename}")
    print(f"Prompt: {prompt[:150]}...")
    
    try:
        # Use SDXL model for high-quality generation
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "negative_prompt": "cartoon, anime, drawing, illustration, low quality, blurry, distorted, deformed, ugly, unrealistic",
                "width": 1024,
                "height": 1024,
                "num_outputs": 1,
                "scheduler": "K_EULER",
                "num_inference_steps": 40,
                "guidance_scale": 7.5,
            }
        )
        
        # Output is a list of URLs
        if output and len(output) > 0:
            image_url = output[0]
            print(f"✅ Image generated successfully")
            
            # Download the image
            print(f"📥 Downloading image...")
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                output_path = f"static/characters/{filename}.jpg"
                
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"✅ Saved to: {output_path}")
                return True
            else:
                print(f"❌ Failed to download image")
                return False
        else:
            print(f"❌ No output from model")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("GENERATING FEMALE SAUDI CHARACTERS WITH REPLICATE SDXL")
    print("=" * 60)
    
    characters = [
        {
            'name': 'northern_woman_red_black',
            'prompt': '''Professional portrait photograph of a beautiful Saudi Arabian woman (25-35 years old) with an attractive, fit physique wearing a traditional Northern Saudi dress with a black base and a stunning red/burgundy embroidered vest with intricate geometric patterns and decorative trim. The dress shows her elegant figure and nice body proportions. She has beautiful facial features with warm expressive eyes, smooth skin, and a gentle smile. She wears a black hijab with red decorative trim. Traditional gold bracelets on her hands. The background shows authentic Saudi heritage village architecture with beige mud-brick walls, traditional wooden elements, and rustic textures - similar to historical Najd or Northern Saudi villages. Full body portrait, professional photography, photorealistic, culturally authentic, natural warm lighting, high detail, 4K quality.'''
        },
        {
            'name': 'sharqawi_woman_black_gold',
            'prompt': '''Professional portrait photograph of a beautiful young Saudi Arabian woman (20-30 years old) with an attractive, elegant physique wearing a traditional black Sharqawi dress. The dress features intricate gold embroidery patterns on the chest and sleeves, with a sheer black overlay adorned with gold trim, showing her graceful figure and nice body proportions. She has beautiful facial features with warm expressive eyes, smooth skin, and a gentle smile. She wears a black hijab with subtle gold embellishments. Traditional gold bracelets visible on her hands. The background shows traditional Saudi architecture with beige mud-brick walls and wooden elements. Full body portrait, professional photography, photorealistic, culturally authentic, natural lighting, high detail, 4K quality.'''
        }
    ]
    
    success_count = 0
    
    for char in characters:
        success = generate_character(char['prompt'], char['name'])
        
        if success:
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully generated {success_count}/{len(characters)} images")
    print("=" * 60)
    
    if success_count > 0:
        print("\n📋 Next steps:")
        print("1. Review the generated images in static/characters/")
        print("2. Upload to Cloudinary using upload_persistent.py")
        print("3. Update the frontend to include these characters")

if __name__ == "__main__":
    main()
