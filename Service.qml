import QtQuick
import Quickshell

Item {
    id: audioService


import QtQuick
import Quickshell

Item {
    id: audioService


    property string currentProfile: "unknown"
    property string hdmiStatus: "disconnected"

    Component.onCompleted: {
        runner.start()
    }

    ProcessRunner {
        id: runner
        command: ["python3", Qt.resolvedUrl("monitor.py").replace("file://", "")]
        
        onReadyReadStandardOutput: {
            let output = runner.readAllStandardOutput().trim()
            if (output.length > 0) {
                try {
                    let data = JSON.parse(output)
                    audioService.currentProfile = data.profile
                    audioService.hdmiStatus = data.hdmi_status
                } catch (e) {
                    console.warn("Audio Switch: Error parseando estado:", e)
                }
            }
        }

        onFinished: {
            console.warn("Audio Switch: Monitor terminado. Reiniciando...")
            Qt.callLater(() => runner.start())
        }
    }
}
