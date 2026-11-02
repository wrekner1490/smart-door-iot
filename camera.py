import cv2
import time
import config

def capture_visitor_photo(save_path=config.VISITOR_IMAGE_PATH):
    print("[INFO] Initializing webcam...")
    # Try index 0 first, fallback to index 1
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[WARNING] Could not open camera at index 0. Trying index 1...")
        cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("[ERROR] Failed to open any camera. Cannot capture photo.")
        return None

    try:
        # Warm up camera for 10 frames to allow auto-exposure/white-balance to adjust
        for _ in range(10):
            ret, frame = cap.read()
            time.sleep(0.05)
            
        # Capture final frame
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path, frame)
            print(f"[INFO] Visitor detected — photo captured at {save_path}")
            return save_path
        else:
            print("[ERROR] Failed to capture a frame from the camera.")
            return None
    except Exception as e:
        print(f"[ERROR] Exception during photo capture: {e}")
        return None
    finally:
        cap.release()
