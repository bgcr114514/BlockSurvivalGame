import pygame.mouse
from pygame.locals import *

from utils import *

IMAGE = get_all_image()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMAGE['player']
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.speed_x = 0
        self.speed_y = 0
        self.press_space = False
        self.run_time= get_current_time()
        self.jump_num = 0
        self.max_jump_num = 1
        self.image_name = 'player'
        self.dir = 'right'
        self.last_move_arm = get_current_time()-500
        self.life = 100
        self.max_life = 100
        self.last_hurt = get_current_time()-500
        self.max_speed_y = 30
        self.is_x_gone = False
        self.l_x = not self.is_x_gone
    def update(self,eff:list) -> tuple:
        # self.speed_x = floor(self.speed_x*0.8)
        
        mouse = pygame.mouse.get_pressed()[0]
        keys = pygame.key.get_pressed()
        if get_current_time()-self.last_move_arm<=MOVE_ARM_TIME or(mouse and get_current_time()-self.last_move_arm>=MOVE_ARM_SLEEP_TIME):
            self.image_name = 'player_move_arm'
            if mouse and get_current_time()-self.last_move_arm>=MOVE_ARM_TIME:
                self.last_move_arm = get_current_time()

        else:
            self.image_name = 'player'
        self.image = pygame.transform.flip(IMAGE[self.image_name], True, False) if self.dir == 'right' else \
            IMAGE[self.image_name]
        
        if keys[K_a]:
            self.speed_x = -5
            self.dir = 'left'
        elif keys[K_d]:
            self.speed_x = 5
            self.dir = 'right'
        else:
            if self.speed_x <0:
                self.speed_x = ceil(self.speed_x*0.99)
            elif self.speed_x>0:
                self.speed_x = floor(self.speed_x*0.99)
        if mouse:
            self.dir = 'right' if pygame.mouse.get_pos()[0] - self.rect.x > 0 else 'left'
        if self.jump_num < self.max_jump_num:
            
            if keys[K_SPACE]:
                self.run_time = get_current_time()
            if keys[K_SPACE] and (not self.press_space):
                self.jump_num += 1
                if not 'antigravity' in eff:
                    self.speed_y = self.max_speed_y*0.6
                else:
                    self.speed_y = self.max_speed_y*-0.6
                self.press_space = True
            else:
                if (get_current_time()-self.run_time)%2 == 1:
                    self.press_space = False
        if self.speed_y >-self.max_speed_y:
            self.speed_y -= GRAVITY
        if 'antigravity' in eff:
            if self.speed_y <self.max_speed_y:
                self.speed_y+=GRAVITY*1.5
                self.rect.y-=1
            self.image = pygame.transform.flip(\
                IMAGE[self.image_name], True, True) \
                    if self.dir == 'right' else \
            pygame.transform.flip(IMAGE[self.image_name], False, True)

        if self.rect.top >HEIGHT or self.life <=0 or self.rect.bottom <= -10000:
            return self.die()
        return None

    def do_left_right(self):
        self.rect.x += self.speed_x
    def do_up_down(self):
        self.rect.y -= self.speed_y
    def return_left_right(self):
        self.rect.x -= self.speed_x
        self.speed_x = 0
    def return_up_down(self,block):

        if self.rect.bottom-block.rect.bottom >=0:
            self.rect.top = block.rect.bottom+GRAVITY
            #self.rect.y+=self.speed_y

        else:
            self.rect.bottom = block.rect.top
            self.jump_num = 0
        self.speed_y = 0
        #self.rect.bottom = HEIGHT / 2 + 50
    def die(self) -> str:
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed_x = 0
        self.speed_y = 0
        self.life = 100
        return 'die'