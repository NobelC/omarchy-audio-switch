#!/bin/bash


ACTIVE_USER=$(who | grep -v root | awk '{print $1}' | head -n1)
USER_ID=$(id -u $ACTIVE_USER)


RUN_AS_USER="sudo -u $ACTIVE_USER env XDG_RUNTIME_DIR=/run/user/$USER_ID DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$USER_ID/bus pactl"


CARD_NAME=$($RUN_AS_USER list cards short | grep -i pci | awk '{print $2}' | head -n 1)


DRM_STATUS_FILE=$(ls /sys/class/drm/card*-HDMI-A-*/status 2>/dev/null | head -n 1)

if [ -z "$DRM_STATUS_FILE" ]; then
    exit 1 
fi

HDMI_STATUS=$(cat "$DRM_STATUS_FILE")

if [ "$HDMI_STATUS" = "connected" ]; then
    $RUN_AS_USER set-card-profile "$CARD_NAME" output:hdmi-stereo
else
    $RUN_AS_USER set-card-profile "$CARD_NAME" output:analog-stereo
fi
