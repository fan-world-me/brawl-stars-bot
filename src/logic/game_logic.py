"""
Game Logic Module
Decides what action to take based on detections.
"""

from src.detection.detector import Detection, Detector
from src.control.adb_controller import Action
from typing import List, Optional
import time
import random


class GameLogic:
    def __init__(self, mode: str = "showdown"):
        self.mode = mode
        self.detector_helper = Detector.__new__(Detector)
        self.detector_helper.model = None
        self.last_attack_time = 0
        self.attack_cooldown = 0.8  # seconds between attacks

        mode_map = {
            "showdown": ShowdownLogic,
            "gem_grab": GemGrabLogic,
            "brawl_ball": BrawlBallLogic,
        }
        LogicClass = mode_map.get(mode, ShowdownLogic)
        self._logic = LogicClass()
        print(f"[Logic] Mode: {mode}")

    def decide(self, detections: List[Detection]) -> Optional[Action]:
        return self._logic.decide(detections)


class ShowdownLogic:
    """
    Solo Showdown logic:
    - Chase enemies when visible
    - Move toward center if no enemies
    - Attack nearest enemy
    """

    def __init__(self):
        self.last_attack = 0
        self.attack_cooldown = 0.8
        self.wander_timer = 0

    def decide(self, detections: List[Detection]) -> Optional[Action]:
        now = time.time()

        enemies = [d for d in detections if d.label == "enemy"]
        nearest_enemy = self._nearest_to_center(enemies)

        # Attack if enemy visible and cooldown passed
        if nearest_enemy and now - self.last_attack > self.attack_cooldown:
            self.last_attack = now
            return Action(type="attack", x=nearest_enemy.x, y=nearest_enemy.y)

        # Move toward nearest enemy
        if nearest_enemy:
            return Action(type="move", x=nearest_enemy.x, y=nearest_enemy.y)

        # No enemies - wander toward center
        if now - self.wander_timer > 2.0:
            self.wander_timer = now
            # Move toward screen center with slight randomness
            tx = 0.5 + random.uniform(-0.1, 0.1)
            ty = 0.5 + random.uniform(-0.1, 0.1)
            return Action(type="move", x=tx, y=ty)

        return Action(type="idle")

    def _nearest_to_center(self, detections: List[Detection]) -> Optional[Detection]:
        if not detections:
            return None
        return min(detections, key=lambda d: (d.x - 0.5)**2 + (d.y - 0.5)**2)


class GemGrabLogic:
    """
    Gem Grab logic:
    - Collect gems
    - Attack enemies
    - Retreat if carrying many gems
    """

    def __init__(self):
        self.last_attack = 0
        self.attack_cooldown = 0.8
        self.gems_carried = 0  # TODO: detect from UI

    def decide(self, detections: List[Detection]) -> Optional[Action]:
        now = time.time()

        enemies = [d for d in detections if d.label == "enemy"]
        gems = [d for d in detections if d.label == "gem"]

        nearest_enemy = self._nearest(enemies)
        nearest_gem = self._nearest(gems)

        # Attack nearby enemies first
        if nearest_enemy and now - self.last_attack > self.attack_cooldown:
            dist = ((nearest_enemy.x - 0.5)**2 + (nearest_enemy.y - 0.5)**2)**0.5
            if dist < 0.3:
                self.last_attack = now
                return Action(type="attack", x=nearest_enemy.x, y=nearest_enemy.y)

        # Collect nearest gem
        if nearest_gem:
            return Action(type="move", x=nearest_gem.x, y=nearest_gem.y)

        # Move toward center
        return Action(type="move", x=0.5, y=0.5)

    def _nearest(self, detections: List[Detection]) -> Optional[Detection]:
        if not detections:
            return None
        return min(detections, key=lambda d: (d.x - 0.5)**2 + (d.y - 0.5)**2)


class BrawlBallLogic:
    """
    Brawl Ball logic:
    - Chase ball
    - Shoot toward enemy goal
    - Defend own goal
    """

    def __init__(self):
        self.last_attack = 0
        self.attack_cooldown = 0.8

    def decide(self, detections: List[Detection]) -> Optional[Action]:
        now = time.time()

        ball = next((d for d in detections if d.label == "ball"), None)
        enemies = [d for d in detections if d.label == "enemy"]
        nearest_enemy = self._nearest(enemies)

        # If we have the ball (ball near center), shoot toward enemy goal (right side)
        if ball and abs(ball.x - 0.5) < 0.05 and abs(ball.y - 0.5) < 0.05:
            if now - self.last_attack > self.attack_cooldown:
                self.last_attack = now
                return Action(type="attack", x=0.95, y=0.5)  # shoot right

        # Chase ball
        if ball:
            return Action(type="move", x=ball.x, y=ball.y)

        # Attack enemy if no ball
        if nearest_enemy and now - self.last_attack > self.attack_cooldown:
            self.last_attack = now
            return Action(type="attack", x=nearest_enemy.x, y=nearest_enemy.y)

        return Action(type="idle")

    def _nearest(self, detections: List[Detection]) -> Optional[Detection]:
        if not detections:
            return None
        return min(detections, key=lambda d: (d.x - 0.5)**2 + (d.y - 0.5)**2)
