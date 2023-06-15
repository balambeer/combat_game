import pygame as pg
import settings
from support import import_folder, CSVTable

class Fighter():
    def __init__(self, game,
                 start_pos,
                 start_facing_left,
                 identifier,
                 movement_distance,
                 max_health,
                 path,
                 animation_speed,
                 draw_health_default,
                 draw_health_left,
                 color):
        self.game = game
        self.id = identifier
        
        # sprites
        self.load_sprites(path)
        self.image = self.sprites["idle"][0]
        
        # animation
        self.animation_speed = animation_speed
        
        # fighter representation
        self.state = "idle"
        self.attack_state = "none"
        self.pain = False
        self.changed_state = False
        self.rect = pg.Rect((start_pos[0] - self.image.get_width() // 2, start_pos[1] - self.image.get_height()),
                            (self.image.get_width(), self.image.get_height()))
        self.facing_left = start_facing_left
        self.movement_speed = movement_distance // int(settings.fps * self.n_images["walk"] * self.animation_speed / 1000 )
        self.health = max_health
        
        self.load_attack_state_lims(path)
        
        # animation
        self.image_rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.image_counter = 0
        self.time_since_last_frame = 0
        
        self.to_fight = False
        self.to_normal = False
        
        # health bar
        self.display_health = draw_health_default
        self.draw_health_left = draw_health_left
        self.heart_image = pg.image.load("assets/sprites/generic/heart.png").convert_alpha()
        self.heart_image_width = self.heart_image.get_width()
        
        # debug
        self.color = color
        
    def load_sprites(self, path):
        self.sprites = { "idle": [],
                         "to_fight": [],
                         "to_normal": [],
                         "walk": [],
                         "turn": [],
                         "shift_forward": [],
                         "shift_backward": [],
                         "attack_low": [],
                         "attack_mid": [],
                         "attack_high": [],
                         "block": [],
                         "pain": [],
                         "death": [] }
        self.n_images = { "idle": 0,
                          "to_fight": 0,
                          "to_normal": 0,
                          "walk": 0,
                          "turn": 0,
                          "shift_forward": 0,
                          "shift_backward": 0,
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
            
    def load_attack_state_lims(self, path):
        csv_table = CSVTable(path + "attack_state_lims.csv")
        self.attack_state_lims = {}
        for row in csv_table.table:
            telegraph_lim = int(row[csv_table.col_index["telegraph_lim"]])
            attack_lim = int(row[csv_table.col_index["attack_lim"]])
            self.attack_state_lims.update({row[csv_table.col_index["name"]]: {"telegraph": telegraph_lim, "attack": attack_lim}})
           
    @property
    def attacking(self):
        return (self.state == "attack_low" or self.state == "attack_mid" or self.state == "attack_high")
    
    @property
    def dead(self):
        return self.health <= 0
    
    @property
    def game_over_condition_met(self):
        return (self.dead and self.image_counter == 0)
    
    def in_fight(self, opponent):
        return (not opponent.dead and abs(self.rect.x - opponent.rect.x) < settings.fight_distance)
    
    def update_state_in_fight(self, control_input, opponent):
        
        if self.pain:
            if self.dead:
                self.state = "death"
            else:
                self.state = "pain"
            self.image_counter = 0
            self.changed_state = True
            self.pain = False
        elif self.state == "block":
            if (opponent.attack_state == "recovery" or opponent.attack_state == "none"):
                if self.attack_state == "riposte":
                    if opponent.state == "attack_low":
                        self.state = "attack_mid"
                    elif opponent.state == "attack_mid":
                        self.state = "attack_high"
                    elif opponent.state == "attack_high":
                        self.state = "attack_low"
                    else:
                        raise Exception("Opponent is not attacking...")
                    self.attack_state = "none"
                else:
                    self.state = "idle"
                    
                self.image_counter = 0
                self.changed_state = True
        elif self.state == "idle":
            if self.to_fight:
                self.state = "to_fight"
                self.image_counter = 0
                self.changed_state = True
                self.to_fight = False
            elif ( control_input == "shift_forward" or
                   control_input == "shift_backward"):
                self.state = control_input
                self.image_counter = 0
                self.changed_state = True
            # Attacks are resolved based on opponents state
            elif (control_input == "attack_low" or
                 control_input == "attack_mid" or
                 control_input == "attack_high" ):
                if opponent.attacking:
                    if opponent.attack_state == "telegraph":
                        if control_input == opponent.state:
                            self.state = "block"
                        elif ( (control_input == "attack_mid" and opponent.state == "attack_low") or
                               (control_input == "attack_high" and opponent.state == "attack_mid") or
                               (control_input == "attack_low" and opponent.state == "attack_high") ):
                            self.state = "block"
                            self.attack_state = "riposte"
                else:
                    self.state = control_input
                
                self.image_counter = 0
                self.changed_state = True
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
            if self.to_normal:
                self.state = "to_normal"
                self.image_counter = 0
                self.changed_state = True
                self.to_normal = False
            elif ( control_input == "walk" or
                   control_input == "turn" or
                   control_input == "attack_low" or
                   control_input == "attack_mid" or
                   control_input == "attack_high" ):
                self.state = control_input
                self.image_counter = 0
                self.changed_state = True
        else:
            if self.image_counter == 0:
                self.state = "idle"
                
    def update_attack_state(self):
        if self.attacking:
            attack_mode = self.state.split("_")[1]
            if ( (self.attack_state == "none" or self.attack_state == "telegraph") and
                 1 <= self.image_counter and
                 self.image_counter <= self.attack_state_lims[attack_mode]["telegraph"] ):
                self.attack_state = "telegraph"
            elif ( (self.attack_state == "telegraph" or self.attack_state == "attack") and
                   1 <= self.image_counter and
                   self.image_counter <= self.attack_state_lims[attack_mode]["attack"] ):
                self.attack_state = "attack"
            else:
                self.attack_state = "recovery"
        elif not (self.state == "block" and self.attack_state == "riposte"):
            self.attack_state = "none"
                
    def update_position_and_facing(self):
        if (self.state == "walk" or self.state == "shift_forward"):
            if self.facing_left:
                self.rect.x -= self.movement_speed
            else:
                self.rect.x += self.movement_speed
        if (self.state == "shift_backward"):
            if self.facing_left:
                self.rect.x += self.movement_speed
            else:
                self.rect.x -= self.movement_speed
        if self.state == "turn" and self.image_counter == 0:
            self.facing_left = not self.facing_left
                
    def update_health(self):
        if self.pain:
            self.health -= 1
            print("Ouch. New health = %i" % self.health)
    
    def animate(self):
        self.time_since_last_frame += self.game.delta_time
        if self.time_since_last_frame > self.animation_speed or self.changed_state:
            
            if not (self.state == "block" and self.image_counter == 0 and not self.changed_state):
                self.image_counter = (self.image_counter + 1) % self.n_images[self.state]
            self.time_since_last_frame = 0
            
            self.image = self.sprites[self.state][self.image_counter]
            if self.attacking:
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
                
            self.update_attack_state()
        
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
        
    def draw_health(self):
        if self.display_health:
            offset = int(settings.health_bar_offset * settings.screen_width)
            y_topleft = offset
            if self.draw_health_left:
                x_topleft = offset
                for i in range(self.health):
                    self.game.screen.blit(self.heart_image, (x_topleft, y_topleft))
                    x_topleft += self.heart_image_width // 2
            else:
                x_topleft = settings.screen_width - offset - self.heart_image_width
                for i in range(self.health):
                    self.game.screen.blit(self.heart_image, (x_topleft, y_topleft))
                    x_topleft -= self.heart_image_width // 2
        
    def draw(self):
        self.draw_health()
        self.game.screen.blit(self.image, self.image_rect)
        pg.draw.rect(self.game.screen,
                     self.color,
                     self.rect,
                     width = 2)