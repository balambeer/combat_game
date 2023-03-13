import sys
import pygame as pg
import settings
from menu import *

class Game:
    # Constructor
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.resolution)
        self.font = pg.font.Font(None, settings.font_size)
        self.game_over = True
        self.game_over_frames = 0
        self.menu = Menu(self)
        
    def new_game(self):
        self.game_over = False
        self.clock = pg.time.Clock()
        self.delta_time = 0
    
    # Check events
    def check_for_quit(self, event):
        return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
    
    def check_events(self):
        for event in pg.event.get():
            if self.check_for_quit(event):
                pg.quit()
                sys.exit()
                
    # Update game state
    def check_game_over_condition(self):
        return pg.mouse.get_pressed()[0]
    
    def update_game_state(self):
        self.delta_time = self.clock.tick(settings.fps)
        
        if self.check_game_over_condition():
            self.menu.update_at_game_over()
            self.game_over = True
        
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')

    # Update screen
    def draw(self):
        pg.display.flip()
        self.screen.fill('gray')      
        
    # main funciton
    def run(self):
        while True:
            self.check_events()
            if not self.game_over:
                self.update_game_state()
                self.draw()
            else:              
                self.menu.draw()
                self.menu.listen_to_inputs()
            
if __name__ == '__main__':
    game = Game()
    game.run()

