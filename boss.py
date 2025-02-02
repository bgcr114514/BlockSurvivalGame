import random

import pygame

from const import *
from utils import *

IMAGE = get_all_image()

class Boss(pygame.sprite.Sprite):
    def __init__(self,boss_name:str,bottom:NUM,centerx:NUM,frame:int =0) -> None:
        super().__init__()
        self.boss_name = boss_name
        self.ai_type=self.boss_name
        self.image:pygame.Surface = pygame.transform.scale(IMAGE[\
            BOSS_IMAGE_TRANSFORM[self.boss_name][0]+('_1' if frame !=0 else '')],
            BOSS_IMAGE_TRANSFORM[self.boss_name][1])
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx
        self.speed_x = 0
        self.speed_y = 0
        self.dir = 'left'
        self.last_run = get_current_time()-500
        self.last_have_hurt = get_current_time()-1000
        self.walk_num = random.uniform(1.0,5)*40
        self.walk_num_num = self.rect.x
        self.life = BOSS_TYPE[self.boss_name][0]
        self.max_life = BOSS_TYPE[self.boss_name][0]
        self.hurt = BOSS_TYPE[self.boss_name][1]
        self.is_ending = False
        self.frame = frame
        self.frame_num = 1 if self.frame !=0 else 0

        self.last_frame = get_current_time()

    def update(self,block,player,item_name) -> None|tuple:
    

        if self.is_ending:
            if self.rect.bottom <=0:
                self.kill()
            else:
                
                self.rect.y-=20
        else:
            self.speed_x *=0.99
            self.speed_y -= 1
            self.dir = 'left' if self.speed_x<0 else ('right' if self.speed_x>0 else self.dir)
            self.image = pygame.transform.flip(pygame.transform.scale(IMAGE\
                [BOSS_IMAGE_TRANSFORM[self.boss_name][0]+(f'_{self.frame_num}' if self.frame !=0 else '')],
            BOSS_IMAGE_TRANSFORM[self.boss_name][1]), True, False) if self.dir == 'right' else \
            pygame.transform.scale(IMAGE[BOSS_IMAGE_TRANSFORM[self.boss_name][0]+(f'_{self.frame_num}' if self.frame !=0 else '')],
            BOSS_IMAGE_TRANSFORM[self.boss_name][1])

            self.ai(player,block)
            

            
            mouse_pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if (mouse[0] and calculate_hypotenuse_length(player.rect.x-self.rect.x,self.rect.y-player.rect.y) <=CAN_REACH_LENGTH
                    and (self.rect.right>=mouse_pos[0] >= self.rect.left and self.rect.bottom >= mouse_pos[1]>=self.rect.top)):
                if get_current_time()-self.last_have_hurt >= 10:
                    self.life -= FIGHT_MUTIPLE.get(item_name,1)
                    self.last_have_hurt = get_current_time()
            if self.life <=0:
                self.kill()
                        
                return 'die',self.boss_name
        
        if self.frame_num !=0 and get_current_time()-self.last_frame>=\
        BOSS_FRAME[self.boss_name][self.frame_num-1]*1000:
            self.last_frame = get_current_time()
            
            self.do_frame()          

    def do_frame(self) -> None:
        
        self.image =  IMAGE[self.boss_name+'_'+str(self.frame_num)] 
        self.frame_num+=1
        if self.frame_num >self.frame:
            self.frame_num = 1
        
    def ai(self,player,block) -> None:
        if abs(self.rect.x - self.walk_num_num) >= self.walk_num:
                self.walk_num = random.uniform(0.0, 15.0) * 40
                self.walk_num_num = self.rect.x
        if self.ai_type == 'big_hen' or self.ai_type == 'biggest_hen':
            if get_current_time()-self.last_run>=500:
                    if player.rect.x-self.rect.x>0:
                        self.speed_x += 1
                    elif player.rect.x-self.rect.x<0:
                        self.speed_x -= 1
                    self.last_run = get_current_time()
            if player.rect.y-self.rect.y>0:
                self.speed_y = -1
            elif player.rect.y-self.rect.y<0:
                self.speed_y = 1
            else:
                self.speed_y = 0
            if self.rect.y >= HEIGHT*0.75:
                self.rect.bottom = player.rect.top - 50
                self.rect.centerx = player.rect.centerx 
            self.do_up_down()
            self.do_left_right()
        elif self.ai_type == 'worm_king':
            if get_current_time()-self.last_run>=500:
                    if player.rect.x-self.rect.x>0:
                        self.speed_x += 5
                    elif player.rect.x-self.rect.x<0:
                        self.speed_x -= 5
                    self.last_run = get_current_time()
            self.speed_y-=GRAVITY            
            if self.rect.y >= HEIGHT:
                    
                    self.kill()
            self.do_up_down()
            if pygame.sprite.spritecollideany(self, block):
                self.return_up_down()
            self.do_left_right()
            '''if pygame.sprite.spritecollideany(self, block):
                self.return_left_right()'''
            if self.rect.left <50 or self.rect.right>WIDTH-50:
                self.speed_x*=-1
            if calculate_hypotenuse_length(self.rect.x-player.rect.x,
                            self.rect.y-player.rect.y)>300:
                self.rect.bottom = player.rect.top - 50
                self.rect.centerx = player.rect.centerx 
    def do_left_right(self) -> None:
        self.rect.x += self.speed_x
    def do_up_down(self) -> None:
        self.rect.y -= self.speed_y
    def return_left_right(self) -> None:
        self.rect.x -= self.speed_x
    def return_up_down(self) -> None:

        self.rect.y+=self.speed_y
        self.speed_y = 0