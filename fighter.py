import pygame as pg
import settings
from support import import_folder

class Fighter():
    def __init__(self, game,
                 start_pos,
                 start_facing_left,
                 movement_distance,
                 max_health,
                 path,
                 animation_speed,
                 color):
        self.game = game
        
        # sprites
        self.load_sprites(path)
        self.image = self.sprites["idle"][0]
        
        # animation
        self.animation_speed = animation_speed
        
        # fighter representation
        self.state = "idle"
        self.attacking = False
        self.pain = False
        self.changed_state = False
        self.rect = pg.Rect((start_pos[0] - self.image.get_width() // 2, start_pos[1] - self.image.get_height()),
                            (self.image.get_width(), self.image.get_height()))
        self.facing_left = start_facing_left
        self.movement_speed = movement_distance // int(settings.fps * self.n_images["move"] * self.animation_speed / 1000 )
        self.health = max_health
        
        # print(self.movement_speed)
        
        # animation
        self.image_rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.image_counter = 0
        self.time_since_last_frame = 0
        
        # debug
        self.color = color
        
    def load_sprites(self, path):
        self.sprites = { "idle": [],
                         "move": [],
                         "turn": [],
                         "attack_low": [],
                         "attack_mid": [],
                         "attack_high": [],
                         "block": [],
                         "pain": [],
                         "death": [] }
        self.n_images = { "idle": 0,
                          "move": 0,
                          "turn": 0,
                          "attack_low": 0,
                          "attack_mid": 0,
                          "attack_high": 0,
                          "block": 0,
                          "pain": 0,
                          "death": 0 }
        
        for state in self.sprites.keys():
            folder_path = path + state
            self.sprites[state] = import_folder(folder_path)
            self.n_images[state] = len(self.sprites[state])
            
    @property
    def telegraphing(self):
        return (self.state == "attack_low" or self.state == "attack_mid" or self.state == "attack_high") and self.image_counter <= settings.telegraphing_limit
    
    @property
    def dead(self):
        return self.health <= 0
    
    def in_fight(self, opponent):
        return abs(self.rect.x - opponent.rect.x) < settings.fight_distance
    
    def update_state_in_fight(self, control_input, opponent):
        
        if self.pain:
            if self.dead:
                self.state = "death"
            else:
                self.state = "pain"
            self.image_counter = 0
            self.changed_state = True
            self.pain = False
        elif self.state == "idle":
            if ( control_input == "move" or
                 control_input == "turn" or
                 control_input == "attack_low" or
                 control_input == "attack_mid" or
                 control_input == "attack_high" ):
                self.state = control_input
                self.image_counter = 0
                self.changed_state = True
                
                if ( control_input == "attack_low" or
                     control_input == "attack_mid" or
                     control_input == "attack_high" ):
                    self.attacking = True
        else:
            if self.image_counter == 0:
                self.state = "idle"
    
    def update_state_not_in_fight(self, control_input):
        
        if self.pain:
            if self.dead:
                self.state = "death"
            else:
                self.state = "pain"
            self.image_counter = 0
            self.changed_state = True
            self.pain = False
        elif self.state == "idle":
            if ( control_input == "move" or
                 control_input == "turn" or
                 control_input == "attack_low" or
                 control_input == "attack_mid" or
                 control_input == "attack_high" ):
                self.state = control_input
                self.image_counter = 0
                self.changed_state = True
                
                if ( control_input == "attack_low" or
                     control_input == "attack_mid" or
                     control_input == "attack_high" ):
                    self.attacking = True
        else:
            if self.image_counter == 0:
                self.state = "idle"
                
    def update_position_and_facing(self):
        if self.state == "move":
            if self.facing_left:
                self.rect.x -= self.movement_speed
            else:
                self.rect.x += self.movement_speed
            # print(self.rect.x)
        if self.state == "turn" and self.image_counter == 0:
            self.facing_left = not self.facing_left
#             if self.facing_left:
#                 print("facing left")
#             else:
#                 print("facing right")
                
    def update_health(self):
        if self.pain:
            self.health -= 1
            print("Ouch. New health = %i" % self.health)
    
    def animate(self):
        self.time_since_last_frame += self.game.delta_time
        if self.time_since_last_frame > self.animation_speed or self.changed_state:
            
            self.image_counter = (self.image_counter + 1) % self.n_images[self.state]
            self.time_since_last_frame = 0
            
            self.image = self.sprites[self.state][self.image_counter]
            if self.state == "attack_low" or self.state == "attack_mid" or self.state == "attack_high":
                if self.facing_left:
                    self.image_rect = self.image.get_rect(bottomright = self.rect.bottomright)
                else:
                    self.image_rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            elif self.state == "death":
                if self.facing_left:
                    self.image_rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
                else:
                    self.image_rect = self.image.get_rect(bottomright = self.rect.bottomright)
            else:
                self.image_rect = self.image.get_rect(center = self.rect.center)
        
    def update(self, control_input, opponent):
        self.changed_state = False
        if not self.dead:
            self.update_health()
            if opponent == None:
                self.update_state_not_in_fight(control_input)
            else:
                self.update_state_in_fight(control_input, opponent)
            self.update_position_and_facing()
        self.animate()
        
    def draw(self):
        self.game.screen.blit(self.image, self.image_rect)
        pg.draw.rect(self.game.screen,
                     self.color,
                     self.rect,
                     width = 2)