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
                 draw_health_default = False,
                 draw_health_left = False,
                 color = "orchid3"):
        super().__init__(game,
                         start_pos,
                         start_facing_left,
                         movement_distance,
                         max_health,
                         path,
                         animation_speed,
                         draw_health_default,
                         draw_health_left,
                         color)
        
        self.last_call_to_ai = 0
        
    def ai_controls_in_fight(self, opponent):
        ai_control = "idle"
        call_time = pg.time.get_ticks()
        if (call_time - self.last_call_to_ai) > settings.ai_update_wait:
            # print("Called AI, elapsed time = %s" % (call_time - self.last_call_to_ai))
            if opponent.attacking:
                if random.random() < 0.1:
                    ai_control = opponent.state
            
            self.last_call_to_ai = call_time
        
        return ai_control
    
    def ai_controls_not_in_fight(self):
        call_time = pg.time.get_ticks()
        if (call_time - self.last_call_to_ai) > settings.ai_update_wait:
            self.last_call_to_ai = call_time
        
        return "idle"
    
    def update(self, opponent):
        if opponent == None:
            ai_controls = self.ai_controls_not_in_fight()
        else:
            ai_controls = self.ai_controls_in_fight(opponent)
        super().update(ai_controls, opponent)