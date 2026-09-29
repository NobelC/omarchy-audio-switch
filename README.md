# Dynamic HDMI Audio Switcher (Omarchy Plugin)

An event-driven Omarchy plugin that dynamically manages audio profile switching between internal laptop speakers and HDMI outputs. It relies on kernel-level `udev` events rather than CPU-intensive polling, eliminating race conditions between the system and the audio server.

## Features

- **Event-Driven Architecture:** Triggers instantly via kernel DRM events when an HDMI cable is plugged or unplugged.
- **Zero Polling:** Consumes no background CPU cycles.
- **Dynamic Hardware Detection:** Automatically identifies the active user session, the primary ALSA PCI audio card, and the exact DRM path (`card0` or `card1`).
- **WirePlumber Native:** Designed to coexist with PipeWire/WirePlumber priorities, allowing Bluetooth devices to seamlessly override the HDMI output naturally.

## Prerequisites

- **OS:** Arch Linux (Omarchy environment)
- **Audio Server:** PipeWire with WirePlumber
- **Compatibility Layer:** `pactl` (usually provided by `pipewire-pulse`)

## Installation

Install directly via the Omarchy plugin manager:

```bash
omarchy plugin install github.com/nobelc/omarchy-hdmi-audio
```

### Manual Installation

If you prefer to install it outside of the Omarchy plugin ecosystem:

```bash
git clone https://github.com/nobelc/omarchy-hdmi-audio.git
cd omarchy-hdmi-audio
sudo ./install.sh
```

## How It Works

1. **Kernel Level:** A custom rule in `/etc/udev/rules.d/99-hdmi-audio.rules` listens for `ACTION=="change"` on the `drm` subsystem.

2. **Environment Bridge:** When triggered, the `udev` rule runs `/usr/local/bin/hdmi-audio-switch.sh` as root. The script dynamically detects the active non-root user and injects the `XDG_RUNTIME_DIR` and D-Bus session variables to establish a connection to the user's PipeWire instance.

3. **Profile Switching:** It executes `pactl set-card-profile` to switch the single ALSA sound card between `output:hdmi-stereo` and `output:analog-stereo` based on the DRM port status.

## Uninstallation

To remove the plugin and restore default behavior:

```bash
omarchy plugin uninstall nobelc.hdmiaudio
```

### Manual Removal

Run the following from the repository root:

```bash
sudo ./uninstall.sh
```

## License

MIT License. Feel free to fork and modify it for your own dotfiles architecture.
