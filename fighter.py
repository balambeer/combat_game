import pygame as pg
from support import import_folder

class Fighter():
    def __init__(self, game,
                 start_pos,
                 movement_speed,
                 max_health,
                 path,
                 animation_speed,
                 color):
        self.game = game
        
        # sprites
        self.load_sprites(path)
        self.image = self.sprites["idle"][0]
        
        # fighter representation
        self.state = "idle"
        self.attacking = False
        self.changed_state = False
        self.rect = pg.Rect((start_pos[0] - self.image.get_width() // 2, start_pos[1] - self.image.get_height()),
                            (self.image.get_width(), self.image.get_height()))
        self.facing_left = True
        self.movement_speed = movement_speed
        self.health = max_health
        
        # animation
        self.image_rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.image_counter = 0
        self.animation_speed = animation_speed
        self.time_since_last_frame = 0
        
        # debug
        self.color = color
        
    def load_sprites(self, path):
        self.sprites = { "idle": [], "move": [], "attack": [] }
        self.n_images = { "idle": 0, "move": 0, "attack": 0 }
        
        for state in self.sprites.keys():
            folder_path = path + state
            self.sprites[state] = import_folder(folder_path)
            self.n_images[state] = len(self.sprites[state])
    
    def update_changed_state(self, control_input):
        if self.state == control_input:
            self.changed_state = False
        else:
            self.changed_state = True
    
    def update_state(self, control_input):
        if self.state == "idle":
            self.update_changed_state(control_input)
            
            if control_input == "move":
                self.image_counter = 0                
                self.state = "move"
            elif control_input == "turn":
                self.facing_left = not self.facing_left
            elif control_input == "attack":
                self.attacking = True
                self.image_counter = 0
                self.state = "attack"
            elif control_input == "idle":
                self.image_counter = 0
                self.state = "idle"
        elif self.state == "attack" or self.state == "move":
            if self.image_counter == 0:
                self.state = "idle"
                
    def update_position(self):
        if self.state == "move":
            if self.facing_left:
                self.rect.x -= self.movement_speed // self.n_images["move"]
            else:
                self.rect.x += self.movement_speed // self.n_images["move"]
    
    def animate(self):
        self.time_since_last_frame += self.game.delta_time
        if self.time_since_last_frame > self.animation_speed or self.changed_state:
            self.image_counter = (self.image_counter + 1) % self.n_images[self.state]
            self.time_since_last_frame = 0
            
            self.image = self.sprites[self.state][self.image_counter]
            if self.state == "attack":
                if self.facing_left:
                    self.image_rect = self.image.get_rect(bottomright = self.rect.bottomright)
                else:
                    self.image_rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            else:
                self.image_rect = self.image.get_rect(center = self.rect.center)
        
#     def update_health(self, enemy):
#         if enemy.attacking:
#             if self.rect.colliderect(enemy.image_rect):
#                 self.health -= 1
#                 print("Ouch. New health = %i" % self.health)
#                 
#     def did_i_hit(self, enemy):
#         if self.attacking:
#             if self.image_rect.colliderect(enemy.rect):
#                 self.attacking = False
        
    def update(self, control_input, enemy):
        self.update_state(control_input)
        self.update_position()
        self.animate()
#         self.update_health(enemy)
#         self.did_i_hit(enemy)
        
    def draw(self):
        self.game.screen.blit(self.image, self.image_rect)
        pg.draw.rect(self.game.screen,
                     self.color,
                     self.rect,
                     width = 2)