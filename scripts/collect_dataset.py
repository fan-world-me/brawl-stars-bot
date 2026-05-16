"""
Dataset Collector
Captures screenshots for YOLO training dataset.
Press 'S' to save screenshot, 'Q' to quit.
"""

import cv2
import os
import time
from src.capture.screen_capture import ScreenCapture

SAVE_DIR = "data/screenshots"
os.makedirs(SAVE_DIR, exist_ok=True)


def collect():
    capture = ScreenCapture()
    count = len(os.listdir(SAVE_DIR))
    print(f"[Collector] Starting. {count} screenshots already collected.")
    print("[Collector] Press S - save frame | Q - quit | Auto-save every 3s")

    last_auto = time.time()

    while True:
        frame = capture.get_frame()
        if frame is None:
            continue

        preview = cv2.resize(frame, (960, 540))
        cv2.putText(preview, f"Saved: {count} | S=save Q=quit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Collector", preview)

        key = cv2.waitKey(1) & 0xFF

        # Auto-save every 3 seconds
        if time.time() - last_auto > 3.0:
            path = os.path.join(SAVE_DIR, f"frame_{count:05d}.jpg")
            cv2.imwrite(path, frame)
            count += 1
            last_auto = time.time()
            print(f"[Collector] Auto-saved: {path}")

        if key == ord('s'):
            path = os.path.join(SAVE_DIR, f"frame_{count:05d}.jpg")
            cv2.imwrite(path, frame)
            count += 1
            print(f"[Collector] Saved: {path}")

        elif key == ord('q'):
            break

    cv2.destroyAllWindows()
    print(f"[Collector] Done. Total screenshots: {count}")


if __name__ == "__main__":
    collect()
