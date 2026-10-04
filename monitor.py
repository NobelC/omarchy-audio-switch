#!/usr/bin/env python3
import os
import sys
import time
import json
import subprocess

def get_active_card():
    try:
        result = subprocess.run(['pactl', 'list', 'cards', 'short'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'pci' in line.lower():
                return line.split()[1]
    except Exception:
        return None
    return None

def check_hdmi_status():
    try:
        for path in os.listdir('/sys/class/drm/'):
            if 'HDMI-A-' in path:
                status_file = os.path.join('/sys/class/drm/', path, 'status')
                with open(status_file, 'r') as f:
                    return f.read().strip()
    except (IOError, OSError):
        pass
    return "disconnected"

def main():
    card = get_active_card()
    if not card:
        sys.exit(0)

    
    sys.stdout.reconfigure(line_buffering=True)
    
    last_state = None
    while True:
        current_state = check_hdmi_status()
        if current_state != last_state:
            profile = "output:hdmi-stereo" if current_state == "connected" else "output:analog-stereo"
            try:
    
                subprocess.run(['pactl', 'set-card-profile', card, profile], check=True, capture_output=True)
                
   
                print(json.dumps({"card": card, "profile": profile, "hdmi_status": current_state}))
            except subprocess.CalledProcessError:
                pass 
            last_state = current_state
        time.sleep(2)

if __name__ == "__main__":
    main()
