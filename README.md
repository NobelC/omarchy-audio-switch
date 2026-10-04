# Dynamic HDMI Audio Switcher

Automatically switches the active audio profile between HDMI and the
internal laptop speakers when an HDMI display is connected or
disconnected in Omarchy.

## Requirements and Dependencies

The plugin relies on software and interfaces provided by a standard
Omarchy installation:

* Omarchy
* Quickshell
* Python 3
* PipeWire with `pactl` compatibility
* Linux DRM interface at `/sys/class/drm/`

No additional packages or external binaries are required.

## Installation

You can add and test this plugin directly through the Omarchy command
line interface.

To clone the plugin and inspect the code before enabling it:

```bash
omarchy plugin add \
  https://github.com/NobelC/omarchy-hdmi-audio.git
```

To install and enable the plugin immediately:

```bash
omarchy plugin add \
  https://github.com/NobelC/omarchy-hdmi-audio.git \
  --enable
```

The plugin monitors HDMI connection status and automatically selects the
appropriate PipeWire audio profile.

## Uninstallation

To completely remove the plugin and its directory from the system:

```bash
omarchy plugin remove omarchy-hdmi-audio
```

## License

This project is licensed under the [MIT License](LICENSE).

See the `LICENSE` file in the repository for the complete license text.
# Dynamic HDMI Audio Switcher

Automatically switches the active audio profile between HDMI and the
internal laptop speakers when an HDMI display is connected or
disconnected in Omarchy.

## Requirements and Dependencies

The plugin relies on software and interfaces provided by a standard
Omarchy installation:

* Omarchy
* Quickshell
* Python 3
* PipeWire with `pactl` compatibility
* Linux DRM interface at `/sys/class/drm/`

No additional packages or external binaries are required.

## Installation

You can add and test this plugin directly through the Omarchy command
line interface.

To clone the plugin and inspect the code before enabling it:

```bash
omarchy plugin add \
  https://github.com/NobelC/omarchy-hdmi-audio.git
```

To install and enable the plugin immediately:

```bash
omarchy plugin add \
  https://github.com/NobelC/omarchy-hdmi-audio.git \
  --enable
```

The plugin monitors HDMI connection status and automatically selects the
appropriate PipeWire audio profile.

## Uninstallation

To completely remove the plugin and its directory from the system:

```bash
omarchy plugin remove omarchy-hdmi-audio
```

## License

This project is licensed under the [MIT License](LICENSE).

See the `LICENSE` file in the repository for the complete license text.

