import math

import pygame
import sympy

from utils import *

IMAGE = get_all_image()

class Missile(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, vx,vy,effect = None,friendly:bool=True):
        super().__init__()
        self.image = pygame.transform.scale(IMAGE[image_name],MISSILE_TRANSFROM)
        self.image_name= image_name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.friendly = friendly
        self._friendly = friendly
        self.effect = effect
        self.start_time = get_current_time()
        x1,y1 = sympy.symbols('x y')
        if vy !=0:
            eq1 = sympy.Eq(x1/y1,vx/vy)
        else:
            eq1 = sympy.Eq(x1/y1,vx/(vy+1))
        eq2 = sympy.Eq(sympy.sqrt(x1**2+y1**2),15)
        e = sympy.solve((eq1,eq2),(x1,y1))
        if len(e) == 2:
            if vx>0 and e[1][0] >0:
                self.vx = e[1][0]
                self.vy = e[1][1]
            else:
                self.vx = e[0][0]
                self.vy = e[0][1]
        '''self.vx = vx
        self.vy = vy'''
        self.move_missile()
        self.move_angle(self.vx,self.vy)
        self.image = pygame.transform.rotate(pygame.transform.scale(IMAGE[image_name],MISSILE_TRANSFROM),self.angle)  
    def update(self,player):
        self.move_missile()
        self.move_angle(self.vx,self.vy)
        if self.rect.top>=HEIGHT or self.rect.bottom<=0 or\
            self.rect.left>=WIDTH or self.rect.right <=0:
            self.kill()
        if not self._friendly and self.rect.colliderect(player.rect):
            self._friendly = True
        else:
            self._friendly = False


    def move_missile(self):
        self.rect.x+=self.vx
        self.rect.y-=self.vy
        self.vy-=0.75
    def move_angle(self,vx,vy):
        if vy == 0:
            self.angle = 90 if vx >0 else -90
        else:
            self.angle =  math.atan(vx/-vy)*57.2957
            
            if vy >0:
                if vx>=0:
                    self.angle += 180
                elif vx<0:
                    self.angle += -180     
        self.angle+=135
        self.image = pygame.transform.rotate(pygame.transform.scale(IMAGE[self.image_name],MISSILE_TRANSFROM),self.angle) 