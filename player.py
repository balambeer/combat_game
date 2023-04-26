import pygame as pg
import settings
from fighter import *

class Player(Fighter):
    def __init__(self, game,
                 start_pos, start_facing_left,
                 movement_speed = settings.movement_speed,
                 max_health = settings.max_health,
                 path = "assets/sprites/fighter_1/",
                 animation_speed = settings.animation_speed,
                 color = "orchid3"):
        super().__init__(game, start_pos, start_facing_left, movement_speed, max_health, path, animation_speed, color)
        
    def get_keyboard_inputs(self):
        
        control_input = "idle"
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if self.facing_left:
                control_input = "move"
            else:
                control_input = "turn"
        if keys[pg.K_RIGHT]:
            if self.facing_left:
                control_input = "turn"
            else:
                control_input = "move"
        if keys[pg.K_a]:
            control_input = "attack_low"
        if keys[pg.K_s]:
            control_input = "attack_mid"
        if keys[pg.K_d]:
            control_input = "attack_high"
        
        return control_input
    
    def update(self):
        super().update(self.get_keyboard_inputs(), self.game.enemy)
