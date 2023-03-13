import pygame as pg
import settings

class Button():
    def __init__(self, game,
                 center_position,
                 text,
                 text_color,
                 idle_color,
                 clicked_color):
        self.game = game
        
        self.pressed = False
        
        self.text_color = text_color
        self.idle_color = idle_color
        self.clicked_color = clicked_color
        
        self.current_color = self.idle_color
        self.text = text
        self.text_rendered = self.game.font.render(text, False, self.text_color)
        self.text_rect = self.text_rendered.get_rect(center = (int(center_position[0] * settings.resolution[0]),
                                                               int(center_position[1] * settings.resolution[1])))
        
        self.background_rect = self.text_rect.inflate(0.1 * self.text_rendered.get_width(),
                                                      0.1 * self.text_rendered.get_height())
        
    def draw(self):
        pg.draw.rect(self.game.screen, self.current_color, self.background_rect)
        pg.draw.rect(self.game.screen, self.text_color, self.background_rect, int(0.1 * self.text_rendered.get_height()))
        self.game.screen.blit(self.text_rendered, self.text_rect)
        
    def is_left_clicked(self):
        if pg.mouse.get_pressed()[0]:
            if self.background_rect.collidepoint(pg.mouse.get_pos()):
                self.pressed = True
        if self.pressed:
            if not pg.mouse.get_pressed()[0]:
                self.pressed = False
                return self.background_rect.collidepoint(pg.mouse.get_pos())
            
class ButtonNewGame(Button):
    def __init__(self, game,
                 center_position = (0.5, 0.6),
                 text = "New Game",
                 text_color = settings.menu_button_color,
                 background_color = settings.menu_background_color,
                 clicked_color = settings.menu_background_color):
        super().__init__(game, center_position, text, text_color, background_color, clicked_color)
        
    def listen(self):
        if self.is_left_clicked():
            self.game.new_game()
        
class Menu():
    def __init__(self, game):
        self.game = game
        
        self.game_title = self.game.font.render("Combat Game", False, settings.menu_text_color)
        self.game_title_rect = self.game_title.get_rect(center = (0.5 * settings.screen_width, 0.2 * settings.screen_height))
        
        self.new_game_button = ButtonNewGame(self.game)
        
    def draw(self):
        pg.display.flip()
        self.game.screen.fill(settings.menu_background_color)
        self.game.screen.blit(self.game_title, self.game_title_rect)
        self.new_game_button.draw()
        
    def update_at_game_over(self):
        pg.mouse.set_visible(True)
        pg.mouse.set_pos((0.5 * settings.screen_width, 0.9 * settings.screen_height))
            
    def listen_to_inputs(self):
        self.new_game_button.listen()
        
