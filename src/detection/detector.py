"""
Object Detection Module
Uses YOLOv8 to detect game objects on screen.
"""

import numpy as np
import cv2
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path


@dataclass
class Detection:
    label: str
    confidence: float
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x

    @property
    def cy(self) -> float:
        return self.y


LABELS = [
    "enemy",
    "ally",
    "self",
    "gem",
    "ball",
    "bush",
    "wall",
    "health_bar_enemy",
    "health_bar_ally",
    "super_ready",
]


class Detector:
    def __init__(self, model_path: str = "models/best.onnx"):
        self.model = None
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        """Load YOLOv8 model (.pt or .onnx)."""

        if not Path(self.model_path).exists():
            print(f"[Detector] Model not found at '{self.model_path}'")
            print("[Detector] Running in MOCK mode (no detections)")
            return

        try:
            from ultralytics import YOLO

            self.model = YOLO(self.model_path, task="detect")

            print(f"[Detector] Model loaded: {self.model_path}")

        except Exception as e:
            print(f"[Detector] Error loading model: {e}")

    def detect(self, frame: np.ndarray, conf_threshold: float = 0.5) -> List[Detection]:
        """Run detection on a frame."""

        if self.model is None:
            return self._mock_detections()

        results = self.model(frame, conf=conf_threshold, verbose=False)[0]

        detections = []

        h, w = frame.shape[:2]

        for box in results.boxes:
            cls_id = int(box.cls[0])

            label = results.names[cls_id]

            conf = float(box.conf[0])

            x_center, y_center, bw, bh = box.xywhn[0].tolist()

            detections.append(
                Detection(
                    label=label,
                    confidence=conf,
                    x=x_center,
                    y=y_center,
                    w=bw,
                    h=bh,
                )
            )

        return detections

    def _mock_detections(self) -> List[Detection]:
        """Return fake detections for testing without a model."""
        return []

    def get_by_label(self, detections: List[Detection], label: str) -> List[Detection]:
        return [d for d in detections if d.label == label]

    def nearest_to_center(self, detections: List[Detection]) -> Optional[Detection]:
        """Find detection nearest to screen center."""

        if not detections:
            return None

        return min(
            detections,
            key=lambda d: (d.x - 0.5) ** 2 + (d.y - 0.5) ** 2
        )

    def draw_detections(
        self,
        frame: np.ndarray,
        detections: List[Detection]
    ) -> np.ndarray:
        """Draw bounding boxes on frame for debug."""

        h, w = frame.shape[:2]

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

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(
                frame,
                f"{d.label} {d.confidence:.2f}",
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
            )

        return frame