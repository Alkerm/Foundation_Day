# OpenAI Setup Guide

This guide will help you set up OpenAI's `gpt-image-1` model for face feature blending.

## 🔑 Step 1: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. **Important**: You need a paid account with credits to use the image editing API

## 💳 Step 2: Add Credits to Your Account

1. Go to [Billing](https://platform.openai.com/account/billing)
2. Add a payment method
3. Add credits (minimum $5 recommended)
4. Image editing costs approximately $0.02-0.08 per image

## 🔧 Step 3: Configure Your Environment

1. Open your `.env` file in the project directory
2. Add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. Save the file

## ✅ Step 4: Install Required Package

Make sure you have the OpenAI Python package installed:

```bash
pip install openai
```

## 🧪 Step 5: Test Your Connection

Run the test script:

```bash
python openai_helper.py
```

You should see:
```
Testing OpenAI connection...
[OpenAI] Connection successful!
[OpenAI] gpt-image-1 model is available!
```

## 📋 What Information You Need to Provide

When using the `gpt-image-1` model, you need:

### **Required:**
1. **Superhero Template Image** - Path or URL to your superhero base image
2. **Child's Photo** - Path or URL to the child's photo
3. **Character Name** - e.g., 'superman', 'batman', 'spiderman'

### **Optional:**
- **Output Format** - 'url' (default) or 'b64_json'
- **Size** - '1024x1024' (default), '1024x1792', or '1792x1024'

## 🎯 Example Usage

### Using Local Files:
```python
from openai_helper import blend_face_features

result = blend_face_features(
    superhero_image_path='./templates/superman.png',
    child_image_path='./uploads/child.jpg',
    character='superman',
    output_format='url'
)

if result:
    print(f"Result URL: {result['url']}")
```

### Using URLs (from Cloudinary):
```python
from openai_helper import blend_face_features_from_urls

result = blend_face_features_from_urls(
    superhero_url='https://res.cloudinary.com/.../superman.png',
    child_url='https://res.cloudinary.com/.../child.jpg',
    character='superman'
)

if result:
    print(f"Result URL: {result['url']}")
```

## 🎨 How It Works

The `gpt-image-1` model:
1. Takes your superhero template as the base image
2. Analyzes the child's facial features from the additional image
3. Blends the child's features (eyes, nose, mouth, expression) into the superhero face
4. **Preserves** the superhero's jawline, hair, body, costume, and background
5. Returns a photorealistic merged image

## 💡 Key Advantages

✅ **No face swap** - Preserves superhero structure  
✅ **Natural blending** - Seamless feature integration  
✅ **High quality** - Photorealistic results  
✅ **Simple API** - Just image + image + prompt  
✅ **No masking needed** - AI handles it automatically  

## 🚨 Troubleshooting

### "Authentication Error"
- Check your API key is correct in `.env`
- Make sure the key starts with `sk-`

### "Insufficient Credits"
- Add credits to your OpenAI account
- Check your balance at https://platform.openai.com/account/billing

### "Model not found"
- The `gpt-image-1` model may not be available in your region yet
- Contact OpenAI support for access

## 📚 API Reference

Full documentation: https://platform.openai.com/docs/guides/images

---

**Ready to use!** Your OpenAI helper is configured in `openai_helper.py`
