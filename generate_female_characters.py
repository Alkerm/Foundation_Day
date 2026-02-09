"""
Generate Female Saudi Character Images using OpenAI DALL-E
Based on user-provided reference images
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import time

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_character_image(prompt, filename):
    """Generate image using DALL-E 3"""
    print(f"\n🎨 Generating: {filename}")
    print(f"Prompt: {prompt[:150]}...")
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        
        image_url = response.data[0].url
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
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("GENERATING FEMALE SAUDI CHARACTERS WITH DALL-E")
    print("=" * 60)
    
    characters = [
        {
            'name': 'sharqawi_woman_black_gold',
            'prompt': '''Professional portrait photograph of a beautiful young Saudi Arabian woman (20-30 years old) wearing an elegant traditional black Sharqawi dress. The dress features intricate gold embroidery patterns on the chest and sleeves, with a sheer black overlay adorned with gold trim. She wears a black hijab with subtle gold embellishments. She has a graceful presence with warm eyes. The background shows traditional Saudi architecture with beige mud-brick walls and wooden elements. Front-facing portrait, professional photography, photorealistic, culturally authentic.'''
        },
        {
            'name': 'northern_woman_red_black',
            'prompt': '''Professional portrait photograph of a Saudi Arabian woman (25-35 years old) wearing a traditional Northern Saudi dress with a black base and a stunning red/burgundy embroidered vest with intricate geometric patterns. She wears a black niqab with decorative red trim showing only her eyes. Traditional gold bracelets visible on her hands. The background shows authentic Saudi heritage architecture with beige walls. Front-facing portrait, professional photography, photorealistic, culturally authentic.'''
        }
    ]
    
    success_count = 0
    
    for char in characters:
        success = generate_character_image(char['prompt'], char['name'])
        
        if success:
            success_count += 1
        
        # Wait between requests to avoid rate limits
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully generated {success_count}/{len(characters)} images")
    print("=" * 60)
    
    if success_count > 0:
        print("\n📋 Next steps:")
        print("1. Review the generated images in static/characters/")
        print("2. Send the third reference dress image (if you have one)")
        print("3. Then we'll upload to Cloudinary and update the frontend")

if __name__ == "__main__":
    main()
