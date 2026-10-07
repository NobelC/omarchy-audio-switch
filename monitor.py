#!/usr/bin/env python3
"""Switches the active PipeWire/PulseAudio sink profile between HDMI and
analog output depending on whether an HDMI display is connected.

Prints one JSON line to stdout every time it changes the profile:
    {"card": "...", "profile": "...", "hdmi_status": "connected"|"disconnected"}
Diagnostics go to stderr so stdout stays machine-readable for Service.qml.
"""
import json
import os
import subprocess
import sys
import time

POLL_SECONDS = 2


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def list_cards():
    """Return pactl's card list as parsed JSON, or None on failure."""
    try:
        result = subprocess.run(
            ["pactl", "-f", "json", "list", "cards"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            log("pactl list cards failed:", result.stderr.strip())
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        log("pactl list cards error:", e)
        return None


def find_card_with_hdmi():
    """Pick the card that actually exposes an HDMI output port, along with
    the real profile names it offers for hdmi and analog output, instead of
    guessing by card name or hardcoding profile strings."""
    cards = list_cards()
    if not cards:
        return None
    for card in cards:
        ports = card.get("ports", {}) or {}
        has_hdmi_port = any(
            (p.get("type") or "").lower() == "hdmi" for p in ports.values()
        )
        if not has_hdmi_port:
            continue
        profiles = list(card.get("profiles", {}) or {})
        hdmi_profiles = sorted(p for p in profiles if "hdmi" in p.lower() and p != "off")
        analog_profiles = sorted(p for p in profiles if "analog" in p.lower() and p != "off")
        if not hdmi_profiles or not analog_profiles:
            continue
        return {
            "name": card["name"],
            "hdmi_profile": hdmi_profiles[0],
            "analog_profile": analog_profiles[0],
        }
    return None


def check_hdmi_status():
    """True if any DRM HDMI connector reports 'connected'."""
    try:
        base = "/sys/class/drm"
        for entry in os.listdir(base):
            if "HDMI-A-" not in entry:
                continue
            status_file = os.path.join(base, entry, "status")
            try:
                with open(status_file) as f:
                    if f.read().strip() == "connected":
                        return "connected"
            except OSError:
                continue
    except OSError as e:
        log("could not read /sys/class/drm:", e)
    return "disconnected"


def set_profile(card_name, profile):
    try:
        subprocess.run(
            ["pactl", "set-card-profile", card_name, profile],
            check=True, capture_output=True, text=True, timeout=5,
        )
        return True
    except subprocess.CalledProcessError as e:
        log(f"failed to set profile {profile} on {card_name}:", e.stderr.strip())
        return False
    except subprocess.TimeoutExpired:
        log(f"timed out setting profile {profile} on {card_name}")
        return False


def main():
    sys.stdout.reconfigure(line_buffering=True)

    card = find_card_with_hdmi()
    if not card:
        log("no sound card with an HDMI port found; exiting")
        sys.exit(0)
    log(f"watching card {card['name']} "
        f"(hdmi={card['hdmi_profile']!r}, analog={card['analog_profile']!r})")

    last_state = None
    while True:
        current_state = check_hdmi_status()
        if current_state != last_state:
            profile = card["hdmi_profile"] if current_state == "connected" else card["analog_profile"]
            if set_profile(card["name"], profile):
                print(json.dumps({
                    "card": card["name"],
                    "profile": profile,
                    "hdmi_status": current_state,
                }))
            last_state = current_state
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
