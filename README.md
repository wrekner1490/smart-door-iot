# Smart Door Visitor System (NodeMCU + Python)

An IoT smart-door setup. A NodeMCU microcontroller detects a visitor at the door
and signals a Python host over serial; the host captures a photo from a webcam,
uploads it, and sends a notification to the owner via Blynk, who can then approve
an unlock.

## Hardware

- NodeMCU (ESP8266/ESP32) running `nodemcu_door/nodemcu_door.ino`
- Door sensor / button + lock actuator wired to the NodeMCU
- Host PC with a webcam, connected to the NodeMCU over USB serial

## Software setup

```
pip install -r requirements.txt
```

`opencv-python`, `pyserial`, `requests`, `Pillow`

1. Flash `nodemcu_door/nodemcu_door.ino` to the board (Arduino IDE).
2. Copy your settings into `config.py`:
   - `SERIAL_PORT` (e.g. `COM3`, or `/dev/ttyUSB0`)
   - `BLYNK_AUTH_TOKEN`, `IMGUR_CLIENT_ID`  ← fill in your own keys
3. Run the host:
   ```bash
   python main.py
   ```

## Files

- `main.py` — host loop: serial poll → capture photo → upload → notify → unlock
- `camera.py` — webcam capture
- `blynk_api.py` — Blynk notifications
- `config.py` — settings and API tokens (placeholders committed; put real values locally)
- `nodemcu_door/nodemcu_door.ino` — firmware

## Status

Course project. Host-side Python is complete; requires the physical NodeMCU rig
and your own Blynk/Imgur keys to run live.
