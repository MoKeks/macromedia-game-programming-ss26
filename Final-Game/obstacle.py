# obstacle.py
# Simple obstacle data class. Parsed from level file but NOT drawn or
# collision-checked in the skeleton. Students implement this in Uebung 003.
from entity import Entity
import pygame

class Obstacle(Entity):
    """Data-only obstacle. Parsed from .rfg level files.

    Students should implement:
    - draw(): render the obstacle as a colored rectangle
    - Collision detection with player
    """

    def __init__(
        self,
        track: int = 0,
        duration_start: int = 0,
        length: int = 0,
        color: tuple[int, int, int] = (255, 255, 255),
        width: int = 5,
        speed: int = 3
    ):
        self.track = track              # Which track (column) the obstacle is on
        self.duration_start = duration_start  # When it appears (in level duration)
        self.length = length            # How long it lasts (in duration units)
        self.color = color              # RGB color tuple
        self.width = width              # Pixel width
        self.alive = True

   
        # Derived screen coordinates (students compute these from track layout)
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def collsion(self, rect):
        if not self.alive:
            return              # Toter Enemy wird nicht gezeichnet
        if self.get_rect().colliderect(rect):
            return True

    # ------------------------------------------------------------------ #
    def step (self, speed) :
        self.pos.y += speed

    def is_alive(self) -> bool:
        """Return True if the enemy is alive. Once HP drops to 0,
        alive is permanently set to False (mirrors C++ behavior)."""
        if self.hp <= 0:
            self.alive = False
        return self.alive
    
    # draw check

    def draw(self, screen):
        if not self.alive:
            return              # Toter Enemy wird nicht gezeichnet
        super().draw(screen)
    #obstcales = pygame.Rect(5, 5, 5, 5)