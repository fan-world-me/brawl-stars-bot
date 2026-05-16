# Brawl Stars Bot 🤖

An AI-powered bot for Brawl Stars using computer vision (YOLOv8) and ADB automation.

> ⚠️ **Warning**: Using bots violates Supercell's ToS. Use a secondary account for testing only.

## License

GPL-3.0 — see [LICENSE](LICENSE)

## Requirements

- Python 3.10+
- NVIDIA GPU (GTX 1660 Ti or better recommended)
- Android emulator (LDPlayer, MuMu, BlueStacks)
- ADB installed and in PATH

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/brawl-stars-bot.git
cd brawl-stars-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install ADB (if not already)
# Windows: download from https://developer.android.com/tools/releases/platform-tools

# 4. Start your emulator and launch Brawl Stars

# 5. Run the bot
python main.py --emulator LDPlayer --mode showdown --debug
```

## Project Structure

```
brawl-stars-bot/
├── main.py                  # Entry point
├── requirements.txt
├── src/
│   ├── capture/
│   │   └── screen_capture.py   # Screen capture from emulator
│   ├── detection/
│   │   └── detector.py         # YOLOv8 object detection
│   ├── control/
│   │   └── adb_controller.py   # ADB touch/swipe commands
│   ├── logic/
│   │   └── game_logic.py       # Game strategy (Showdown, Gem Grab, Brawl Ball)
│   └── gui/
│       └── overlay.py          # Debug overlay
├── scripts/
│   ├── collect_dataset.py      # Collect screenshots for training
│   └── train_model.py          # Train YOLOv8 model
├── models/                     # Trained model weights (not in git)
└── data/
    └── screenshots/            # Raw screenshots for labeling
```

## Development Roadmap

### Stage 1 — Setup ✅
- [x] Project structure
- [x] Screen capture module
- [x] ADB controller
- [x] Basic game logic

### Stage 2 — Vision (In Progress)
- [ ] Collect 500+ screenshots
- [ ] Label with Roboflow or LabelImg
- [ ] Train YOLOv8n model
- [ ] Validate detection accuracy

### Stage 3 — Game Modes
- [ ] Showdown logic
- [ ] Gem Grab logic
- [ ] Brawl Ball logic

### Stage 4 — Advanced
- [ ] State machine (lobby → game → end screen)
- [ ] Auto reward collection
- [ ] Brawler selection
- [ ] Reinforcement learning agent (PPO)

## Training Your Own Model

```bash
# Step 1: Collect screenshots while playing
python scripts/collect_dataset.py

# Step 2: Label images
# Use Roboflow (free): https://roboflow.com
# Export as YOLOv8 format to data/dataset/

# Step 3: Train
python scripts/train_model.py
```

## Supported Emulators

| Emulator | ADB Port | Status |
|----------|----------|--------|
| LDPlayer | 5555 | ✅ Recommended |
| MuMu Player | 7555 | ✅ Works |
| BlueStacks | 5555 | ✅ Works |
| Nox | 62001 | ⚠️ Untested |

## Contributing

Pull requests welcome! See roadmap above for what needs work.
