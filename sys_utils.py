"""Turn off (and optionally back on) the monitor in Windows 10/11."""

import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import POINTER, cast

# WinAPI constants (documented & stable)
HWND_BROADCAST   = 0xFFFF
WM_SYSCOMMAND    = 0x0112
SC_MONITORPOWER  = 0xF170    # monitor-power command

def monitor_off() -> None:
    """Shut the screen off immediately."""
    ctypes.windll.user32.PostMessageW(
        HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2
    )


def set_mute(state: bool):  # True = mute, False = unmute
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(state, None)

if __name__ == "__main__":
    monitor_off()
