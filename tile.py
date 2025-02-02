from const import *
from utils import *

IMAGE: dict[str,pygame.Surface] = get_all_image()
class Tile(pygame.sprite.Sprite):
    def __init__(self,tile_num:int,tile_name:str,dig_time:NUM = 0,x:int = 0,y:int = 0):
        super().__init__()
        self.tile_name: str = tile_name
        self.image: pygame.Surface = IMAGE[self.tile_name]
        self.dig_time: NUM = dig_time
        self.tile_num = tile_num
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mouse_pos: None|tuple[int,int] = None
        self.tile_dig_time: NUM = int(TILE_DIG_TIME[self.tile_num-1]) / CRAFT_SPEED
        self.have_player = False



    def update(self,player_rect:tuple[int,int],player_use:str) -> str|None|tuple[str,int,int]:
        self.update_mouse()
        if calculate_hypotenuse_length(player_rect[0]-self.rect.centerx,player_rect[1]-self.rect.centery) <= CAN_REACH_LENGTH:
            self.have_player = True
            if self.mouse_pos is not None:
                if self.rect.left <= self.mouse_pos[0] <= self.rect.right and self.mouse_pos[1] <= self.rect.bottom and self.mouse_pos[
                    1] >= self.rect.top:
                    self.dig_time += DRAFTS_DIG_MUTIPLE.get(player_use,1)
                    if self.dig_time >= self.tile_dig_time:
                        self.kill()
                        return self.tile_name,self.rect.centerx,self.rect.top
                    return
        else:
            self.have_player = False

    def update_mouse(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.mouse_pos = pygame.mouse.get_pos()
        else:
            self.mouse_pos = None
