import random

import pygame.sprite

from utils import *

IMAGE = get_all_image()
class Block(pygame.sprite.Sprite):
    def __init__(self,block_id:int,is_retry = True,block_num:int = 0,blocks_name:str = '',dig_time:NUM = 0,x:int = 0,y:int = 0,last_block:str = '',
                 last_x:NUM=0,last_y:NUM=0,is_player_put=0):
        super().__init__()
        if is_retry:
            self.id:int = block_id
            self.block_num:int = random.randint(1,len(BLOCK_NAME))
            self.block_name:str = find_block_tile('block',self.block_num)
            self.image:pygame.surface = IMAGE[self.block_name]
            self.dig_time:NUM = 0
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH / 2 - 120 + block_id * 40, HEIGHT / 2 + 80)
            self.last_block: str = ''
            self.last_x = 0
            self.last_y = 0
        else:
            self.id: int = block_id
            self.block_num: int = block_num
            self.block_name: str = blocks_name
            self.image: pygame.surface = IMAGE[self.block_name]
            self.dig_time: NUM = dig_time
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.last_block: str = last_block
            self.last_x = last_x
            self.last_y = last_y
        self.is_player_put = is_player_put
        self.mouse_pos: None|tuple[int,int] = None
        self.block_dig_time: NUM = int(BLOCK_DIG_TIME[self.block_num - 1]) / CRAFT_SPEED
        self.other_block()



    def update(self,player_rect,player_use,hour,mine) -> str|None|tuple:
        self.update_mouse()
        self.image = pygame_set_alpha('./image/'+self.block_name+'.png',get_alpha(hour,mine))
        if self.mouse_pos is not None:
            if self.rect.left <= self.mouse_pos[0] <= self.rect.right and self.mouse_pos[1] <= self.rect.bottom and self.mouse_pos[
                1] >= self.rect.top:
                if calculate_hypotenuse_length(player_rect[0]-self.rect.centerx,player_rect[1]-self.rect.centery) <= CAN_REACH_LENGTH:
                    self.dig_time += DRAFTS_DIG_MUTIPLE.get(player_use,1)
                    self.other_block()
                    if self.dig_time <= 1 and self.last_block!='' :
                        if self.is_player_put:
                            self.kill()
                        return self.last_block,self.last_x,self.last_y
                    return

    def update_mouse(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.mouse_pos = pygame.mouse.get_pos()
        else:
            self.mouse_pos = None
    def other_block(self):
        set_block_crack_things = set_block_crack(self.block_dig_time, self.dig_time)
        if not set_block_crack_things and type(set_block_crack_things) == bool:

            for mlt in MINERAL_LIST:
                if self.block_name == mlt:
                    break
            else:

                self.last_block = self.block_name
                self.last_x = int(self.rect.centerx)
                self.last_y = int(self.rect.top)
                self.block_num = random.randint(1, len(BLOCK_NAME))
                self.block_name = find_block_tile('block', self.block_num)
                self.image = IMAGE[self.block_name]
                self.block_dig_time = int(BLOCK_DIG_TIME[self.block_num - 1]) / CRAFT_SPEED
                self.dig_time = 0
                return
            self.last_block = self.block_name.split('_block')[0]+'_ore'
            self.last_x = int(self.rect.centerx)
            self.last_y = int(self.rect.top)
            self.block_num = random.randint(1, len(BLOCK_NAME))
            self.block_name = find_block_tile('block', self.block_num)
            self.image = IMAGE[self.block_name]
            self.block_dig_time = int(BLOCK_DIG_TIME[self.block_num - 1]) / CRAFT_SPEED
            self.dig_time = 0
