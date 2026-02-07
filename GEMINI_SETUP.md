# Gemini API Setup Guide

## Step 1: Get Your Free Gemini API Key

1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

2. **Sign in**: Use your Google account to sign in

3. **Create API Key**:
   - Click **"Create API key"**
   - Select an existing Google Cloud project or create a new one
   - Copy your API key (it starts with `AIza...`)

4. **Important**: Keep your API key secure! Don't share it publicly.

## Step 2: Add API Key to Your Project

1. **Open the `.env` file** in your project folder (create it if it doesn't exist)

2. **Add your API key**:
   ```
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   ```

3. **Save the file**

## Step 3: Verify Setup

Run the verification script:
```bash
python verify_setup.py
```

This will test your Gemini API connection.

## Pricing Information

- **Free Tier**: 15 requests per minute, 1,500 requests per day
- **Perfect for testing** and small applications
- For production use, you may need to upgrade to a paid plan

## Troubleshooting

**Error: "API key not found"**
- Make sure you created the `.env` file in the correct directory
- Check that the API key is on a line starting with `GEMINI_API_KEY=`
- No quotes needed around the key

**Error: "Invalid API key"**
- Verify you copied the entire key from Google AI Studio
- Make sure there are no extra spaces before or after the key

**Error: "Quota exceeded"**
- You've hit the free tier limit (15 requests/minute)
- Wait a minute and try again
- Consider upgrading your plan if needed

## Need Help?

Visit the [Gemini API Documentation](https://ai.google.dev/docs) for more information.
