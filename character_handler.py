import pygame as pg
from player import *
from npc import *

class CharacterHandler():
    def __init__(self, game):
        self.game = game
        self.enemy_list = []
        self.dead_enemy_list = []
        self.fight_list = []
        
        self.player = Player(self.game,
                             ( int(0.2 * settings.screen_width),
                               int(1.25 * settings.sky_proportion * settings.screen_height) ),
                             False
                            ) # TODO: placeholder

        self.enemy_list.append(
            NPC(self.game,
                ( int(0.8 * settings.screen_width),
                  int(1.25 * settings.sky_proportion * settings.screen_height) ),
                True
                ) # TODO: placeholder
            )
        
    def resolve_fight_with_enemy(self, enemy):
        if self.player.attacking:
            if enemy.rect.colliderect(self.player.image_rect):
                enemy.pain = True
                self.player.attacking = False
        if enemy.attacking:
            if self.player.rect.colliderect(enemy.image_rect):
                self.player.pain = True
                enemy.attacking = False
                
    def resolve_fights(self):
        for fighting_enemy in self.fight_list:
            self.resolve_fight_with_enemy(fighting_enemy)
        
    def update_lists(self):
        for enemy in self.enemy_list:
            if enemy.dead and enemy.image_counter == 0:
                self.dead_enemy_list.append(enemy)
                self.enemy_list.remove(enemy)
            if enemy.in_fight(self.player) and len(self.fight_list) == 0:
                self.fight_list.append(enemy)
                self.enemy_list.remove(enemy)
        for enemy in self.fight_list:
            if enemy.dead and enemy.image_counter == 0:
                self.dead_enemy_list.append(enemy)
                self.fight_list.remove(enemy)
            if not enemy.in_fight(self.player):
                self.enemy_list.append(enemy)
                self.fight_list.remove(enemy)
        
    def update(self):
        self.update_lists()
        
        if len(self.fight_list) == 0:
            self.player.update(None)
        else:
            # Player reacts to only the 1st enemy in the fight_list
            self.player.update(self.fight_list[0])
        for enemy in self.enemy_list:
            enemy.update(None)
        for enemy in self.fight_list:
            enemy.update(self.player)
            self.resolve_fight_with_enemy(enemy)
            
    def draw(self):
        self.player.draw()
        for enemy in self.enemy_list:
            enemy.draw()
        for dead_enemy in self.dead_enemy_list:
            dead_enemy.draw()
        for fighting_enemy in self.fight_list:
            fighting_enemy.draw()