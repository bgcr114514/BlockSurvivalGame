import pygame
from pygame.math import Vector2

from const import *
from player import *
from utils import *

IMAGE = get_all_image()
class Barrage(pygame.sprite.Sprite):
    def __init__(self,
                ai_type:str,
                image_name:str,
                x:int,
                y:int,
                player_class:Player,
                friendly:bool=False,
                aggression:bool=False,
                hurt:int = 0,
                retention_time:int=1000,
                eff:str = "",
                eff_time:int = 0,
                ):
        super().__init__()
        self.type:str = ai_type
        self.start_time = get_current_time()
        self.retention_time = retention_time
        self.image_name:str = image_name
        self.image:pygame.Surface = IMAGE[self.image_name]
        self.rect:pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.friendly = friendly     #Is just hurt player, it means 是否友善
        self.aggression = aggression     #Is just hurt enemy and boss. it means 是否伤害敌怪,False:not,True:yes
        self.hurt = 0 if not (not self.friendly or self.aggression) else hurt

        self.eff = eff
        self.eff_time = eff_time
        if self.type == 'to_player_sprint':
            self.dx = player_class.rect.x - self.rect.x
            self.dy = player_class.rect.y - self.rect.y
            self.image = pygame.transform.rotate(self.image,\
                    ((pygame.math.Vector2(1,0).angle_to(\
                        (player_class.rect.x-self.rect.x,player_class.rect.y-self.rect.y)))+150)*-1)
            self.image.get_rect(center=self.image.get_rect(center=(Vector2(self.rect.center).x, Vector2(self.rect.center).y)).center)
    def update(self,player_group:pygame.sprite.Group,enemy:pygame.sprite.Group):


        player_class:Player = player_group.sprites()[0]
        if self.retention_time<=get_current_time()-self.start_time:
            self.kill()
            
        
        if not self.friendly:
                    if pygame.sprite.spritecollideany(self,player_group):
                        player_class.life-=self.hurt
                        get_all_audio()['player_hurt'].play()
                        self.kill()
        elif self.aggression:
            if pygame.sprite.spritecollideany(self,enemy):
                for eny in enemy.sprites():
                    eny.life-=self.hurt
                    

        if self.type == 'to_player_sprint':
            self.is_kill()
            self.dx = player_class.rect.x - self.rect.x
            self.dy = player_class.rect.y - self.rect.y
            self.image = pygame.transform.rotate(IMAGE[self.image_name],\
                        ((pygame.math.Vector2(1,0).angle_to(\
                            (player_class.rect.x-self.rect.x,player_class.rect.y-self.rect.y)))+150)*-1)
            self.image.get_rect(center=self.image.get_rect(center=(Vector2(self.rect.center).x, Vector2(self.rect.center).y)).center)
                
            self.rect.x += self.dx/30
            self.rect.y += self.dy/30
        elif self.type == "drop_item":
            if self.rect.top>=HEIGHT:
                self.kill()
            self.rect.y+=10
        
    def is_kill(self):
         if self.rect.left>=WIDTH or self.rect.right<=0 or self.rect.top>=HEIGHT or self.rect.bottom<=0:
            self.kill()

        

