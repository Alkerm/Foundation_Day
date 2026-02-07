# Quick Setup Guide

## 🚀 Get Face Swapping Working in 3 Steps

### Step 1: Get a Free Hugging Face API Key

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: `photo-booth-app`
4. Select permission: **Read** (free tier)
5. Click "Generate"
6. Copy the token (starts with `hf_...`)

### Step 2: Configure the App

1. Create a `.env` file in the project folder:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` and add your token:
   ```
   HUGGINGFACE_API_KEY=hf_your_token_here
   ```

### Step 3: Run the App

```bash
python app.py
```

Open http://localhost:5000 and test!

---

## 📝 How It Works

The app now uses Hugging Face's Inference API with these fallback options:

1. **Primary**: Face swap models (if available)
2. **Fallback**: FLUX.1-schnell image generation
3. **Final fallback**: Returns character image

---

## ⚠️ Important Notes

- **Free tier**: Unlimited requests with rate limits
- **API key required**: HF router.huggingface.co requires authentication
- **Processing time**: 10-30 seconds per swap
- **Quality**: Depends on model availability

---

## 🔧 Troubleshooting

**"401 Unauthorized"**
→ Check your API key in `.env` file

**"503 Model Loading"**
→ Wait 20 seconds, the app will retry automatically

**"Face swap failed"**
→ App will fall back to image generation or character image

---

## 💡 Alternative: Use Replicate (Recommended for Production)

For better reliability and quality:
1. Sign up at https://replicate.com
2. Get API token
3. Update `.env`: `REPLICATE_API_TOKEN=your_token`
4. Cost: ~$0.01-0.05 per swap

Let me know if you want to switch to Replicate!
