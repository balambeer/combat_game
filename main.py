import sys
import pygame as pg
import settings
from menu import *
from player import *

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
        
        self.player = Player(self,
                             (100, int(1.25 * settings.sky_proportion * settings.screen_height)), # TODO: placeholder
                             settings.movement_speed,
                             "assets/sprites/fighter_1/",
                             settings.animation_speed)
    
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
        if self.check_game_over_condition():
            self.menu.update_at_game_over()
            self.game_over = True
        else:
            self.delta_time = self.clock.tick(settings.fps)
            self.player.update()
        
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')

    # Update screen
    def draw_background(self):
        sky_height = int(settings.sky_proportion * settings.screen_height)
        pg.draw.rect(self.screen,
                     "lightskyblue1",
                     pg.Rect(0, 0, settings.screen_width, sky_height))
        pg.draw.rect(self.screen,
                     "olivedrab3",
                     pg.Rect(0, sky_height,
                             settings.screen_width, settings.screen_height - sky_height))
        
    
    def draw(self):
        pg.display.flip()
        self.draw_background()
        self.player.draw()
        
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

