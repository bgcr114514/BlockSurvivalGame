import pygame
import random
from math import sin, cos, radians
from utils import *
from const import *

AUDIO = get_all_audio()
IMAGE = get_all_image()
class Smoke:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(10, 30) 
        self.lifetime = random.randint(50, 100) 
        self.angle = random.uniform(0, 360)  
        self.speed = random.uniform(1, 5)  
        self.alpha = 3   
        self.start_time = get_current_time()

    def update(self,wind_speed = 0):
        self.x += self.speed * cos(radians(self.angle))*random.uniform(0.7, 1.3)
        self.y += self.speed * sin(radians(self.angle))
        self.x -= wind_speed*random.uniform(0.3, 1)*min(((get_current_time() - self.start_time)/1000),1)*0.7
        self.y -= random.randint(1,5)
        self.alpha -= 50 if self.alpha > 50 else 0 
        self.speed *= 0.95
            
            
        self.size += 0.5 if self.size < 50 else 0
        self.lifetime -= 0.5

        
            


    def draw(self, surface:pygame.Surface):
        
        rect = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(rect, (255, 255, 255, self.alpha), (int(self.size), int(self.size)), int(self.size))
        surface.blit(rect, (int(self.x - self.size), int(self.y - self.size)))


class SmokeEmitter:
    def __init__(self, x, y,surface = None):
        self.x = x
        self.y = y
        self.particles:list[Smoke] = []
        self.emit()
        self.dust_list = []
        self.start_time = get_current_time()
        for i in range(random.randint(3,9)):
            self.dust_list .append(\
                [self.x,self.y,random.randint(-3,3),random.randint(4,8),random.randint(2,4),random.randint(100,200)])
        AUDIO['firecraker'].play()

    def emit(self):
        for _ in range(random.randint(50, 80)): 
            self.particles.append(Smoke(self.x, self.y))

    def update(self,wind_speed = 0):
        for particle in self.particles:
            particle.update(wind_speed)
            if particle.lifetime <= 0 or particle.alpha <= 0 :
                self.particles.remove(particle)
        for i in self.dust_list:
            i[0] += i[2]
            i[1] -= i[3]
            i[3] -= GRAVITY
            i[5] -= 10
            if i[5] <= 0:
                self.dust_list.remove(i)
            

        self.particles = [particle for particle in self.particles if particle.lifetime > 0]

    def draw(self, surface:pygame.Surface):
        if get_current_time() - self.start_time < 200:
            
            surface.blit(IMAGE["firecraker_bg"],(int(self.x)-70, int(self.y)-70))
            pygame.draw.circle(surface, (144, 144, 144), (int(self.x), int(self.y)), random.randint(10,20))
        for particle in self.particles:
            particle.draw(surface)
        for i in self.dust_list:
            pygame.draw.rect(surface,(0,0,0),pygame.Rect(i[0],i[1],i[4],i[4]))



