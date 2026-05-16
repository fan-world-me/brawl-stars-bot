"""
Brawl Stars Bot - Main Entry Point
License: GPL-3.0
"""

from src.capture.screen_capture import ScreenCapture
from src.detection.detector import Detector
from src.control.adb_controller import ADBController
from src.logic.game_logic import GameLogic
from src.gui.overlay import Overlay
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Brawl Stars Bot")
    parser.add_argument("--emulator", type=str, default="MuMu", help="Emulator name (LDPlayer, BlueStacks, MuMu)")
    parser.add_argument("--mode", type=str, default="showdown", help="Game mode (showdown, gem_grab, brawl_ball)")
    parser.add_argument("--debug", action="store_true", help="Show debug overlay")
    parser.add_argument("--collect-rewards", action="store_true", help="Only collect rewards, don't play")
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"[BOT] Starting Brawl Stars Bot")
    print(f"[BOT] Emulator: {args.emulator} | Mode: {args.mode}")

    # Init modules
    capture = ScreenCapture(emulator=args.emulator)
    detector = Detector(model_path="models/best.onnx")
    controller = ADBController(emulator=args.emulator)
    logic = GameLogic(mode=args.mode)
    overlay = Overlay(enabled=args.debug)

    print("[BOT] All modules initialized. Starting loop...")

    try:
        while True:
            # 1. Capture screen
            frame = capture.get_frame()
            if frame is None:
                print("[BOT] No frame captured, retrying...")
                time.sleep(1)
                continue

            # 2. Detect objects
            detections = detector.detect(frame)

            # 3. Decide action
            action = logic.decide(detections)

            # 4. Execute action
            if action:
                controller.execute(action)

            # 5. Debug overlay
            overlay.draw(frame, detections, action)

            time.sleep(0.05)  # ~20 FPS loop

    except KeyboardInterrupt:
        print("\n[BOT] Stopped by user.")
    finally:
        overlay.close()


if __name__ == "__main__":
    main()
