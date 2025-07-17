# 🦖 Dino Game (Python + Pygame)

This is a pixel-art inspired recreation of the classic **Google Chrome Dino game**, built in Python using the **Pygame** library. Jump over cacti, survive the night, and race for high scores — now with sounds, animations, and extra features!

---

## 🎮 Features

- ✅ Smooth dino jumping and running animation
- 🌵 Randomized cactus obstacles (multiple types)
- 🎵 Sound effects for jumping, game over, and milestones
- 🌙 Day/Night mode switch as you survive longer
- 🛡️ Shield power-up (press `S` to activate!)
- 🏁 Score tracking with high score persistence
- 🖼️ Press-to-start screen and restart on game over
- 🌄 Scrolling background and ground for realism

---

## 🧰 Requirements

- Python 3.7+
- Set up a virtual environment:
  ### For Windows
  
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
  
  ### For macOS/Linux
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```
  
- [Pygame](https://www.pygame.org/)  
Install via pip:

```bash
pip install pygame
```
---
📁 Folder Structure
```
dino_game/
│
├── dino_game.py           # Main game code
├── assets/
│   ├── dino1.png
│   ├── dino2.png
│   ├── cactus1.png
│   ├── cactus2.png
│   ├── ground.png
│   ├── background_day.png
│   ├── background_night.png
│   ├── gameover.mp3
│   ├── jump.mp3
│   ├── milestone.mp3
│   └── shield.png
├── highscore.txt
└── README.md
```
---

🚀 How to Run
```bash
python dino_game.py
```

Jump: SPACE or ↑

Shield: S

Restart: R (after game over)

---

🔔 Milestone Sound
A sound will play once when you hit 500 points. You can customize the milestone.mp3 sound in the assets/ folder.

---
🧠 Credits & Notes
Created by @aijzkhai05

Inspired by Google Chrome's offline Dino game

Art and sounds are original or sourced from open libraries

Fully beginner-friendly and expandable
