import requests
import config

def send_notification(message):
    try:
        url = f"{config.BLYNK_SERVER}/notify"
        params = {
            "token": config.BLYNK_AUTH_TOKEN,
            "body": message
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        print("[INFO] Blynk notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to send Blynk notification: {e}")

def set_virtual_pin(pin, value):
    try:
        url = f"{config.BLYNK_SERVER}/update"
        params = {
            "token": config.BLYNK_AUTH_TOKEN,
            pin: value
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        print(f"[INFO] Blynk pin {pin} updated.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to update Blynk pin {pin}: {e}")

def get_virtual_pin(pin):
    try:
        url = f"{config.BLYNK_SERVER}/get?token={config.BLYNK_AUTH_TOKEN}&{pin}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get Blynk pin {pin}: {e}")
        return None

def reset_decision_pins():
    print("[INFO] Resetting decision pins (V1, V2)...")
    set_virtual_pin("V1", 0)
    set_virtual_pin("V2", 0)
