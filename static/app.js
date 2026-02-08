// State management
let currentScreen = 'camera';
let capturedPhoto = null;
let selectedCharacter = null;
let videoStream = null;

// DOM elements
const cameraScreen = document.getElementById('camera-screen');
const characterScreen = document.getElementById('character-screen');
const processingScreen = document.getElementById('processing-screen');
const resultScreen = document.getElementById('result-screen');

const cameraFeed = document.getElementById('camera-feed');
const photoCanvas = document.getElementById('photo-canvas');
const captureBtn = document.getElementById('capture-btn');
const cameraError = document.getElementById('camera-error');

const capturedPreview = document.getElementById('captured-preview');
const characterCards = document.querySelectorAll('.character-card');
const retakeBtn1 = document.getElementById('retake-btn-1');
const retakeBtn2 = document.getElementById('retake-btn-2');

const resultImage = document.getElementById('result-image');
const printBtn = document.getElementById('print-btn');

const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');

// Initialize camera on page load
window.addEventListener('DOMContentLoaded', () => {
    initCamera();
    setupEventListeners();
});

// Initialize camera
async function initCamera() {
    console.log('initCamera called');

    // Check if the origin is secure (Localhost or HTTPS)
    const isSecureOrigin = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    if (!isSecureOrigin) {
        console.warn('Camera may not work on non-secure origin:', location.origin);
        alert('⚠️ Camera access requires a secure connection (HTTPS or Localhost). Please check your browser address bar.');
    }

    try {
        // Try with more basic constraints first for better compatibility
        const constraints = {
            video: true
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);

        console.log('Camera stream obtained:', stream.id);
        videoStream = stream;
        cameraFeed.srcObject = stream;

        // Explicitly set muted again by code
        cameraFeed.muted = true;

        // Explicitly call play to handle browsers that block autoplay
        cameraFeed.onloadedmetadata = () => {
            console.log('Video metadata loaded, playing...');
            cameraFeed.play().catch(e => console.error('Error playing video:', e));
        };

        cameraError.style.display = 'none';
        captureBtn.disabled = false;

    } catch (error) {
        console.error('Camera access error:', error);
        cameraError.style.display = 'block';

        let errorMsg = '⚠️ Camera access denied. Please allow camera permissions and refresh.';
        if (error.name === 'NotAllowedError') {
            errorMsg = '⚠️ Camera access denied by user. Please enable it in browser settings and refresh.';
        } else if (error.name === 'NotFoundError') {
            errorMsg = '⚠️ No camera found on this device.';
        } else if (error.name === 'NotReadableError') {
            errorMsg = '⚠️ Camera is already in use by another application.';
        }

        cameraError.innerHTML = `<p>${errorMsg}</p>`;
        captureBtn.disabled = true;
    }
}

// Setup event listeners
function setupEventListeners() {
    // Capture photo
    captureBtn.addEventListener('click', capturePhoto);

    // Character selection
    characterCards.forEach(card => {
        card.addEventListener('click', () => selectCharacter(card));
    });

    // Retake buttons
    retakeBtn1.addEventListener('click', retakePhoto);
    retakeBtn2.addEventListener('click', retakePhoto);

    // Print button
    printBtn.addEventListener('click', printPhoto);

    // File upload
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
}

// Handle file upload fallback
function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (event) {
        capturedPhoto = event.target.result;
        capturedPreview.src = capturedPhoto;

        // Stop camera stream if active
        if (videoStream) {
            videoStream.getTracks().forEach(track => track.stop());
        }

        // Switch to character selection screen
        switchScreen('character');
    };
    reader.readAsDataURL(file);
}

// Capture photo from video stream
function capturePhoto() {
    const canvas = photoCanvas;
    const video = cameraFeed;

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to base64 (use PNG for maximum quality)
    capturedPhoto = canvas.toDataURL('image/png');

    // Show preview
    capturedPreview.src = capturedPhoto;

    // Stop camera stream
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }

    // Switch to character selection screen
    switchScreen('character');
}

// Select character
function selectCharacter(card) {
    // Remove previous selection
    characterCards.forEach(c => c.classList.remove('selected'));

    // Mark as selected
    card.classList.add('selected');
    selectedCharacter = card.dataset.character;

    // Start face swap process after short delay
    setTimeout(() => {
        performFaceSwap();
    }, 500);
}

// Perform face swap with polling
async function performFaceSwap() {
    console.log('performFaceSwap called');
    console.log('capturedPhoto:', capturedPhoto ? 'exists' : 'null');
    console.log('selectedCharacter:', selectedCharacter);

    if (!capturedPhoto || !selectedCharacter) {
        alert('Please capture a photo and select a character');
        return;
    }

    // Switch to processing screen
    switchScreen('processing');
    updateLoadingText('Uploading your photo...');

    try {
        // Step 1: Start face swap (upload to Cloudinary + start Replicate)
        console.log('Sending request to /swap-face...');
        const response = await fetch('/swap-face', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                child_photo: capturedPhoto,
                character: selectedCharacter
            })
        });

        console.log('Response received:', response.status);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Face swap failed');
        }

        const data = await response.json();
        const predictionId = data.prediction_id;
        console.log('Prediction ID:', predictionId);

        // Step 2: Poll for completion
        updateLoadingText('Creating your traditional photo...');
        const resultUrl = await pollForResult(predictionId);

        if (resultUrl) {
            // Display result
            resultImage.src = resultUrl;
            switchScreen('result');
        } else {
            throw new Error('Failed to generate result');
        }

    } catch (error) {
        console.error('Face swap error:', error);
        alert(`Sorry, something went wrong: ${error.message}\nPlease try again.`);
        switchScreen('character');
    }
}

// Poll for prediction result
async function pollForResult(predictionId, maxAttempts = 60) {
    let attempts = 0;

    while (attempts < maxAttempts) {
        try {
            const response = await fetch(`/check-status/${predictionId}`);

            if (!response.ok) {
                throw new Error('Failed to check status');
            }

            const data = await response.json();
            const status = data.status;

            console.log(`[Poll ${attempts + 1}] Status: ${status}`);

            if (status === 'succeeded') {
                console.log('Generation complete!');
                return data.result_url;
            } else if (status === 'failed') {
                throw new Error(data.error || 'Generation failed');
            }

            // Update loading text based on progress
            const elapsed = attempts * 2;
            if (elapsed < 10) {
                updateLoadingText('Starting AI processing...');
            } else if (elapsed < 20) {
                updateLoadingText('Analyzing your face...');
            } else {
                updateLoadingText('Almost done, creating your traditional photo...');
            }

            // Wait 2 seconds before next poll
            await new Promise(resolve => setTimeout(resolve, 2000));
            attempts++;

        } catch (error) {
            console.error('Polling error:', error);
            throw error;
        }
    }

    throw new Error('Timeout: Generation took too long');
}

// Update loading text
function updateLoadingText(text) {
    const loadingText = document.querySelector('.loading-text');
    if (loadingText) {
        loadingText.textContent = text;
    }
}

// Retake photo
function retakePhoto() {
    // Reset state
    capturedPhoto = null;
    selectedCharacter = null;

    // Remove character selections
    characterCards.forEach(c => c.classList.remove('selected'));

    // Restart camera
    initCamera();

    // Switch back to camera screen
    switchScreen('camera');
}

// Print photo
function printPhoto() {
    window.print();
}

// Switch between screens
function switchScreen(screen) {
    // Hide all screens
    cameraScreen.classList.remove('active');
    characterScreen.classList.remove('active');
    processingScreen.classList.remove('active');
    resultScreen.classList.remove('active');

    // Show selected screen
    switch (screen) {
        case 'camera':
            cameraScreen.classList.add('active');
            break;
        case 'character':
            characterScreen.classList.add('active');
            break;
        case 'processing':
            processingScreen.classList.add('active');
            break;
        case 'result':
            resultScreen.classList.add('active');
            break;
    }

    currentScreen = screen;
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }
});
