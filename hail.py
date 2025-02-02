import random

from const import *
from utils import *

IMAGE = get_all_image()
class Hail(pygame.sprite.Sprite):
    def __init__(self,surface):
        super().__init__()
        self.image:pygame.Surface = IMAGE['hail']
        self.rect:pygame.Rect = self.image.get_rect()
        self.rect.x = random.randint(-100, WIDTH + 100)
        self.rect.y = random.randint(-100, -50)
        self.speed_y = 1

        self.surface = surface

    def update(self,is_ending,speed_x,player,block,tile):
        self.rect.y += abs(speed_x)+self.speed_y
        self.speed_y+=1
        self.rect.x -= speed_x
        is_meet_player = pygame.sprite.spritecollideany(self,player)
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y > HEIGHT or is_meet_player or\
            pygame.sprite.spritecollideany(self,block) or pygame.sprite.spritecollideany(self,tile):
            self.initialization(is_ending)
            if is_meet_player:
                player.sprites()[0].life-=3
            
            
        if is_ending:
            del self
    def initialization(self,is_ending) -> None:
        if not is_ending:
            self.rect.x = random.randint(-100, WIDTH + 100)
            self.rect.y = random.randint(-100, -50)
            self.speed_y = 1
            self.size = random.randint(1, 2)
