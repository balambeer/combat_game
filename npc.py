import pygame as pg
import settings
import random
from fighter import *

class NPC(Fighter):
    def __init__(self, game,
                 start_pos, start_facing_left, npc_level, identifier,
                 movement_distance = settings.movement_distance,
                 max_health = settings.max_health,
                 path = "assets/sprites/fighter_2/",
                 animation_speed = settings.animation_speed,
                 draw_health_default = False,
                 draw_health_left = False,
                 color = "orchid3",
                 size = settings.fighter_size_on_screen):
        super().__init__(game,
                         start_pos,
                         start_facing_left,
                         identifier,
                         movement_distance,
                         max_health,
                         path,
                         animation_speed,
                         draw_health_default,
                         draw_health_left,
                         color,
                         size)
        
        self.last_call_to_ai = 0
        self.load_fight_logic(npc_level)
        
    def load_fight_logic(self, npc_level):
        csv_table = CSVTable("assets/enemy_logic/fight_logic.csv")
        self.fight_logic = {}
        for row in csv_table.table:
            if int(row[csv_table.col_index["level"]]) == npc_level:
                for i in range(1, len(row)):
                    self.fight_logic.update({ csv_table.header[i]: float(row[i]) })      
        
    def ai_controls_in_fight(self, opponent):
        ai_control = "idle"
        call_time = pg.time.get_ticks()
        if (call_time - self.last_call_to_ai) > settings.ai_update_wait:
            # print("Called AI in fight, time = %s, elapsed time = %s" % (call_time, call_time - self.last_call_to_ai))
            self.last_call_to_ai = call_time
            random_number = random.random()
            
            if opponent.attacking:
                if random_number < self.fight_logic["block_prob"]:
                    ai_control = opponent.state
                elif random_number < (self.fight_logic["block_prob"] + self.fight_logic["riposte_prob"]):
                    if opponent.state == "attack_low":
                        ai_control = "attack_mid"
                    elif opponent.state == "attack_mid":
                        ai_control = "attack_high"
                    elif opponent.state == "attack_high":
                        ai_control = "attack_low"
                    else:
                        raise Exception("Opponent is not attacking...")
            else:
                if random.random() < self.fight_logic["attack_prob"]:
                    if random_number < self.fight_logic["low_attack_prob"]:
                        ai_control = "attack_low"
                    elif random_number < (self.fight_logic["low_attack_prob"] + self.fight_logic["mid_attack_prob"]):
                        ai_control = "attack_mid"
                    else:
                        ai_control = "attack_high"
        
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