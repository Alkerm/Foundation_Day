# Replicate Instruct-Pix2Pix - Information Summary

## 📋 What You Need to Provide

### ✅ **Required Information**

1. **Superhero Template Image URL**
   - Format: Public URL (e.g., from Cloudinary)
   - Example: `https://res.cloudinary.com/.../superman.png`

2. **Character Name**
   - Type: String
   - Options: `'superman'`, `'batman'`, `'spiderman'`, `'wonderwoman'`, `'ironman'`

3. **Child's Photo URL** (Optional but recommended)
   - Format: Public URL
   - Example: `https://res.cloudinary.com/.../child.jpg`
   - Note: Referenced in the prompt for better results

4. **Replicate API Token**
   - You already have this in your `.env` file ✅
   - Format: `r8_...`

---

### 🔧 **Optional Parameters**

- **`image_guidance_scale`**: `1.0` to `2.0` (default: `1.5`)
  - Controls how much to preserve the original image
  - Higher = more preservation of superhero structure
  - Lower = more creative freedom

- **`guidance_scale`**: `7.0` to `15.0` (default: `7.5`)
  - Controls how strictly to follow the text instruction
  - Higher = follows prompt more strictly
  - Lower = more subtle changes

- **`num_inference_steps`**: `20` to `100` (default: `50`)
  - Quality vs speed tradeoff
  - Higher = better quality but slower
  - Lower = faster but lower quality

---

## 🎯 API Call Structure

### Method 1: Basic (Single Image + Prompt)
```python
from replicate_instruct_pix2pix import blend_with_instruct_pix2pix

result_url = blend_with_instruct_pix2pix(
    superhero_image_url='https://cloudinary.com/.../superman.png',
    character='superman',
    image_guidance_scale=1.5,
    guidance_scale=7.5,
    num_inference_steps=50
)
```

### Method 2: With Child Reference (Recommended)
```python
from replicate_instruct_pix2pix import blend_with_child_reference

result_url = blend_with_child_reference(
    superhero_image_url='https://cloudinary.com/.../superman.png',
    child_image_url='https://cloudinary.com/.../child.jpg',
    character='superman',
    image_guidance_scale=1.5,
    guidance_scale=7.5
)
```

---

## 🎨 How It Works

1. **Receives:**
   - Base image (superhero template)
   - Text instruction (character-specific blending prompt)
   - Optional: Child image URL referenced in prompt

2. **Processes:**
   - Analyzes the text instruction
   - Edits the image according to the prompt
   - Preserves structure based on `image_guidance_scale`

3. **Returns:**
   - URL to the edited/blended image
   - Valid for download immediately

---

## 💡 Key Differences from OpenAI

| Feature | Replicate Pix2Pix | OpenAI gpt-image-1 |
|---------|-------------------|-------------------|
| **Price** | ~$0.005-0.01/image | ~$0.02-0.08/image |
| **Input** | 1 image + prompt | 2 images + prompt |
| **Child Reference** | Via prompt text | Direct image input |
| **Quality** | Good | Excellent |
| **Your Credits** | ✅ Already have | Need to add |

---

## 📝 Example Prompts Used

### Superman:
```
Keep the superhero's jawline, skull shape, hair, and hairstyle unchanged.
Blend the child's facial characteristics (eyes, nose, mouth, cheeks, expression)
into the Superman face naturally.
No face swapping. No replacement of head shape.
Maintain the superhero's strong jawline and facial structure while reflecting 
the child's features.
Preserve the Superman costume, logo, and background completely.
High-quality, coherent lighting. Photorealistic result.

Reference the facial features from this child's photo: [CHILD_URL]
Extract the child's eyes, nose, mouth, and expression.
Blend these features naturally into the superhero's face.
```

---

## 💰 Pricing Comparison

- **Replicate Instruct-Pix2Pix**: ~$0.005-$0.01 per image
- **OpenAI gpt-image-1**: ~$0.02-$0.08 per image
- **Savings**: 2-8x cheaper on Replicate!

---

## 🚀 Quick Start

```python
# 1. Import the helper
from replicate_instruct_pix2pix import blend_with_child_reference

# 2. Call with your URLs
result_url = blend_with_child_reference(
    superhero_image_url='https://cloudinary.com/.../superman.png',
    child_image_url='https://cloudinary.com/.../child.jpg',
    character='superman'
)

# 3. Get the result
if result_url:
    print(f"Success! Image URL: {result_url}")
else:
    print("Failed to blend images")
```

---

## ⚙️ Parameter Tuning Tips

### For Better Preservation of Superhero:
```python
image_guidance_scale=1.8  # Higher preservation
guidance_scale=10.0       # Stricter instruction following
num_inference_steps=75    # Higher quality
```

### For More Creative Blending:
```python
image_guidance_scale=1.2  # More freedom
guidance_scale=7.0        # Looser instruction following
num_inference_steps=50    # Balanced quality
```

---

## 📚 Files Created

- **`replicate_instruct_pix2pix.py`** - Main helper module
- **`test_replicate_pix2pix.py`** - Test script with examples
- **`REPLICATE_PIX2PIX_INFO.md`** - This documentation

---

## ✅ Ready to Use!

Everything is set up. You already have:
- ✅ Replicate API token in `.env`
- ✅ Credits on Replicate
- ✅ Helper functions ready to use

Just call the functions with your image URLs and start blending! 🎨
