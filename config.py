import os

SERIAL_PORT = "COM3"           # user sets this — /dev/ttyUSB0 on Linux/Mac
BAUD_RATE = 9600
BLYNK_AUTH_TOKEN = "YOUR_BLYNK_TOKEN_HERE"
BLYNK_SERVER = "https://blynk.cloud/external/api"
IMGUR_CLIENT_ID = "YOUR_IMGUR_CLIENT_ID_HERE"
POLL_INTERVAL = 2              # seconds between Blynk polls
DECISION_TIMEOUT = 30          # seconds to wait for owner response
UNLOCK_DURATION = 5            # seconds relay stays open

# Workspace base directory path properly joined
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISITOR_IMAGE_PATH = os.path.join(BASE_DIR, "visitor.jpg")
