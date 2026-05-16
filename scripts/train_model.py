"""
YOLO Model Training Script
Trains YOLOv8 on your labeled Brawl Stars dataset.

Before running:
1. Label screenshots using Roboflow or LabelImg
2. Export dataset in YOLOv8 format
3. Put dataset in data/dataset/ folder
4. Run: python scripts/train_model.py
"""

from ultralytics import YOLO
import yaml
import os

DATASET_YAML = "data/dataset/data.yaml"
MODEL_OUTPUT = "models/detector.pt"
BASE_MODEL = "yolov8n.pt"  # nano - fastest, good for real-time


def create_sample_yaml():
    """Create a sample dataset.yaml if not exists."""
    os.makedirs("data/dataset", exist_ok=True)
    sample = {
        "path": "data/dataset",
        "train": "images/train",
        "val": "images/val",
        "nc": 8,
        "names": ["enemy", "ally", "self", "gem", "ball", "bush", "wall", "super_ready"]
    }
    with open(DATASET_YAML, "w") as f:
        yaml.dump(sample, f)
    print(f"[Train] Sample dataset.yaml created at {DATASET_YAML}")
    print("[Train] Now add your labeled images to data/dataset/images/train/ and data/dataset/images/val/")


def train():
    if not os.path.exists(DATASET_YAML):
        print(f"[Train] Dataset config not found: {DATASET_YAML}")
        create_sample_yaml()
        return

    print(f"[Train] Starting training with {BASE_MODEL}")
    model = YOLO(BASE_MODEL)

    results = model.train(
        data=DATASET_YAML,
        epochs=20,
        imgsz=416,
        batch=32,
        device=0,          # GPU (0 = first GPU = GTX 1660 Ti)
        workers=4,
        patience=20,       # Early stopping
        save=True,
        project="models",
        name="brawl_detector",
    )

    # Copy best weights
    best = "models/brawl_detector/weights/best.pt"
    if os.path.exists(best):
        import shutil
        shutil.copy(best, MODEL_OUTPUT)
        print(f"[Train] Best model saved to {MODEL_OUTPUT}")

    print("[Train] Training complete!")
    return results


if __name__ == "__main__":
    train()
