import sys

import pygame

from utils import *

IMAGE = get_all_image()

class ItemPic(pygame.sprite.Sprite):
    def __init__(self,row:int,is_opening:bool,page:int,surface,should_page:int):
        super().__init__()
        self.synthesis_time = 100
        self.mouse_pos = pygame.mouse.get_pos()
        self.image_name = None
        self.page = page
        self.row = row
        self.should_page = should_page
        self.is_opening = is_opening
        self.image = IMAGE['None']
        self.rect = self.image.get_rect()
        self.rect.x = 23
        self.rect.y = 50*(self.row-1)+212
        self.surface:pygame.Surface = surface
        self.last_synthesis = get_current_time()-self.synthesis_time
        

    def update(self,is_opening:bool,page:int,tile_name:list,row:int,can_synthesis_list:list) -> None|tuple:
        self.is_opening = is_opening
        self.page = page
        self.row = row
        mouse  = pygame.mouse.get_pressed()[0]
        
        self.mouse_pos = pygame.mouse.get_pos()
        if self.is_opening and (len(can_synthesis_list)%10 == 0 or (len(can_synthesis_list)%10 != 0 and
            len(can_synthesis_list)%10 >=self.row)) and \
                (self.should_page==self.page):

            try:
                self.image_name = can_synthesis_list[10*(self.page-1)+self.row-1]
            except IndexError:
                print(self.row,self.page,10*(self.page-1)+self.row-1)
            self.image = pygame.transform.scale(IMAGE[self.image_name],
                                                ITEM_TRANSFORM)
            if self.rect.left <= self.mouse_pos[0] <= self.rect.right and self.mouse_pos[1] <= self.rect.bottom and self.mouse_pos[
                1] >= self.rect.top:
                if mouse and get_current_time()-self.last_synthesis >=self.synthesis_time:
                    if SYNTHESIS_FORMULA[self.image_name][3] in tile_name:
                        self.last_synthesis = get_current_time()

                        return self.image_name,SYNTHESIS_FORMULA[self.image_name][2]

            

        else:

            #self.image = IMAGE['None']
            self.image_name = 'None'
    def draw_self_font(self):
        text_surface = ITEM_NUM_FONT.render(str(SYNTHESIS_FORMULA[self.image_name][2]), True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.rect.x+ITEM_TRANSFORM[0]
        text_rect.top = self.rect.y+ITEM_TRANSFORM[1]
        self.surface.blit(text_surface, text_rect)
    def draw_formula(self):
        draw_num = 1
        for fma in SYNTHESIS_FORMULA[self.image_name][0]:
            self.surface.blit(IMAGE['item_bg'],(15+draw_num*50,self.rect.y-6))
            self.surface.blit(pygame.transform.scale(IMAGE[fma],ITEM_TRANSFORM),(self.rect.x+draw_num*50,self.rect.y))
            


            text_surface = ITEM_NUM_FONT.render(str(SYNTHESIS_FORMULA[self.image_name][1][draw_num-1]), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.x = self.rect.x+draw_num*50+ITEM_TRANSFORM[0]-5
            text_rect.top = self.rect.y+ITEM_TRANSFORM[1]-5
            self.surface.blit(text_surface, text_rect)


            draw_num+=1
        text_surface = ITEM_NUM_FONT.render('在'+CH_EN[SYNTHESIS_FORMULA[self.image_name][3]]+'里合成', True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.x = self.rect.x+draw_num*50+ITEM_TRANSFORM[0]-5
        text_rect.centery = self.rect.centery
        self.surface.blit(text_surface, text_rect)
                
