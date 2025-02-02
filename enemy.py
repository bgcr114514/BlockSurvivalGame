import random

import pygame.sprite

from utils import *

IMAGE = get_all_image()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,name,frame = 0):
        super().__init__()
        self.frame = frame
        self.frame_num = 0 if self.frame==0 else 1
        self.last_frame = get_current_time()
        self.self_group = pygame.sprite.Group()
        self.self_group.add(self)
        self.name = name
        self.last_run = get_current_time() - 500
        if random.randint(1,2) == 1:
            self.dir = 'right'
            self.image = pygame.transform.flip(IMAGE[self.name if self.frame==0 else f'{self.name}_1'], True, False)
        else:
            self.dir = 'left'
            self.image = IMAGE[self.name if self.frame==0 else f'{self.name}_1']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = 0
        self.speed_x = 0
        self.life = ENEMY_TYPE[self.name][0]
        self.max_life= ENEMY_TYPE[self.name][0]
        self.hurt = ENEMY_TYPE[self.name][1]
        self.walk_num = random.uniform(1.0,5)*40
        self.walk_num_num = self.rect.x
        self.last_have_hurt = get_current_time()-2000
    def update(self,block:pygame.sprite.Group,player,item_name) -> None|tuple:
        self.speed_x *= 0.99
        self.speed_y -= GRAVITY
        self.dir = 'left' if self.speed_x < 0 else ('right' if self.speed_x > 0 else self.dir)
        if self.frame_num ==0:
            self.image = pygame.transform.flip(IMAGE[self.name], True, False) \
            if self.dir == 'right' else IMAGE[self.name]
        else:
            self.image = pygame.transform.flip(IMAGE[self.name+'_1'], True, False) \
            if self.dir == 'right' else IMAGE[self.name+"_1"]

        #self.do_up_down()

        self.ai(player)

        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        if (mouse[0] and calculate_hypotenuse_length(player.rect.x - self.rect.x,
                                                     self.rect.y - player.rect.y) <= CAN_REACH_LENGTH
                and (self.rect.right >= mouse_pos[0] >= self.rect.left and self.rect.bottom >= mouse_pos[
                    1] >= self.rect.top))\
            and get_current_time() - self.last_have_hurt >= 100:
                self.life -= FIGHT_MUTIPLE.get(item_name, 1)
                self.last_have_hurt = get_current_time()
                self.speed_x += -3 if player.rect.x - self.rect.x > 0 else 3
                self.speed_y = 5

                if self.life <= 0:
                    self.kill()
                    
                    return 'die', self.name

        self.do_up_down()
        
            
        for blk in block.sprites():
            
            if pygame.sprite.spritecollideany(blk,self.self_group):
                self.return_up_down(blk)
        self.do_left_right()
        if pygame.sprite.spritecollideany(self,block):
                self.return_left_right()


        if self.frame_num !=0 and get_current_time()-self.last_frame>=\
        ENEMY_FRAME[self.name][self.frame_num-1]*1000:
            self.last_frame = get_current_time()
            
            self.do_frame()  
        if self.rect.y >= HEIGHT:
            self.kill()
        return

    def ai(self,player):
        if ENEMY_AI_TYPE[self.name]== 'jog':
            self.speed_x = -1 if self.dir == 'left' else 1
        elif ENEMY_AI_TYPE[self.name] == 'run':
            if get_current_time() - self.last_run >= 500:
                if player.rect.x - self.rect.x > 0:
                    self.speed_x += 5
                elif player.rect.x - self.rect.x < 0:
                    self.speed_x -= 5
                self.last_run = get_current_time()
        elif ENEMY_AI_TYPE[self.name] == 'jog_neutral':
            if self.max_life/3 <=self.life:
                self.speed_x = -1 if self.dir == 'left' else 1

            else:
                if get_current_time() - self.last_run >= 500:
                    if player.rect.x - self.rect.x > 0:
                        self.speed_x += 5
                    elif player.rect.x - self.rect.x < 0:
                        self.speed_x -= 5
                    self.last_run = get_current_time()
        elif ENEMY_AI_TYPE[self.name] == 'wrigg':
            self.speed_x = -1 if self.dir == 'left' else 1
        
        if abs(self.rect.x - self.walk_num_num) >= self.walk_num:
            
            self.walk_num = random.uniform(0.0, 12.0) * 40
            self.walk_num_num = self.rect.x
            self.speed_x*=-1
        

    '''def do_left_right(self):
        self.rect.x += self.speed_x
    def do_up_down(self):
        self.rect.y -= self.speed_y
    def return_left_right(self):
        self.rect.x -= self.speed_x*2
        if ENEMY_AI_TYPE[self.name] == 'run':
            self.speed_y= random.randint(5,11)
            self.speed_x*=0.5
        elif ENEMY_AI_TYPE[self.name] == 'jog' or ENEMY_AI_TYPE[self.name] == 'jog_neutral':
            self.speed_x *=-0.9
        

    def return_up_down(self):

        self.rect.y+=self.speed_y*2
        self.speed_y = 0'''
    def do_frame(self):
        
        self.image =  IMAGE[self.name+'_'+str(self.frame_num)] 
        self.frame_num+=1
        if self.frame_num >self.frame:
            self.frame_num = 1

    def do_left_right(self):
        self.rect.x += self.speed_x
    def do_up_down(self):
        self.rect.y -= self.speed_y
    def return_left_right(self):
        self.rect.x-=self.speed_x*2

        if ENEMY_AI_TYPE[self.name] == 'run':
            self.speed_y= random.randint(5,11)
            self.speed_x*=0.5
        elif ENEMY_AI_TYPE[self.name] == 'jog' or ENEMY_AI_TYPE[self.name] == 'jog_neutral':
            self.speed_x *=-0.9
        
    def return_up_down(self,block):

        if self.rect.bottom-block.rect.bottom >=0:
            self.rect.top = block.rect.bottom+1
            self.rect.y+=self.speed_y

        else:
            self.rect.bottom = block.rect.top-2
        self.speed_y = 0