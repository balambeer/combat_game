import pygame as pg
import settings
import random
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
        
    def ai_controls_in_fight(self, opponent):
        ai_control = "idle"
        if opponent.attacking:
            if random.random() < 0.5:
                ai_control = opponent.state
        
        return ai_control
    
    def ai_controls_not_in_fight(self):
        return "idle"
    
    def update(self, opponent):
        if opponent == None:
            ai_controls = self.ai_controls_not_in_fight()
        else:
            ai_controls = self.ai_controls_in_fight(opponent)
        super().update(ai_controls, opponent)