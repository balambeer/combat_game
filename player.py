import pygame as pg
from fighter import *

class Player(Fighter):
    def __init__(self, game,
                 start_pos,
                 movement_speed,
                 path,
                 animation_speed):
        super().__init__(game, start_pos, movement_speed, path, animation_speed)
        
    def get_keyboard_inputs(self):
        
        control_input = "idle"
        
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            if self.facing_left:
                control_input = "move"
            else:
                control_input = "turn"
        if keys[pg.K_d]:
            if self.facing_left:
                control_input = "turn"
            else:
                control_input = "move"
        if keys[pg.K_s]:
            control_input = "attack"
        
        print("Control input = %s" % control_input)
        return control_input
    
    def update(self):
        super().update(self.get_keyboard_inputs())
