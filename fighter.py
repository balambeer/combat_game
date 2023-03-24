import pygame as pg
from support import import_folder

class Fighter():
    def __init__(self, game,
                 start_pos,
                 movement_speed,
                 path,
                 animation_speed):
        self.game = game
        
        # sprites
        self.load_sprites(path)
        self.image = self.sprites["idle"][0]
        
        # fighter representation
        self.state = "idle"
        self.changed_state = False
        self.rect = pg.Rect((start_pos[0], start_pos[1] - self.image.get_height()),
                            (self.image.get_width(), self.image.get_height()))
        self.facing_left = True
        self.movement_speed = movement_speed
        
        # animation
        self.image_rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.image_counter = 0
        self.animation_speed = animation_speed
        self.time_since_last_frame = 0               
        
    def load_sprites(self, path):
        self.sprites = { "idle": [], "move": [], "attack": [] }
        self.n_images = { "idle": 0, "move": 0, "attack": 0 }
        
        for state in self.sprites.keys():
            folder_path = path + state
            self.sprites[state] = import_folder(folder_path)
            self.n_images[state] = len(self.sprites[state])
    
    @property
    def taking_inputs(self):
        return (self.state == "idle" or self.state == "move")
    
    def update_changed_state(self, control_input):
        if self.state == control_input:
            self.changed_state = False
        else:
            self.changed_state = True
    
    def update_state(self, control_input):
        print("Taking inputs = %s" % self.taking_inputs)
        if self.taking_inputs:
            self.update_changed_state(control_input)
            
            if control_input == "move":
                if not self.state == "move":
                    self.image_counter = 0                
                self.state = "move"
                if self.facing_left:
                    self.rect.x -= self.movement_speed
                else:
                    self.rect.x += self.movement_speed
            elif control_input == "turn":
                self.facing_left = not self.facing_left
            elif control_input == "attack":
                self.image_counter = 0
                self.state = "attack"
            elif control_input == "idle":
                self.image_counter = 0
                self.state = "idle"
        elif self.state == "attack":
            if self.image_counter == 0:
                self.state = "idle"
    
    def animate(self, control_input):
        self.time_since_last_frame += self.game.delta_time
        if self.time_since_last_frame > self.animation_speed or self.changed_state:
            self.image_counter = (self.image_counter + 1) % self.n_images[self.state]
            self.time_since_last_frame = 0
        
            if self.state == "attack":
                print("state = %s" % self.state)
                print("image_counter = %i" % self.image_counter)
            
            self.image = self.sprites[self.state][self.image_counter]
            if self.state == "attack":
                if self.facing_left:
                    self.image_rect = self.image.get_rect(bottomright = self.rect.bottomright)
                else:
                    self.image_rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            else:
                self.image_rect = self.image.get_rect(center = self.rect.center)
        
    def update(self, control_input):
        self.update_state(control_input)
        self.animate(control_input)
        
#         print(self.rect.x)
#         print(self.image_rect.x)
        
    def draw(self):
        self.game.screen.blit(self.image, self.image_rect)
        pg.draw.rect(self.game.screen,
                     "orchid3",
                     self.rect,
                     width = 2)