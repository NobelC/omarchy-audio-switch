#!/bin/bash
if [ "$EUID" -ne 0 ]; then 
    exit 1
fi

rm -f /usr/local/bin/hdmi-audio-switch.sh
rm -f /etc/udev/rules.d/99-hdmi-audio.rules

udevadm control --reload-rules
echo "Plugin desinstalado correctamente."
