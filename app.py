from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
import base64
from dotenv import load_dotenv

# Import our helper modules
import cloudinary_helper
import replicate_helper

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Disable output buffering
os.environ['PYTHONUNBUFFERED'] = '1'

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Store active predictions in memory (for polling)
active_predictions = {}


@app.before_request
def log_request_info():
    """Log details of every incoming request"""
    try:
        if request.path != '/health':
            print(f"\n[REQUEST] {request.method} {request.path}", flush=True)
            if request.content_length:
                print(f"[REQUEST] Content Length: {request.content_length} bytes", flush=True)
    except Exception as e:
        print(f"[ERROR] Error in before_request: {e}", flush=True)


@app.errorhandler(Exception)
def handle_exception(e):
    """Global error handler for all unhandled exceptions"""
    print(f"\n[CRITICAL ERROR] Unhandled Exception: {str(e)}", flush=True)
    import traceback
    tb = traceback.format_exc()
    print(tb, flush=True)
    
    # Save to file immediately
    try:
        with open('crash_log.txt', 'a', encoding='utf-8') as f:
            from datetime import datetime
            f.write(f"\n{'='*60}\n")
            f.write(f"TIME: {datetime.now()}\n")
            f.write(f"PATH: {request.path}\n")
            f.write(f"ERROR: {str(e)}\n")
            f.write(f"TRACEBACK:\n{tb}\n")
    except:
        pass
        
    return jsonify({'error': f'Server Error: {str(e)}'}), 500


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/swap-face', methods=['POST'])
def swap_face():
    """
    Start face swap process:
    1. Upload child photo to Cloudinary
    2. Generate face mask (for compatibility, not used by current model)
    3. Upload mask to Cloudinary
    4. Start Replicate prediction with lucataco/faceswap
    5. Return prediction ID for polling
    """
    print("=" * 60, flush=True)
    print("FACE SWAP REQUEST RECEIVED", flush=True)
    print("=" * 60, flush=True)
    
    try:
        data = request.get_json()
        
        if not data or 'child_photo' not in data or 'character' not in data:
            print("[ERROR] Missing required fields", flush=True)
            return jsonify({'error': 'Missing required fields: child_photo and character'}), 400
        
        # Decode child photo from base64
        child_photo_b64 = data['child_photo'].split(',')[1]  # Remove data:image/png;base64,
        child_image_bytes = base64.b64decode(child_photo_b64)
        character = data['character']
        
        print(f"[INFO] Character: {character}", flush=True)
        print(f"[INFO] Image size: {len(child_image_bytes)} bytes", flush=True)
        
        # Step 1: Upload child photo to Cloudinary
        print("[STEP 1] Uploading child photo to Cloudinary...", flush=True)
        upload_result = cloudinary_helper.upload_temp_image(child_image_bytes)
        
        if not upload_result:
            return jsonify({'error': 'Failed to upload image to cloud storage'}), 500
        
        child_image_url = upload_result['url']
        child_public_id = upload_result['public_id']
        
        print(f"[SUCCESS] Child image uploaded: {child_image_url[:50]}...", flush=True)
        
        # Step 2: Generate face mask
        print("[STEP 2] Generating face mask...", flush=True)
        from face_mask_generator import get_mask_generator
        mask_bytes = None
        try:
            mask_generator = get_mask_generator()
            mask_bytes = mask_generator.generate_mask(child_image_bytes)
            if not mask_bytes:
                print("[WARNING] Face mask generation failed (no face detected). Proceeding without mask...", flush=True)
        except Exception as mask_err:
            print(f"[WARNING] Mask generation error: {mask_err}. Proceeding without mask...", flush=True)
        
        # Step 3: Upload mask to Cloudinary (if generated)
        mask_image_url = ""
        mask_public_id = ""
        
        if mask_bytes:
            print("[STEP 3] Uploading mask to Cloudinary...", flush=True)
            mask_upload_result = cloudinary_helper.upload_temp_image(mask_bytes)
            
            if mask_upload_result:
                mask_image_url = mask_upload_result['url']
                mask_public_id = mask_upload_result['public_id']
                print(f"[SUCCESS] Mask uploaded: {mask_image_url[:50]}...", flush=True)
            else:
                print("[WARNING] Mask upload failed. Proceeding without mask...", flush=True)
        else:
            print("[INFO] Skipping mask upload (no mask available)", flush=True)
        
        # Step 4: Start Replicate prediction with SDXL IP-Adapter FaceID
        print("[STEP 4] Starting AI face blending...", flush=True)
        prediction_info = replicate_helper.start_face_generation(
            child_image_url=child_image_url,
            mask_image_url=mask_image_url,
            character=character
        )
        
        if not prediction_info:
            # Cleanup uploaded images
            cloudinary_helper.delete_temp_image(child_public_id)
            cloudinary_helper.delete_temp_image(mask_public_id)
            return jsonify({'error': 'Failed to start AI processing'}), 500
        
        prediction_id = prediction_info['prediction_id']
        
        # Store prediction info for cleanup later
        active_predictions[prediction_id] = {
            'child_cloudinary_id': child_public_id,
            'mask_cloudinary_id': mask_public_id,
            'character': character,
            'status': 'processing'
        }
        
        print(f"[SUCCESS] Prediction started: {prediction_id}", flush=True)
        print("=" * 60, flush=True)
        
        return jsonify({
            'prediction_id': prediction_id,
            'status': 'processing',
            'message': 'Face blending started. Poll /check-status to get updates.'
        })
        
    except Exception as e:
        print(f"[ERROR] Exception in swap_face: {str(e)}", flush=True)
        import traceback
        tb_str = traceback.format_exc()
        print(tb_str, flush=True)
        
        # Also write to error log file
        with open('error_log.txt', 'a') as f:
            from datetime import datetime
            f.write(f"\n{'='*50}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Error: {str(e)}\n")
            f.write(f"Traceback:\n{tb_str}\n")
        
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/check-status/<prediction_id>', methods=['GET'])
def check_status(prediction_id):
    """
    Check the status of a face generation prediction.
    In sync mode, results are returned immediately.
    """
    try:
        print(f"[POLL] Checking status for: {prediction_id}", flush=True)
        
        if prediction_id not in active_predictions:
            return jsonify({'error': 'Prediction not found'}), 404
        
        # Check Replicate status
        status_info = replicate_helper.check_prediction_status(prediction_id)
        
        if not status_info:
            return jsonify({'error': 'Failed to check prediction status'}), 500
        
        status = status_info['status']
        prediction_data = active_predictions[prediction_id]
        
        # Update stored status
        prediction_data['status'] = status
        
        if status == 'succeeded':
            print(f"[SUCCESS] Prediction completed: {prediction_id}", flush=True)
            result_url = status_info.get('result_url')
            
            # Validate that we have a result URL
            if not result_url:
                print(f"[ERROR] No result URL in status_info: {status_info}", flush=True)
                return jsonify({
                    'error': 'Failed to generate result - no output URL received from AI model'
                }), 500
            
            print(f"[SUCCESS] Result URL: {result_url}", flush=True)
            
            # Cleanup Cloudinary images (both child and mask)
            child_id = prediction_data.get('child_cloudinary_id')
            mask_id = prediction_data.get('mask_cloudinary_id')
            
            if child_id:
                print(f"[CLEANUP] Deleting child image...", flush=True)
                cloudinary_helper.delete_temp_image(child_id)
            
            if mask_id:
                print(f"[CLEANUP] Deleting mask image...", flush=True)
                cloudinary_helper.delete_temp_image(mask_id)
            
            # Remove from active predictions
            del active_predictions[prediction_id]
            
            return jsonify({
                'status': 'succeeded',
                'result_url': result_url
            })
        
        elif status == 'failed':
            print(f"[FAILED] Prediction failed: {prediction_id}", flush=True)
            error_msg = status_info.get('error', 'Unknown error')
            
            # Cleanup
            child_id = prediction_data.get('child_cloudinary_id')
            mask_id = prediction_data.get('mask_cloudinary_id')
            
            if child_id:
                cloudinary_helper.delete_temp_image(child_id)
            
            if mask_id:
                cloudinary_helper.delete_temp_image(mask_id)
            
            del active_predictions[prediction_id]
            
            return jsonify({
                'status': 'failed',
                'error': error_msg
            })
        
        else:
            # Shouldn't happen in sync mode, but handle it
            return jsonify({
                'status': status
            })
        
    except Exception as e:
        print(f"[ERROR] Exception in check_status: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'cloudinary': 'configured' if os.getenv('CLOUDINARY_API_KEY') else 'not configured',
        'replicate': 'configured' if os.getenv('REPLICATE_API_TOKEN') else 'not configured'
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SUPERHERO PHOTO BOOTH - IP-Adapter Face Inpaint")
    print("=" * 60)
    print("Using:")
    print("  - Cloudinary for temporary image storage")
    print("  - OpenCV for face detection")
    print("  - Replicate lucataco/ip_adapter-face-inpaint")
    print("  - Face masking for structure preservation")
    print("=" * 60)
    print("Server starting at: http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
