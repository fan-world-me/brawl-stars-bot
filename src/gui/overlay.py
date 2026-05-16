"""
Debug Overlay Module
Shows real-time detection info on screen.
"""

import cv2
import numpy as np
from typing import List, Optional
from src.detection.detector import Detection
from src.control.adb_controller import Action


class Overlay:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.window_name = "BrawlBot Debug"
        if enabled:
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_name, 960, 540)
            print("[Overlay] Debug window opened")

    def draw(self, frame: np.ndarray, detections: List[Detection], action: Optional[Action]):
        if not self.enabled or frame is None:
            return

        display = frame.copy()
        h, w = display.shape[:2]

        # Draw detections
        colors = {
            "enemy": (0, 0, 255),
            "ally": (0, 255, 0),
            "self": (255, 255, 0),
            "gem": (0, 255, 128),
            "ball": (255, 128, 0),
        }
        for d in detections:
            x1 = int((d.x - d.w / 2) * w)
            y1 = int((d.y - d.h / 2) * h)
            x2 = int((d.x + d.w / 2) * w)
            y2 = int((d.y + d.h / 2) * h)
            color = colors.get(d.label, (200, 200, 200))
            cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
            cv2.putText(display, f"{d.label} {d.confidence:.2f}",
                        (x1, max(y1 - 5, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

        # Draw action info
        if action:
            info = f"Action: {action.type}"
            if action.x is not None:
                info += f" -> ({action.x:.2f}, {action.y:.2f})"
            cv2.putText(display, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Draw detection count
        cv2.putText(display, f"Detections: {len(detections)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow(self.window_name, display)
        cv2.waitKey(1)

    def close(self):
        if self.enabled:
            cv2.destroyAllWindows()
