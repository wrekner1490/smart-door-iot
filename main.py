import time
import serial
import base64
import requests
import os
import config
from camera import capture_visitor_photo
import blynk_api

def upload_image_to_imgur(image_path):
    print("[INFO] Uploading photo to Imgur...")
    fallback_url = "https://i.imgur.com/placeholder.png"
    
    if not os.path.exists(image_path):
        print(f"[ERROR] Image file not found at {image_path}")
        return fallback_url
        
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
        url = "https://api.imgur.com/3/image"
        payload = {'image': encoded_string}
        headers = {
            'Authorization': f'Client-ID {config.IMGUR_CLIENT_ID}'
        }
        
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('success'):
            imgur_url = data['data']['link']
            print(f"[INFO] Photo uploaded: {imgur_url}")
            return imgur_url
        else:
            print(f"[ERROR] Imgur API returned failure: {data}")
            return fallback_url
            
    except Exception as e:
        print(f"[ERROR] Failed to upload image to Imgur: {e}")
        return fallback_url

def main():
    print("[INFO] Starting Smart Visitor Door System...")
    
    try:
        ser = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=1)
        print(f"[INFO] Connected to NodeMCU on {config.SERIAL_PORT} at {config.BAUD_RATE} baud.")
        time.sleep(2) # Give NodeMCU time to reset after serial connect
    except Exception as e:
        print(f"[ERROR] Could not open serial port {config.SERIAL_PORT}: {e}")
        return
        
    print("[INFO] Listening for visitors...")
    
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line == "PERSON_DETECTED":
                    print("\n[INFO] --------------------------------------------------")
                    print("[INFO] PERSON_DETECTED signal received from NodeMCU.")
                    
                    # 1. Capture photo
                    image_path = capture_visitor_photo()
                    
                    # 2. Upload to Imgur
                    imgur_url = "https://i.imgur.com/placeholder.png"
                    if image_path:
                        imgur_url = upload_image_to_imgur(image_path)
                        
                    # 3. Push to Blynk
                    blynk_api.send_notification("Someone is at your door! Check the Blynk app.")
                    blynk_api.set_virtual_pin("V5", imgur_url)
                    blynk_api.reset_decision_pins()
                    
                    print("[INFO] Owner notified via Blynk — waiting for decision...")
                    
                    # 4. Poll Blynk for owner decision
                    start_time = time.time()
                    decision = None
                    
                    while (time.time() - start_time) < config.DECISION_TIMEOUT:
                        v1_val = blynk_api.get_virtual_pin("V1") # ALLOW
                        v2_val = blynk_api.get_virtual_pin("V2") # DENY
                        
                        if v1_val and '1' in v1_val:
                            decision = "ALLOW"
                            break
                        elif v2_val and '1' in v2_val:
                            decision = "DENY"
                            break
                            
                        time.sleep(config.POLL_INTERVAL)
                        
                    # 5. Act on decision
                    if decision == "ALLOW":
                        print("[INFO] Owner pressed ALLOW. Sending UNLOCK command...")
                        ser.write(b"UNLOCK\n")
                        print("[INFO] Door unlocked for 5 seconds.")
                    else:
                        if decision == "DENY":
                            print("[INFO] Owner pressed DENY. Sending LOCK command...")
                        else:
                            print("[INFO] Access denied / timed out. Sending LOCK command...")
                        ser.write(b"LOCK\n")
                        
                    # Wait briefly to let command transmit before resetting pins
                    time.sleep(0.5)
                    
                    # 6. Reset pins after decision/timeout
                    blynk_api.reset_decision_pins()
                    print("[INFO] Listening for visitors...")
                    
        except KeyboardInterrupt:
            print("\n[INFO] Exiting...")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error in main loop: {e}")
            time.sleep(1)
            
    if 'ser' in locals() and ser.is_open:
        ser.close()

if __name__ == "__main__":
    main()
