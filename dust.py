import random

from const import *
from utils import *

IMAGE:dict[str,pygame.Surface] = get_all_image()
class Dust:
    def __init__(self,speed_x:int) -> None:
        self.x = 0 if speed_x<=0 else WIDTH
        self.y = random.randint(0,HEIGHT)
        self.image_name = 'dust'
        #self.image = IMAGE[self.image_name]
    def move(self,speed_x:int) -> None:
        if (self.x>=0 and speed_x>=0) or (self.x<=WIDTH and speed_x<=0):
            self.x-=speed_x
            self.y+=random.randrange(-5,5)
        else:
            self.x = WIDTH if speed_x>=0 else 0
            self.y = random.randint(0,HEIGHT)


    def draw(self,surface:pygame.Surface) -> None:
        #surface.blit(self.image,(self.x,self.y))
        pygame.draw.rect(surface, '#585858',
        pygame.Rect(self.x,self.y,5,5))