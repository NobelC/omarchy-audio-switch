import QtQuick
import Quickshell

import QtQuick
import Quickshell
import Quickshell.Io

Item {
    id: audioService

    property string currentProfile: "unknown"
    property string hdmiStatus: "disconnected"

    Component.onCompleted: runner.running = true

    Process {
        id: runner
        command: ["python3", Qt.resolvedUrl("monitor.py").toString().replace("file://", "")]
        running: false

        stdout: SplitParser {
            onRead: data => {
                if (data.length === 0) return
                try {
                    const parsed = JSON.parse(data)
                    audioService.currentProfile = parsed.profile
                    audioService.hdmiStatus = parsed.hdmi_status
                } catch (e) {
                    console.warn("Audio Switch: Error parseando estado:", e, data)
                }
            }
        }

        stderr: SplitParser {
            onRead: data => console.warn("Audio Switch (monitor.py):", data)
        }

        onRunningChanged: {
            if (!running) {
                console.warn("Audio Switch: monitor.py terminó. Reiniciando...")
                Qt.callLater(() => runner.running = true)
            }
        }
    }
}
