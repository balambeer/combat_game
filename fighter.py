import pygame as pg
from support import import_folder

class Fighter():
    def __init__(self, game,
                 start_pos,
                 path):
        self.game = game
        self.state = "idle"
        
        self.load_sprites(path)
        self.image = self.sprites["idle"][0]
        self.rect = pg.Rect((start_pos[0], start_pos[1] - self.image.get_height()),
                            (self.image.get_width(), self.image.get_height()))
        self.image_rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
        
    def load_sprites(self, path):
        self.sprites = { "idle": [], "move": [], "attack": [] }
        
        for state in self.sprites.keys():
            folder_path = path + state
            self.sprites[state] = import_folder(folder_path)
            
    def animate(self):
        self.image = self.sprites["idle"][0]
        self.image_rect = self.image.get_rect(center = self.rect.center)
        
    def update(self):
        self.animate()
        
    def draw(self):
        self.game.screen.blit(self.image, self.image_rect)