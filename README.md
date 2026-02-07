# Photo Booth Face Swap Application

A web-based photo booth application that captures live photos via camera, swaps faces with superhero characters using AI, and enables printing.

## Features

- 📸 **Live Camera Preview** - Real-time camera feed with WebRTC
- 🦸 **Character Selection** - Choose from Superman, Batman, Spider-Man, Wonder Woman
- ✨ **AI Face Swap** - Powered by Hugging Face API (free tier)
- 🖨️ **Print Functionality** - Print your superhero transformation
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Create `.env` file for API configuration:
```bash
cp .env.example .env
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Allow camera permissions when prompted

4. Follow the on-screen instructions:
   - Position yourself in the camera
   - Click "Capture Photo"
   - Select a superhero character
   - Wait for processing
   - Print or retake!

## Requirements

- Python 3.8+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Camera/webcam access
- Internet connection (for AI processing)

## API Usage

The application uses Hugging Face's free inference API:
- **Free tier**: 30,000 requests/month
- **Perfect for**: 10-15 devices with moderate usage
- **No GPU required** on your server

## Project Structure

```
KHAL/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main HTML interface
├── static/
│   ├── style.css         # CSS styling
│   ├── app.js            # JavaScript logic
│   └── characters/       # Superhero character images
│       ├── superman.png
│       ├── batman.png
│       ├── spiderman.png
│       └── wonderwoman.png
└── README.md             # This file
```

## Deployment

For production deployment:
1. Use a production WSGI server (gunicorn, waitress)
2. Set `FLASK_ENV=production` in `.env`
3. Configure HTTPS for camera access
4. Use a reverse proxy (nginx, Apache)

## License

MIT License - Feel free to use and modify!
