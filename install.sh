#!/bin/bash
if [ "$EUID" -ne 0 ]; then 
    echo "Debe ejecutarse como root"
    exit 1
fi

cp hdmi-audio-switch.sh /usr/local/bin/
chmod +x /usr/local/bin/hdmi-audio-switch.sh
cp 99-hdmi-audio.rules /etc/udev/rules.d/

udevadm control --reload-rules
udevadm trigger
echo "Plugin instalado y reglas de udev recargadas."
