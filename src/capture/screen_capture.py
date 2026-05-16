"""
Screen Capture Module
Captures frames from the emulator window.
"""

import numpy as np
import cv2
import mss
import mss.tools
from typing import Optional


EMULATOR_WINDOWS = {
    "LDPlayer": "LDPlayer",
    "BlueStacks": "BlueStacks App Player",
    "MuMu": "MuMuPlayer",
    "Nox": "Nox App Player",
}


class ScreenCapture:
    def __init__(self, emulator: str = "MuMu"):
        self.emulator = emulator
        self.window_title = EMULATOR_WINDOWS.get(emulator, emulator)
        self.region = None
        self.sct = mss.mss()

        print(f"[Capture] Initialized for {emulator}")
        self._find_window()

    def _find_window(self):
        """Find the emulator window region on screen."""
        # TODO: Use pygetwindow or win32gui to find emulator window automatically
        # For now, fallback to manual region or full screen
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle("Android Device")
            if windows:
                w = windows[0]
                self.region = {"top": w.top, "left": w.left, "width": w.width, "height": w.height}
                print(f"[Capture] Found window: {self.region}")
            else:
                print(f"[Capture] Window '{self.window_title}' not found, using full screen")
                monitor = self.sct.monitors[1]
                self.region = monitor
        except ImportError:
            print("[Capture] pygetwindow not installed, using full screen")
            self.region = self.sct.monitors[1]

    def get_frame(self) -> Optional[np.ndarray]:
        """Capture current frame from emulator."""
        try:
            screenshot = self.sct.grab(self.region)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame
        except Exception as e:
            print(f"[Capture] Error: {e}")
            return None

    def get_frame_resized(self, width: int = 1280, height: int = 720) -> Optional[np.ndarray]:
        """Capture and resize frame."""
        frame = self.get_frame()
        if frame is not None:
            return cv2.resize(frame, (width, height))
        return None

    def save_screenshot(self, path: str):
        """Save a screenshot for dataset collection."""
        frame = self.get_frame()
        if frame is not None:
            cv2.imwrite(path, frame)
            print(f"[Capture] Screenshot saved: {path}")
