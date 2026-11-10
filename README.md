[![Telegram](https://img.shields.io/badge/Telegram-@fan__world__me-2CA5E0?style=flat-square&logo=telegram)](https://t.me/fan_world_me)   [![Discord](https://img.shields.io/badge/Discord-fan__world__me-5865F2?style=flat-square&logo=discord)](https://discord.com/users/1040301536036786248)   [![GitHub](https://img.shields.io/badge/GitHub-fan--world--me-181717?style=flat-square&logo=github)](https://github.com/fan-world-me)   [![Portfolio](https://img.shields.io/badge/Portfolio-fan--world--me.github.io-00e5ff?style=flat-square&logo=githubpages&logoColor=white)](https://fan-world-me.github.io/)

# Brawl Stars Bot 🤖

An AI-powered bot for Brawl Stars using computer vision (YOLOv8) and ADB automation.

> ⚠️ **Warning**: Using bots violates Supercell's ToS. Use a secondary account for testing only.

---

### 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-detection-FF6F00?style=flat-square&logo=ultralytics&logoColor=white)
![ADB](https://img.shields.io/badge/ADB-automation-34A853?style=flat-square&logo=android&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA_GPU-recommended-76B900?style=flat-square&logo=nvidia&logoColor=white)

---

### 📋 Requirements

- Python 3.10+
- NVIDIA GPU (GTX 1660 Ti or better recommended)
- Android emulator (LDPlayer, MuMu, BlueStacks)
- ADB installed and in PATH

---

### 🔧 Setup

```bash
# 1. Clone the repo
git clone https://github.com/fan-world-me/brawl-stars-bot.git
cd brawl-stars-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install ADB (if not already)
# Windows: download from https://developer.android.com/tools/releases/platform-tools

# 4. Start your emulator and launch Brawl Stars

# 5. Run the bot
python main.py --emulator LDPlayer --mode showdown --debug
```

---

### 🗂️ Project Structure

```
brawl-stars-bot/
├── main.py                     — entry point
├── requirements.txt
├── src/
│   ├── capture/
│   │   └── screen_capture.py   — screen capture from emulator
│   ├── detection/
│   │   └── detector.py         — YOLOv8 object detection
│   ├── control/
│   │   └── adb_controller.py   — ADB touch/swipe commands
│   ├── logic/
│   │   └── game_logic.py       — game strategy (Showdown, Gem Grab, Brawl Ball)
│   └── gui/
│       └── overlay.py          — debug overlay
├── scripts/
│   ├── collect_dataset.py      — collect screenshots for training
│   └── train_model.py          — train YOLOv8 model
├── models/                     — trained model weights (not in git)
└── data/
    └── screenshots/            — raw screenshots for labeling
```

---

### 🧠 Training Your Own Model

```bash
# Step 1: Collect screenshots while playing
python scripts/collect_dataset.py

# Step 2: Label images
# Use Roboflow (free): https://roboflow.com
# Export as YOLOv8 format to data/dataset/

# Step 3: Train
python scripts/train_model.py
```

---

### 📱 Supported Emulators

| Emulator | ADB Port | Status |
|---|---|---|
| LDPlayer | 5555 | ✅ Recommended |
| MuMu Player | 7555 | ✅ Works |
| BlueStacks | 5555 | ✅ Works |
| Nox | 62001 | ⚠️ Untested |

---

### 🗺️ Development Roadmap

**Stage 1 — Setup** ✅
- [x] Project structure
- [x] Screen capture module
- [x] ADB controller
- [x] Basic game logic

**Stage 2 — Vision** *(in progress)*
- [ ] Collect 500+ screenshots
- [ ] Label with Roboflow or LabelImg
- [ ] Train YOLOv8n model
- [ ] Validate detection accuracy

**Stage 3 — Game Modes**
- [ ] Showdown logic
- [ ] Gem Grab logic
- [ ] Brawl Ball logic

**Stage 4 — Advanced**
- [ ] State machine (lobby → game → end screen)
- [ ] Auto reward collection
- [ ] Brawler selection
- [ ] Reinforcement learning agent (PPO)

---

### 🤝 Contributing

Pull requests welcome! See the roadmap above for what needs work.

---

### 📄 License

[GPL-3.0](LICENSE) © [fan-world-me](https://github.com/fan-world-me)

---

Made with 🩵 in Ukraine 🇺🇦

[![Telegram](https://img.shields.io/badge/Telegram-@fan__world__me-2CA5E0?style=flat-square&logo=telegram)](https://t.me/fan_world_me)   [![Discord](https://img.shields.io/badge/Discord-fan__world__me-5865F2?style=flat-square&logo=discord)](https://discord.com/users/1040301536036786248)   [![Portfolio](https://img.shields.io/badge/Portfolio-fan--world--me.github.io-00e5ff?style=flat-square&logo=githubpages&logoColor=white)](https://fan-world-me.github.io/)
