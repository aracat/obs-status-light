import time
import os
import time
import math
from busylight.lights import Light

TEMP_FILE = os.path.join(os.getenv("TEMP"), "obs_status.txt")
STALE_TIMEOUT = 3  # seconds

def lerp(a, b, t):
    return int(a + (b - a) * t)

def congestion_to_color(value, intensity):
    t = max(0.0, min(1.0, value))  # Clamp
    r = lerp(0, intensity, t)
    g = lerp(intensity, 0, t)
    b = 0
    return (r, g, b)

def read_status():
    try:
        # Check file modification time
        if not os.path.exists(TEMP_FILE):
            return None

        modified_time = os.path.getmtime(TEMP_FILE)
        if time.time() - modified_time > STALE_TIMEOUT:
            return (0, "stale")

        with open(TEMP_FILE, "r") as f:
            line = f.read().strip()
            if "," not in line:
                return None
            congestion_str, state = line.split(",", 1)
            congestion = float(congestion_str)
            return congestion, state.strip().lower()
    except:
        return None

def main():
    if light is None:
        print("Failed to find a light")
        return

    light.on((255, 255, 255))
    time.sleep(3)

    last_update = time.time()
    result = read_status()
    
    blink = 0
    breathe_base = time.time()
    while True:
        breathe = (math.sin((time.time() - breathe_base) * 3.14159 / 2) + 1.0) / 2.0
        
        try:
            if last_update + 1 < time.time():
                blink = 255 - blink
                result = read_status()
                last_update = time.time()
            if result is None:
                light.on((blink, 0, blink))                     # Flashing purple = malformed or missing file
            else:
                congestion, state = result
                if state == "offline":
                    light.on((0, 0, lerp(40, 64, breathe)))     # Blue = not streaming
                elif state == "disconnected":
                    light.on((blink, 0, 0))                     # Red = attempting to reconnect
                elif state == "online":
                    color = congestion_to_color(congestion, lerp(160, 255, breathe))
                    light.on(color)                             # Green/Red = stream online
                elif state == "stale":
                    light.on((0, 0, blink))                     # Flashing blue = stale
                else:
                    light.on((blink, 0, blink))                 # Flashing purple = malformed status
        except:
            try:
                light.on((blink, 0, blink))                     # Flashing purple = other error
            except:
                pass
        time.sleep(0.1)

if __name__ == "__main__":
    light = Light.first_light()
    try:
        main()
    finally:
        light.off()
    
