import pygame as pg
import settings
from fighter import *

class NPC(Fighter):
    def __init__(self, game,
                 start_pos, start_facing_left,
                 movement_distance = settings.movement_distance,
                 max_health = settings.max_health,
                 path = "assets/sprites/fighter_2/",
                 animation_speed = settings.animation_speed,
                 color = "orchid3"):
        super().__init__(game, start_pos, start_facing_left, movement_distance, max_health, path, animation_speed, color)
        
    def ai_controls(self):
        return "idle"
    
    def update(self):
        super().update(self.ai_controls())