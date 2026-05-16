"""
ADB Controller Module
Sends touch/swipe commands to the emulator via ADB.
"""

import subprocess
import time
import random
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Action:
    type: str          # "move", "attack", "super", "tap", "swipe", "idle"
    x: Optional[float] = None   # target x (0-1 normalized)
    y: Optional[float] = None   # target y (0-1 normalized)
    duration: float = 0.0


# Default ADB ports per emulator
EMULATOR_PORTS = {
    "LDPlayer": 5555,
    "BlueStacks": 5555,
    "MuMu": 7555,
    "Nox": 62001,
}

# Default screen resolution (match your emulator settings)
SCREEN_W = 900
SCREEN_H = 1600

# Virtual joystick center position (normalized)
JOYSTICK_CENTER = (0.15, 0.82)
JOYSTICK_RADIUS = 0.08  # normalized radius

# Attack button position (normalized)
ATTACK_BTN = (0.92, 0.75)
SUPER_BTN = (0.92, 0.88)


class ADBController:
    def __init__(self, emulator: str = "MuMu", port: Optional[int] = None):
        self.emulator = emulator
        self.port = port or EMULATOR_PORTS.get(emulator, 5555)
        self.device = "127.0.0.1:7555"
        self._connect()

    def _connect(self):
        """Connect to emulator via ADB."""
        result = self._run(f"adb connect {self.device}")
        if "connected" in result or "already" in result:
            print(f"[ADB] Connected to {self.device}")
        else:
            print(f"[ADB] Warning: {result}")

    def _run(self, cmd: str) -> str:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
        except Exception as e:
            return str(e)

    def _norm_to_px(self, x: float, y: float) -> Tuple[int, int]:
        """Convert normalized (0-1) coords to pixel coords."""
        return int(x * SCREEN_W), int(y * SCREEN_H)

    def tap(self, x: float, y: float):
        """Tap at normalized position."""
        px, py = self._norm_to_px(x, y)
        self._run(f"adb -s {self.device} shell input tap {px} {py}")

    def swipe(self, x1: float, y1: float, x2: float, y2: float, duration_ms: int = 200):
        """Swipe from (x1,y1) to (x2,y2)."""
        px1, py1 = self._norm_to_px(x1, y1)
        px2, py2 = self._norm_to_px(x2, y2)
        self._run(f"adb -s {self.device} shell input swipe {px1} {py1} {px2} {py2} {duration_ms}")

    def move_joystick(self, direction_x: float, direction_y: float):
      cx, cy = JOYSTICK_CENTER
      tx = cx + direction_x * JOYSTICK_RADIUS
      ty = cy + direction_y * JOYSTICK_RADIUS
      tx = max(0.0, min(1.0, tx))
      ty = max(0.0, min(1.0, ty))
      # Держим палец на джойстике дольше
      self.swipe(cx, cy, tx, ty, duration_ms=500)

    def attack(self, aim_x: Optional[float] = None, aim_y: Optional[float] = None):
        """Press attack button, optionally aiming at a position."""
        if aim_x is not None and aim_y is not None:
            # Swipe from attack button toward aim
            self.swipe(ATTACK_BTN[0], ATTACK_BTN[1], aim_x, aim_y, duration_ms=100)
        else:
            self.tap(ATTACK_BTN[0], ATTACK_BTN[1])

    def use_super(self, aim_x: Optional[float] = None, aim_y: Optional[float] = None):
        """Use super ability."""
        if aim_x is not None and aim_y is not None:
            self.swipe(SUPER_BTN[0], SUPER_BTN[1], aim_x, aim_y, duration_ms=100)
        else:
            self.tap(SUPER_BTN[0], SUPER_BTN[1])

    def execute(self, action: Action):
        """Execute a game action."""
        if action.type == "move" and action.x is not None:
            # Calculate direction from center to target
            dx = action.x - 0.5
            dy = action.y - 0.5
            length = (dx**2 + dy**2) ** 0.5
            if length > 0:
                dx /= length
                dy /= length
            self.move_joystick(dx, dy)

        elif action.type == "attack":
            self.attack(action.x, action.y)

        elif action.type == "super":
            self.use_super(action.x, action.y)

        elif action.type == "tap" and action.x is not None:
            self.tap(action.x, action.y)

        elif action.type == "idle":
            pass  # Do nothing

        time.sleep(action.duration)

    def take_screenshot_adb(self, save_path: str):
        """Take screenshot via ADB (slower but reliable)."""
        self._run(f"adb -s {self.device} shell screencap -p /sdcard/screen.png")
        self._run(f"adb -s {self.device} pull /sdcard/screen.png {save_path}")
