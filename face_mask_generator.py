"""
Face Mask Generator Module - Robust Version
Generates simple oval face masks without MediaPipe dependency.

Creates masks that:
- White (editable): center oval region for face
- Black (frozen): edges, jawline, hair
"""

import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

print("[FaceMask] Loading Robust Face Mask Generator v2.0", flush=True)

class FaceMaskGenerator:
    def __init__(self):
        """Initialize face detector"""
        # Use OpenCV's Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
    
    def generate_mask(self, image_bytes):
        """
        Generate face mask from image bytes - EXTREMELY DEFENSIVE IMPLEMENTATION
        """
        # 1. DEFINE VARIABLE FIRST
        image = None
        
        try:
            # 2. VALIDATE INPUT
            if not image_bytes:
                print("[FaceMask] Error: Empty image bytes", flush=True)
                return None
                
            # 3. DECODE IMAGE
            try:
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as decode_err:
                print(f"[FaceMask] Decode exception: {decode_err}", flush=True)
                return None
                
            # 4. CHECK DECODE RESULT
            if image is None:
                print("[FaceMask] Failed to decode image (result is None)", flush=True)
                return None
            
            # 5. FACE DETECTION
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = image.shape[:2]
            
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                print("[FaceMask] No face detected", flush=True)
                return None
            
            # 6. GENERATE MASK
            x, y, w, h = faces[0]
            mask = np.zeros((height, width), dtype=np.uint8)
            
            center_x = x + w // 2
            center_y = y + h // 2
            oval_width = int(w * 0.6)
            oval_height = int(h * 0.7)
            
            cv2.ellipse(
                mask,
                (center_x, center_y),
                (oval_width // 2, oval_height // 2),
                0, 0, 360, 255, -1
            )
            
            mask = cv2.GaussianBlur(mask, (51, 51), 0)
            mask_pil = Image.fromarray(mask)
            
            buffer = BytesIO()
            mask_pil.save(buffer, format='PNG')
            return buffer.getvalue()
            
        except Exception as e:
            print(f"[FaceMask] Unexpected error: {str(e)}", flush=True)
            import traceback
            traceback.print_exc()
            return None

    def generate_mask_from_base64(self, base64_image):
        try:
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]
            image_bytes = base64.b64decode(base64_image)
            return self.generate_mask(image_bytes)
        except Exception as e:
            print(f"[FaceMask] Base64 error: {e}", flush=True)
            return None

# Singleton instance
_mask_generator = None

def get_mask_generator():
    global _mask_generator
    if _mask_generator is None:
        _mask_generator = FaceMaskGenerator()
    return _mask_generator
