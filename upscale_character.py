"""
Upscale Character Image to 4K using Replicate Real-ESRGAN
"""
import replicate
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upscale_image_to_4k(image_path, output_filename):
    """
    Upscale an image to 4K resolution using Real-ESRGAN
    
    Args:
        image_path: Path to the input image
        output_filename: Name for the output file (without extension)
    """
    print(f"\n{'='*60}")
    print("UPSCALING IMAGE TO 4K")
    print(f"{'='*60}")
    print(f"Input: {image_path}")
    print(f"Output: static/characters/{output_filename}.png")
    
    try:
        # Open and upload the image
        print("\n[1/3] Reading image file...")
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print(f"✓ Image loaded ({len(image_data)} bytes)")
        
        # Run Real-ESRGAN upscaling
        print("\n[2/3] Upscaling with Real-ESRGAN (4x scale)...")
        print("This may take 30-60 seconds...")
        
        output = replicate.run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
            input={
                "image": open(image_path, 'rb'),
                "scale": 4,  # 4x upscaling for 4K quality
                "face_enhance": True  # Enhance facial features
            }
        )
        
        print("✓ Upscaling complete!")
        
        # Download the result
        print("\n[3/3] Downloading upscaled image...")
        
        # Output is a URL string
        if isinstance(output, str):
            result_url = output
        elif isinstance(output, list) and len(output) > 0:
            result_url = output[0]
        else:
            print(f"✗ Unexpected output format: {type(output)}")
            return False
        
        print(f"Result URL: {result_url[:50]}...")
        
        # Download the upscaled image
        response = requests.get(result_url)
        
        if response.status_code == 200:
            output_path = f"static/characters/{output_filename}.png"
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Saved to: {output_path}")
            print(f"\n{'='*60}")
            print("✅ UPSCALING COMPLETE!")
            print(f"{'='*60}")
            print(f"\nFile size: {len(response.content):,} bytes")
            print(f"Location: {output_path}")
            
            return True
        else:
            print(f"✗ Failed to download: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Upscale the character image
    # Replace this with the path to your image
    image_path = input("Enter the path to your image: ").strip('"').strip("'")
    output_name = input("Enter output filename (without extension): ").strip()
    
    if not output_name:
        output_name = "northern_character_4k"
    
    success = upscale_image_to_4k(image_path, output_name)
    
    if success:
        print("\n✅ Next steps:")
        print("1. Check the upscaled image in static/characters/")
        print("2. Upload to Cloudinary if needed")
        print("3. Add to the photo booth app")
    else:
        print("\n✗ Upscaling failed. Please check the error messages above.")
