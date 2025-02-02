from functools import partial

from missile import *
from barrage import *
from block import *
from boss import *
from could import *
from droplet import *
from dust import *
from enemy import *
from hail import *
from item import *
from itempic import *
from player import *
from smoke import *
from tile import *

class Game:
    def __init__(self, surface, item_dict:dict,read_files=None,tile_files:str|list[str] = '') -> None:
        self.effect_dict = {}
        self.surface:pygame.Surface = surface
        self.block_sprites = pygame.sprite.Group()
        self.tile_class = pygame.sprite.Sprite
        self.tile_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.smoke_list:list[SmokeEmitter] = []
        self.last_missile = get_current_time()
        self.block_update = ''
        self.have_tile:set|list = []
        self.cn_have_tile:list = []
        self.item_dict = item_dict
        self.is_rain = random.sample([True,False],1)[0]
        self.is_have_droplet = False
        self.have_droplet_num = 0


        if self.is_rain:
            self.rain_end_time = get_current_time()+random.randint(10,120)*1000
            self.next_rain = get_current_time()
        else:
            self.rain_end_time = 0
            self.next_rain = get_current_time()+random.randint(10,120)*1000
        if read_files is None:
            for i in range(6):
                self.block_class = Block(i)
                self.block_sprites.add(self.block_class)
        else:
            for i in range(int(len(read_files)/BLOCK_SAVE_NUM)):
                self.block_class = Block(i,False,int(read_files[i*BLOCK_SAVE_NUM].split('\n')[0]),
                                         read_files[i*BLOCK_SAVE_NUM+1].split('\n')[0],
                                         float(read_files[i*BLOCK_SAVE_NUM+2].split('\n')[0]),
                                         int(read_files[i*BLOCK_SAVE_NUM+3].split('\n')[0]),
                                         int(read_files[i*BLOCK_SAVE_NUM+4].split('\n')[0]),
                                         read_files[i*BLOCK_SAVE_NUM+5].split('\n')[0],
                                         read_files[i*BLOCK_SAVE_NUM+6].split('\n')[0],
                                         read_files[i*BLOCK_SAVE_NUM+7].split('\n')[0],
                                         bool(int(read_files[i*BLOCK_SAVE_NUM+8].split('\n')[0])))
        
                self.block_sprites.add(self.block_class)
        if tile_files != '':
            for i in range(int(len(tile_files)/TILE_SAVE_NUM)):
                self.tile_class = Tile(int(tile_files[i*TILE_SAVE_NUM].split('\n')[0]),
                                        str(tile_files[i*TILE_SAVE_NUM+1].split('\n')[0]),
                                         float(tile_files[i*TILE_SAVE_NUM+2].split('\n')[0]),
                                         int(tile_files[i*TILE_SAVE_NUM+3].split('\n')[0]),
                                         int(tile_files[i*TILE_SAVE_NUM+4].split('\n')[0]),
                                         )
        
                self.tile_group.add(self.tile_class)

        self.player_class = Player()
        self.player_sprites = pygame.sprite.Group()
        self.item_class = None
        self.player_sprites.add(self.player_class)
        self.item_group = pygame.sprite.Group()
        self.update_player = None
        self.enemy_group = pygame.sprite.Group()
        self.droplet_group = []

        self.boss_group = pygame.sprite.Group()
        self.item_pic_group = pygame.sprite.Group()
        for i in range(len(SYNTHESIS_FORMULA)):
            self.item_pic_group.add(ItemPic(i%10+1,True,i//10,self.surface,int(floor((i+1)/10)+1 if (i+1)%10!=0 else (i+1)/10)))
        self.can_synthesis_list:list= []
        self.boss_group.add(Boss('worm_king',HEIGHT/2,WIDTH/2,2))
        self.boss_group.add(Boss('big_hen',HEIGHT/2,WIDTH/2))
        
        self.is_have_droplet_num = 0

        self.last_put_block = get_current_time()-PUT_BLOCK_SLEEP_TIME
        self.mouse:Mouse = Mouse()
        self.last_eat_food = get_current_time()-FODD_SLEEP_TIME *1000
        self.could_group = []       
        self.last_could = get_current_time()

        
        self.next_wind = get_current_time()+random.randint(10,5000)*1000
        self.last_wind_time = get_current_time()
        self.wind_end_time = get_current_time()
        self.is_have_wind = False
        self.is_have_dust = False

        self.is_have_dust_num = 0

        self.dust_group = []

        self.wind_speed = random.randint(-10,10)

        self.is_hail =  False
        self.is_have_hail = False
        self.is_have_hail_num = 0

        self.hail_end_time = 0
        self.next_hail = get_current_time()+random.randint(100,600)*1000
        
        self.hail_group = pygame.sprite.Group()

        self.last_play_wind = get_current_time()

        self.barrage_group = pygame.sprite.Group()
        self.boss_last_barrage = get_current_time()
        self.can_throw = False
        self.run_time = get_current_time()

        self.is_open_shop = False
        self.last_smoke_time = get_current_time()-500

        self.shop_dict={}    #self.shop_dict[卖的物品] = [买的物品,要卖的数量,要买的数量]
        self.button_list = []
        while len(self.shop_dict)<6:
            i = len(self.shop_dict)
            add_ = random.sample(list(CH_EN.keys()),1)[0]
            while add_ == 'knapsack':
                add_ = random.sample(list(CH_EN.keys()),1)[0]
            add_i = random.sample(list(CH_EN.keys()),1)[0]
            while add_i == 'knapsack' or add_i == add_:
                add_i = random.sample(list(CH_EN.keys()),1)[0]
            self.shop_dict[add_] = [add_i,random.randint(1,50),random.randint(1,20)]
            self.button_list.append(\
        Button(i%3*100+450,i//3*150+250,60,30,'red','购买',INTRODUCE_FONT,
        'white',partial(self.buy,i),5))
            
    def update(self,is_opening,item_choice_num,page,hour,mine) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_t] and keys[K_LCTRL] :
            self.run_time = get_current_time()
        if len(self.item_dict)-1>=item_choice_num and keys[K_t] and keys[K_LCTRL] and self.can_throw:
            self.can_throw = False
            self.item_group.add(Item(list(self.item_dict.keys())[item_choice_num],
                                                self.player_class.rect.left-20 if self.player_class.dir == 'left' else self.player_class.rect.right+20,
                                                self.player_class.rect.bottom,
                                                list(self.item_dict.values())[item_choice_num]))
            del self.item_dict[list(self.item_dict.keys())[item_choice_num]]
        else:
            if (get_current_time()-self.run_time)%2 == 1:
                    self.can_throw = True
            else:
                self.can_throw = False
        self.wind_speed += random.uniform(0.2,-0.2)
        self.wind_speed = round(self.wind_speed,2) if round(self.wind_speed)<=30 else 30
        will_del = []
        for k in self.effect_dict.keys():
            self.effect_dict[k]-=1
            if self.effect_dict[k]<=0:
                will_del.append(k)
        for i in will_del:
            del self.effect_dict[i]
        if "life_add" in self.effect_dict:
            self.player_class.life=min(self.player_class.life+0.1,self.player_class.max_life)
        
        self.update_could()
        self.update_wind_and_dust()
        try:
            item_name = list(self.item_dict.keys())[item_choice_num]
        except IndexError:
            item_name = 'hand'
        if item_name == "firecraker" and pygame.mouse.get_pressed()[2] and get_current_time()-self.last_smoke_time>500:
            self.item_dict[item_name] -= 1
            if self.item_dict[item_name] == 0:
                del self.item_dict[item_name]
            self.missile_group.add(Missile('firecraker',self.player_class.rect.centerx,
            self.player_class.rect.centery-30,
            pygame.mouse.get_pos()[0]-self.player_class.rect.x,self.player_class.rect.y-pygame.mouse.get_pos()[1],"firecraker",False))
            
            self.last_smoke_time = get_current_time()
        self.boss_come(hour)
        self.player_update()
        self.update_enemy(item_name)
        self.update_boss(item_name)

        self.update_block(item_name,hour,mine)
        self.update_tile(item_name)
        self.update_item()
        self.update_droplet()
        self.update_hail()
        self.update_item_pic(is_opening,page)
        self.update_smoke()

        self.put_things(item_name)
        
        self.update_eat_food(item_name)
        self.mouse.update()
        self.update_missile(item_choice_num)
        i_g = pygame.sprite.Group()
        i_g.add(self.enemy_group)
        i_g.add(self.boss_group)
        #print(i_g is self.enemy_group)

        self.barrage_group.update(self.player_sprites,i_g)
        if self.is_open_shop:
            for bun in self.button_list:
                bun.update()
        
    def buy(self,num:int) -> None:
        #self.shop_dict[买的物品] = [卖的物品,要卖的数量,要买的数量]
        if list(self.shop_dict.keys())[num] in list(self.item_dict.keys()):
            if list(self.shop_dict.values())[num][1] <= \
                self.item_dict.get(list(self.shop_dict.keys())[num],0):
                if len(self.item_dict)<10:
                    self.item_dict[list(self.shop_dict.keys())[num]] -= \
                    list(self.shop_dict.values())[num][1]
                    if self.item_dict[list(self.shop_dict.keys())[num]] == 0:
                        del self.item_dict[list(self.shop_dict.keys())[num]]
                    self.item_dict[list(self.shop_dict.values())[num][0]] = \
                        self.item_dict.get(list(self.shop_dict.values())[num][0],0)+list(self.shop_dict.values())[num][2]

    def update_smoke(self):
        for smo in self.smoke_list:
            smo.update(self.wind_speed)
    def update_missile(self,num) -> None:
        if len(self.missile_group) == 0:
            self.last_missile = get_current_time()-200
        if len(self.item_dict)-1>=num and ('bow' in list(self.item_dict.keys())[num] == self.item_dict.get('arrow',0)>=1):
            
            mouse = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse[2]:
                
                if self.item_dict['arrow'] == 0:
                    del self.item_dict['arrow']
                if get_current_time()-self.last_missile>=200:
                    self.item_dict['arrow'] -= 1
                    if self.item_dict['arrow'] == 0:
                        del self.item_dict['arrow']
                    self.missile_group.add(Missile('arrow',self.player_class.rect.centerx,
                    self.player_class.rect.centery-30,
                    (mouse_pos[0]-self.player_class.rect.centerx),
                    (self.player_class.rect.centery-mouse_pos[1])))
                    self.last_missile = get_current_time()
        self.missile_group.update(self.player_class)
        for mis in self.missile_group.sprites():
                    if pygame.sprite.spritecollideany(mis,self.block_sprites):
                        self.missile_eff(mis)
                        mis.kill()
                    if pygame.sprite.spritecollideany(mis,self.enemy_group):
                        for eny in self.enemy_group.sprites():
                            if pygame.sprite.spritecollideany(eny,self.missile_group):
                                eny.last_have_hurt = get_current_time()
                                eny.life-=MISSILE_MUTIPLE.get(mis.image_name,0)
                            self.missile_eff(mis)
                            mis.kill()
                        
                    if pygame.sprite.spritecollideany(mis,self.boss_group):
                        for bos in self.boss_group.sprites():
                            bos.last_have_hurt = get_current_time()
                            bos.life-=MISSILE_MUTIPLE.get(mis.image_name,0)
                        self.missile_eff(mis)
                        mis.kill()
                    if (not mis._friendly) and pygame.sprite.spritecollideany(mis,self.player_sprites):
                        self.player_class.life-=MISSILE_MUTIPLE.get(mis.image_name,0)
                        self.missile_eff(mis)
                        mis.kill()
                            
        
    def missile_eff(self,mis:Missile):
        if mis.effect == 'firecraker':
            self.smoke_list.append(SmokeEmitter(mis.rect.centerx,mis.rect.centery,self.surface))
    def update_hail(self) -> None:
        
        if not self.is_hail:
            self.hail_end_time = get_current_time()
        elif self.is_hail:
            self.next_hail = get_current_time()
        if self.hail_end_time - get_current_time() <0:
            self.next_hail = get_current_time()+random.randint(10,2304)*1000
            self.is_hail = False
            self.is_have_hail_num=0
        if self.next_hail - get_current_time() <0:
            self.hail_end_time = get_current_time()+random.randint(10,780)*1000
            self.is_hail = True
        
        for hal in self.hail_group:
            hal.update(not self.is_hail,self.wind_speed,self.player_sprites,
            self.block_sprites,self.tile_group)
            for hal in self.hail_group.sprites():
                if pygame.sprite.spritecollideany(hal,self.player_sprites):
                    self.player_class.life-=10
                    get_all_audio()['player_hurt'].play()
        if self.is_hail:
            self.have_hail_num = random.randint(10,500)
            if not self.is_have_hail:
                if self.have_hail_num > self.is_have_hail_num:
                    self.hail_group.add(Hail(self.surface))
                    self.is_have_hail_num+=1
                else:
                    self.is_have_hail = True
    
    def update_wind_and_dust(self) -> None:
        if not self.is_have_wind:
            self.wind_end_time = get_current_time()
        elif self.is_have_wind:
            self.next_wind = get_current_time()
            '''if get_current_time()-self.last_wind_time>=get_all_audio()['wind'].get_length():
                get_all_audio()['wind'].play()
                self.last_play_wind = get_current_time()'''
        if self.wind_end_time - get_current_time() <0 or (abs(self.wind_speed)<=5 and \
            self.is_have_wind):
            self.next_wind = get_current_time()+random.randint(10,2304)*1000
            self.is_have_wind = False
            self.is_have_dust_num=0
        if self.next_wind - get_current_time() <0 or (abs(self.wind_speed)>=20 and \
            not self.is_have_wind):
            self.last_play_wind = get_current_time()-get_all_audio()['wind'].get_length()
            self.wind_end_time = get_current_time()+random.randint(10,780)*1000
            self.is_have_wind = True

        if len(self.dust_group)!=0:
            for dut in self.dust_group:
                dut.move(self.wind_speed)
                if not self.is_have_wind:
                    self.dust_group.remove(dut)
                    del dut

        if self.is_have_wind:
            self.have_dust_num = random.randint(100 ,200)
            if not self.is_have_dust:
                if self.have_dust_num > self.is_have_dust_num:
                    self.dust_group.append(Dust(int(self.wind_speed)))
                    self.is_have_dust_num+=1
                else:
                    self.is_have_wind = True
    
    def update_could(self) -> None:
        for col in self.could_group:
            col.move(self.wind_speed)
            if col.x<=0:
                self.could_group.remove(col)
                del col

        if get_current_time()-self.last_could>=1000:
            self.could_group.append(Could(int(self.wind_speed)+1))
            self.last_could = get_current_time()
    
    def put_things(self,item_name) -> None:
        if calculate_hypotenuse_length(self.mouse.rect.x-self.player_class.rect.x,\
            self.mouse.rect.y-self.player_class.rect.y)<=CAN_PUT_LENGTH \
                and(item_name in BLOCK_NAME or  item_name in TILE_NAME):
            self.mouse.rect.x = int(((self.mouse.rect.x+20)//40-0.5)*40)
            self.mouse.rect.y= int(((self.mouse.rect.y-20)//40+0.5)*40)
            image = IMAGE[item_name+'alpha']
            self.surface.blit(image,(((self.mouse.rect.x+20)//40-0.5)*40,
                                                    ((self.mouse.rect.y-20)//40+0.5)*40))
            if get_current_time()-self.last_put_block>=PUT_BLOCK_SLEEP_TIME and \
                not pygame.sprite.spritecollideany(self.mouse,self.tile_group) and \
                not pygame.sprite.spritecollideany(self.mouse,self.player_sprites) and \
                not pygame.sprite.spritecollideany(self.mouse,self.block_sprites) and \
                not pygame.sprite.spritecollideany(self.mouse,self.enemy_group) and \
                not pygame.sprite.spritecollideany(self.mouse,self.boss_group):

                self.update_put_block(item_name)
                self.update_put_tile(item_name)
                
                self.surface.blit(image,(((self.mouse.rect.x+20)//40-0.5)*40,
                                                    ((self.mouse.rect.y-20)//40+0.5)*40))
            else:
                
                self.surface.blit(IMAGE['error_put'],(((self.mouse.rect.x+20)//40-0.5)*40,
                                                    ((self.mouse.rect.y-20)//40+0.5)*40))
    
    def update_eat_food(self,item_name) -> None:

        if item_name in list(FOOD_GIVE_HP.keys()) and pygame.mouse.get_pressed()[2] and \
            get_current_time() - self.last_eat_food >= FODD_SLEEP_TIME*1000:
            
            self.last_eat_food = get_current_time()
            if self.player_class.max_life-self.player_class.life <=FOOD_GIVE_HP[item_name]:
                self.player_class.life = self.player_class.max_life
            else:
                self.player_class.life+=FOOD_GIVE_HP[item_name]
            self.effect_dict['eat_food'] = frame_time_to_time(FODD_SLEEP_TIME)
            self.item_dict[item_name] -= 1
            if self.item_dict[item_name] == 0:
                del self.item_dict[item_name]

    def update_tile(self,choice_name) -> None:

        for itl in self.tile_group:
            if pygame.mouse.get_pressed()[0] and itl.tile_name == "tile_firecraker" and pygame.sprite.collide_rect(itl,self.mouse): 
                #代码莫明奇妙的跑起来了，甚至还完成了我搞不出的功能？？？？？,,全屏幕一起炸
                self.smoke_list.append(SmokeEmitter(itl.rect.centerx,itl.rect.centery,self.surface))
                itl.kill()
            self.tile_update = itl.update(self.player_class.rect.center,choice_name)
            if self.tile_update is not None:
                

                self.item_class = Item(self.tile_update[0],int(self.tile_update[1]),int(self.tile_update[2])-5)
                self.item_group.add(self.item_class)
                self.tile_update = itl.update(self.player_class.rect.center,choice_name)
    
    def update_put_block(self,item_name:str) -> None:
        
        mouse = pygame.mouse.get_pressed()

        if mouse[2] and item_name in BLOCK_NAME: 
                
            self.block_sprites.add(Block(block_id=-1,is_retry=False,block_num=get_velue_position(BLOCK_NAME,item_name,0),blocks_name=item_name,dig_time=0,
                                                x=((self.mouse.rect.x+20)//40-0.5)*40,
                                                y=((self.mouse.rect.y-20)//40+0.5)*40,
                                                is_player_put=True))
                    
            self.item_dict[item_name] -= 1
            if self.item_dict[item_name] == 0:
                del self.item_dict[item_name]
            self.last_put_block = get_current_time()

    def update_put_tile(self,item_name:str) -> None:
        mouse = pygame.mouse.get_pressed()
        
        if item_name in TILE_NAME: 
            self.mouse.rect.x += TILE_PUT[TILE_NAME.index(item_name)][0]
            self.mouse.rect.y += TILE_PUT[TILE_NAME.index(item_name)][1]
            if pygame.sprite.spritecollideany(self.mouse,self.tile_group) or\
                pygame.sprite.spritecollideany(self.mouse,self.block_sprites):
                if mouse[2]:
                    self.mouse.rect.x -= TILE_PUT[TILE_NAME.index(item_name)][0]
                    self.mouse.rect.y -= TILE_PUT[TILE_NAME.index(item_name)][1]
                    self.tile_group.add(Tile(tile_name=item_name,tile_num=get_velue_position(TILE_NAME,item_name,0),
                                                x=((self.mouse.rect.x+20)//40-0.5)*40,
                                                y=((self.mouse.rect.y-20)//40+0.5)*40,))
                    
                    self.item_dict[item_name] -= 1
                    if self.item_dict[item_name] == 0:
                        del self.item_dict[item_name]
                    self.last_put_block = get_current_time()
            else:
                self.mouse.rect.x -= TILE_PUT[TILE_NAME.index(item_name)][0]
                self.mouse.rect.y -= TILE_PUT[TILE_NAME.index(item_name)][1]
                image = IMAGE[item_name+'alpha']
                self.surface.blit(image,(((self.mouse.rect.x+20)//40-0.5)*40,
                                                        ((self.mouse.rect.y-20)//40+0.5)*40))
                self.surface.blit(IMAGE['error_put'],(((self.mouse.rect.x+20)//40-0.5)*40,
                                                        ((self.mouse.rect.y-20)//40+0.5)*40))
    
    
    def boss_come(self,hour) -> None:
        if not self.is_have_droplet and self.is_rain:
            if self.item_dict.get('chicken',0)>=100 and self.item_dict.get('feathers',0)>=50 \
                    and random.randint(1,10) == 3 and hour>18 and is_boss_in_group(self.boss_group,'big_hen'):
                self.boss_group.add(Boss('big_hen', 0, WIDTH / 2))
    
    def update_item_pic(self,is_opening,page) -> None:


        self.have_tile = {'knapsack'}
        self.cn_have_tile = []
        for til in self.tile_group.sprites():
            if til.have_player:
                self.have_tile.add(til.tile_name)
        self.have_tile = list(self.have_tile)
        for hal in self.have_tile:
            self.cn_have_tile.append(CH_EN[hal])
        self.can_synthesis_list = []
        for k,v in SYNTHESIS_FORMULA.items():
            for v0 in v[0]:
                if (not (v0 in self.item_dict)) or \
                    self.item_dict[v0]<v[1][get_velue_position(v[0],v0)-1] or\
                         not v[3]in self.have_tile:
                        break
            else:
                self.can_synthesis_list.append(k)
                        
        if len(self.can_synthesis_list)!=0:    
            itm_num = 0
            for itp in self.item_pic_group.sprites():
                
                itm_num += 1
                itp_update = itp.update(is_opening,page,self.have_tile,(itm_num-1)%10+1,
                self.can_synthesis_list)

                """and self.item_dict.get(itp_)<=
                                SYNTHESIS_FORMULA[itp_update[0]][1][get_velue_position(SYNTHESIS_FORMULA[itp_update[0]],itp_)]"""

                if itp_update is not None:
                    if not(itp_update[0] in self.item_dict):
                        can_syn_2_aug = False

                        for itp_ in SYNTHESIS_FORMULA[itp_update[0]][0]:
                            if itp_ in self.item_dict and self.item_dict.get(itp_)<=\
                                SYNTHESIS_FORMULA[itp_update[0]][1][get_velue_position(SYNTHESIS_FORMULA[itp_update[0]][0],itp_)-1]:
                                can_syn_2_aug = True
                                break
                    else:
                        can_syn_2_aug = True
                    
                    if can_syn_2_aug or len(self.item_dict)<10:
                        
                        for itp_ in SYNTHESIS_FORMULA[itp_update[0]][0]:
                            if not(itp_ in self.item_dict) or\
                                (itp_ in self.item_dict and SYNTHESIS_FORMULA[itp_update[0]][1][0]>self.item_dict[itp_]):
                                break
                        else:
                            for itl in self.item_dict.keys():
                                if itp_update[0] == itl:
                                    self.item_dict[itp_update[0]] += itp_update[1]
                                    break
                            else:
                                self.item_dict[itp_update[0]] = itp_update[1]
                            
                            for itm in SYNTHESIS_FORMULA[itp_update[0]][0]:
                                self.item_dict[itm] -= SYNTHESIS_FORMULA[itp_update[0]][1][0]
                                if self.item_dict[itm] == 0:
                                    del self.item_dict[itm]
    
    '''def update_item_pic(self, is_opening, page) -> None:
        # 初始化已有的瓦片集合
        self.have_tile = {'knapsack'}
        self.cn_have_tile = []
        
        # 收集玩家所在位置的瓦片
        for til in self.tile_group.sprites():
            if til.have_player:
                self.have_tile.add(til.tile_name)
        
        
        # 初始化可合成物品列表
        self.can_synthesis_list = []
        
        # 检查每个合成公式是否满足条件
        for k, v in SYNTHESIS_FORMULA.items():
            can_synthesize = True
            for v0 in v[0]:
                if v0 not in self.item_dict or self.item_dict[v0] < v[1][get_velue_position(v[0], v0) - 1] or v[3] not in self.have_tile:
                    can_synthesize = False
                    break
            if can_synthesize:
                self.can_synthesis_list.append(k)

        # 如果有可合成的物品，则更新每个物品图片
        if len(self.can_synthesis_list) != 0:
            itm_num = 0
            for itp in self.item_pic_group.sprites():
                itm_num += 1
                itp_update = itp.update(is_opening, page, self.have_tile, (itm_num - 1) % 10 + 1, self.can_synthesis_list)

                if itp_update is not None:
                    # 检查是否可以合成该物品
                    can_synthesize = True
                    for itp_ in SYNTHESIS_FORMULA[itp_update[0]][0]:
                        if itp_ not in self.item_dict or self.item_dict[itp_] < SYNTHESIS_FORMULA[itp_update[0]][1][get_velue_position(SYNTHESIS_FORMULA[itp_update[0]][0], itp_) - 1]:
                            can_synthesize = False
                            break
                    
                    # 如果可以合成或背包未满，则进行合成
                    if can_synthesize or len(self.item_dict) < 10:
                        # 增加合成物品的数量
                        if itp_update[0] in self.item_dict:
                            self.item_dict[itp_update[0]] += itp_update[1]
                        else:
                            self.item_dict[itp_update[0]] = itp_update[1]
                        
                        # 减少合成所需的物品数量
                        for itm in SYNTHESIS_FORMULA[itp_update[0]][0]:
                            self.item_dict[itm] -= SYNTHESIS_FORMULA[itp_update[0]][1][0]
                            if self.item_dict[itm] == 0:
                                del self.item_dict[itm]'''

    def update_droplet(self) -> None:
        
        if not self.is_rain:
            self.rain_end_time = get_current_time()
        elif self.is_rain:
            self.next_rain = get_current_time()
        if self.rain_end_time - get_current_time() <0:
            self.next_rain = get_current_time()+random.randint(10,2304)*1000
            self.is_rain = False
            self.is_have_droplet_num=0
        if self.next_rain - get_current_time() <0:
            self.rain_end_time = get_current_time()+random.randint(10,780)*1000
            self.is_rain = True

        
        for dol in self.droplet_group:
            dol.move(not self.is_rain,self.wind_speed)
        if self.is_rain:
            self.have_droplet_num = random.randint(10,500)
            if not self.is_have_droplet:
                if self.have_droplet_num > self.is_have_droplet_num:
                    self.droplet_group.append(Droplet(self.surface))
                    self.is_have_droplet_num+=1
                else:
                    self.is_have_droplet = True
        
    def update_item(self) -> None:
        
        for itm in self.item_group.sprites():
            if len(self.item_dict) <10 or itm.item_name in self.item_dict:
                if pygame.sprite.spritecollideany(itm,self.player_sprites):
                    
                    for itl in self.item_dict.keys():
                        if itm.item_name == itl:
                            self.item_dict[str(itm.item_name)] += itm.num
                            break
                    else:
                        self.item_dict[str(itm.item_name)] = itm.num
                    itm.kill()
        for itm in self.item_group.sprites():
            if not pygame.sprite.spritecollideany(itm,self.block_sprites):
                itm.update()
            else:
                itm.rect.y-=1
                
                itm.speed_y = 0
            if itm.num > 1:
                draw_font(self.surface,ITEM_NUM_FONT,str(itm.num),
                itm.rect.right,itm.rect.bottom)

    def update_block(self,choice_name,hour,mine) -> None:
        for blk in self.block_sprites.sprites():
                self.block_update = blk.update(self.player_class.rect.center,
                choice_name,hour,mine)
                if self.block_update is not None:
                    if self.block_update[0] == "lucky_block":
                        if random.randint(1,2) == 1:
                            things = list(CH_EN.keys())[random.randint(0,len(list(CH_EN.keys()))-1)]
                            if things != 'hand' and things != 'knapsack':
                                self.item_class = \
                                    Item(things,int(self.block_update[1]),int(self.block_update[2])-5)
                                self.item_group.add(self.item_class)
                        else:
                            self.effect_dict[random.sample(list(EFF_INTRODUCE.keys()),1)[0]] = 3000
                    else:
                        self.item_class = Item(self.block_update[0],int(self.block_update[1]),int(self.block_update[2])-5)
                        self.item_group.add(self.item_class)
                    if random.randint(1,23)==1 and blk.is_player_put == False:
                        enemy_name = random.sample(ENEMY_NAME,1)[0]
                        self.enemy_group.add(Enemy(int(self.block_update[1]),int(self.block_update[2])-5,
                        enemy_name,ENEMY_TYPE[enemy_name][2]))
                    have_plant_num = random.randint(1,500)
                    if blk.is_player_put == False and (blk.last_block=='grass_block' or blk.last_block =='soil_block'):
                        food_name = ''
                        if 40<have_plant_num<50:
                            food_name = 'dugar_cane'
                        elif 30<have_plant_num<40:
                            food_name='apple'
                        elif 20<have_plant_num<30:
                            food_name='orange'
                        elif 50<have_plant_num<55:
                            food_name='tea-leaf'
                        if food_name != '':
                            self.item_class = Item(food_name,int(self.block_update[1]),int(self.block_update[2])-5)
                            self.item_group.add(self.item_class)
                    self.block_update = blk.update(self.player_class.rect.center,
                    choice_name,hour,mine)

    def player_update(self) -> None:
        
        self.player_collision_detection()
        player_rect = self.player_class.rect.centerx,self.player_class.rect.top
        self.update_player=self.player_class.update(list(self.effect_dict.keys()))
        if self.update_player == 'die':
            for itm_key in self.item_dict.keys():
                self.item_group.add(Item(itm_key,player_rect[0]+random.randint(-80,80),
                player_rect[1],self.item_dict[itm_key]))
            self.item_dict.clear()
            for bog in self.boss_group:
                bog.is_ending = True
        if self.is_have_wind and self.player_class.speed_x==0:
            self.player_class.speed_x= -floor(self.wind_speed)
             
    def update_enemy(self,item_name) -> None:
        for eny in self.enemy_group.sprites():
                eny_up = eny.update(self.block_sprites,self.player_class,item_name)
                if eny_up is not None:
                    for i in range(len(ENEMY_SPOILS[eny_up[1]][0])):
                        for itl in range(random.randint(ENEMY_SPOILS[eny_up[1]][1][i][0],ENEMY_SPOILS[eny_up[1]][1][i][1])):
                            x_add = random.uniform(-10,10)
                            self.item_group.add(Item(ENEMY_SPOILS[eny_up[1]][0][i],
                            eny.rect.centerx+x_add,eny.rect.bottom))
                    eny.kill()
                    
        
        for i,eny in enumerate(self.enemy_group):
            if pygame.sprite.spritecollideany(eny,self.player_sprites) and get_current_time()-self.player_class.last_hurt>=500 and eny.hurt >0:
                self.player_class.speed_x = -10 if eny.dir == 'left' else 10
                self.player_class.life -= self.enemy_group.sprites()[i].hurt
                get_all_audio()['player_hurt'].play()
                self.player_class.last_hurt  = get_current_time()
                break
        return

    def update_boss(self,item_name) -> None:
        if len(self.boss_group.sprites())==10:
            pass
        for bog in self.boss_group.sprites():
                    bog_up = bog.update(self.block_sprites,self.player_class,\
                        item_name)
                    if bog_up is not None:
                        for i in range(len(BOSS_SPOILS[bog_up[1]][0])):
                            for itl in range(random.randint(BOSS_SPOILS[bog_up[1]][1][i][0],BOSS_SPOILS[bog_up[1]][1][i][1])):
                                x_add = random.uniform(-10,10)
                                self.item_group.add(Item(BOSS_SPOILS[bog_up[1]][0][i],
                                bog.rect.centerx+x_add,bog.rect.centery))
        for i,bog in enumerate(self.boss_group):
                if pygame.sprite.groupcollide(self.player_sprites,[bog],False,False,pygame.sprite.collide_mask) and get_current_time()-self.player_class.last_hurt>=500 and bog.hurt >0:
                    self.player_class.speed_x = -10 if bog.dir == 'left' else 10
                    self.player_class.life -= self.boss_group.sprites()[i].hurt
                    get_all_audio()['player_hurt'].play()
                    self.player_class.last_hurt  = get_current_time()
                    break   
        if len(self.boss_group.sprites())>=1 :
            have_boss = [i.boss_name for i in self.boss_group.sprites()]
            if "big_hen" in have_boss:
                    if self.boss_group.sprites()[0].life <=self.boss_group.sprites()[0].max_life/1.01:    
                        num = 10 if  self.boss_group.sprites()[0].life <=self.boss_group.sprites()[0].max_life/3 else 3
                    else:
                        num = 0
                    if len(self.barrage_group.sprites())<num and get_current_time()-self.boss_last_barrage>=500:
                        self.boss_last_barrage = get_current_time()
                        self.barrage_group.add(Barrage('to_player_sprint',
                                                        'feathers',
                                                        random.randint(0,WIDTH),
                                                        random.randint(0,HEIGHT),
                                                        self.player_class,
                                                        False, False, 
                                                        round(BOSS_TYPE['big_hen'][1]/3)))
            if "biggest_hen" in have_boss:
                    num = 15 if  self.boss_group.sprites()[0].life <=self.boss_group.sprites()[0].max_life/3 else 6
                    if len(self.barrage_group.sprites())<num and get_current_time()-self.boss_last_barrage>=500:
                        self.boss_last_barrage = get_current_time()
                        self.barrage_group.add(Barrage('to_player_sprint',
                                                        'feathers',
                                                        random.randint(0,WIDTH),
                                                        random.randint(0,HEIGHT),
                                                        self.player_class,
                                                        False, False, 
                                                        round(BOSS_TYPE['biggest_hen'][1]/3)))
                    if len(self.barrage_group.sprites()) < num+3 and get_current_time()%10000 <= 100:
                        self.boss_last_barrage = get_current_time()
                        self.barrage_group.add(Barrage('drop_item',
                                                       'egg',
                                                       random.randint(0, WIDTH),0,
                                                       self.player_class,
                                                       False, False, 
                                                       round(BOSS_TYPE['biggest_hen'][1]/3)))

    def draw_player_hp(self) -> None:
        if self.player_class.life < 0:
            self.player_class.life = 0
        bar_len = 100 + self.player_class.max_life * 0.5
        bar_height = 20
        fill = (self.player_class.life / self.player_class.max_life) * bar_len
        x = self.surface.get_width() - bar_len-20
        y = 30
        outline_rect = pygame.Rect(x, y, bar_len, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(self.surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(self.surface, "#000000", outline_rect, 2)

        text_surface = PLAYER_FONT.render(str(self.player_class.life)+'/'+
        str(self.player_class.max_life), True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.right = int(self.surface.get_width()-(bar_len-20)/2)
        text_rect.y = 30
        self.surface.blit(text_surface, text_rect)

    def draw_boss_hp(self) -> None:
        
        for i,bos in enumerate(self.boss_group.sprites()):
            draw_boss = self.boss_group.sprites()[i].life/self.boss_group.sprites()[i].max_life
            if bos.life/bos.max_life>draw_boss:
                draw_boss = bos.life        

        if self.boss_group.sprites()[i].life < 0:
            self.boss_group.sprites()[i].life = 0
        bar_len = (100 + self.player_class.max_life * 2)*2
        if bar_len >= self.surface.get_width()/3*2:
            bar_len = self.surface.get_width()/3*2
        bar_height = BOSS_LIFE_HEIGHT
        fill = (self.boss_group.sprites()[i].life / \
            self.boss_group.sprites()[i].max_life) * bar_len
        x = (self.surface.get_width()-bar_len)/2
        y = HEIGHT-50
        
        outline_rect = pygame.Rect(x, y, bar_len, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(self.surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(self.surface, "#000000", outline_rect, 2)
        image_r = 30
        pygame.draw.circle(self.surface,(0,0,0),(x-image_r*0.55,y+(bar_height/2)),image_r)
        pygame.draw.circle(self.surface,(255,255,0),(x-image_r*0.55,y+(bar_height/2)),image_r*0.9)

        boss_image_icon = pygame.transform.scale(self.boss_group.sprites()[i].image,
        (1.3*image_r,1.3*image_r))
        boss_icon_rect = boss_image_icon.get_rect()
        boss_icon_rect.center = (int(x-image_r*0.55),int(y+(bar_height/2)))

        self.surface.blit(boss_image_icon,boss_icon_rect)

        text_surface = BOSS_FONT.render(str(self.boss_group.sprites()[i].life)+'/'+
        str(self.boss_group.sprites()[i].max_life)+\
        f"({round(self.boss_group.sprites()[i].life/self.boss_group.sprites()[i].max_life*100,1)}%)"
            , True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = int(self.surface.get_width()/2)
        text_rect.top = HEIGHT-50
        self.surface.blit(text_surface, text_rect)

    def draw(self,is_opening,page) -> None:
        
        for i,(k,v) in enumerate(self.effect_dict.items()):
            
            self.surface.blit(pygame.transform.scale(IMAGE[k+'_icon'],EFF_TRANSFORM),(10+50*i,90))
            have_time = time_to_frame_time(v,0)
            draw_font(self.surface,INFORMATION_FONT,
                str(round(have_time))+'秒' if have_time<60 else str(have_time//60)+'分钟' ,
                10+50*i,140)

        self.hail_group.draw(self.surface)

        for col in self.could_group:
            col.draw(self.surface)
        self.draw_player_hp()
        if len(self.boss_group) !=0:
            self.draw_boss_hp()

        self.player_sprites.draw(self.surface)
        for smo in self.smoke_list:
            smo.draw(self.surface)
        self.block_sprites.draw(self.surface)
        self.item_group.draw(self.surface)
        for itm in self.item_group.sprites():
            if itm.num > 1:
                draw_font(self.surface,ITEM_NUM_FONT,str(itm.num),
                itm.rect.right-5,itm.rect.bottom-5)
        self.enemy_group.draw(self.surface)
        if self.is_rain:
            for dot in self.droplet_group:
                dot.draw()
        
        
        if len(self.can_synthesis_list)!=0:
            if is_opening:
                for i in range(10 if len(self.can_synthesis_list)%10 == 0 or \
                    page*10 <=len(self.can_synthesis_list) else len(self.can_synthesis_list)%10):
                    self.surface.blit(IMAGE['item_bg'], (15,50*i+206))
            for itp in self.item_pic_group.sprites():
                if itp.image_name != 'None':
                    self.surface.blit(pygame.transform.scale(IMAGE[itp.image_name],
                                                    ITEM_TRANSFORM),itp.rect)

        
        for blk in self.block_sprites.sprites():
            try:
                self.surface.blit(set_block_crack(blk.block_dig_time, blk.dig_time),blk.rect)
            except TypeError:
                pass
        

        self.tile_group.draw(self.surface)
        for til in self.tile_group.sprites():
            try:
                self.surface.blit(set_block_crack(til.tile_dig_time, til.dig_time),til.rect)
            except TypeError:
                pass
            if til.tile_name == 'furnace':
                image:pygame.Surface = pygame.transform.scale(IMAGE['light'],
                (280,280))
                rect_i = image.get_rect()
                rect_i.center = til.rect.center
                self.surface.blit(image,rect_i)
            if til.tile_name == 'torch':
                image:pygame.Surface = pygame.transform.scale(IMAGE['light'],
                (300,300))
                rect_i = image.get_rect()
                rect_i.center = til.rect.center
                self.surface.blit(image,rect_i)
        self.boss_group.draw(self.surface)

        self.barrage_group.draw(self.surface)

        
        if is_opening and len(self.can_synthesis_list)!=0:
            
            for itp in self.item_pic_group:
                if itp.image_name != 'None':
                    itp.draw_self_font()
                    
                    if itp.rect.left <= itp.mouse_pos[0] <= itp.rect.right and itp.mouse_pos[1] <= itp.rect.bottom and itp.mouse_pos[
                        1] >= itp.rect.top:
                        itp.draw_formula()
        self.missile_group.draw(self.surface)
        for dut in self.dust_group:
            dut.draw(self.surface)
        if self.is_open_shop:
            for bun in self.button_list:
                bun.draw(self.surface)
            for i in range(6):
                draw_rounded_square(self.surface,i%3*100+450,i//3*150+155,60,90,3,"blue")
                self.surface.blit(\
            pygame.transform.scale(IMAGE[self.shop_dict[list(self.shop_dict.keys())[i]][0]]
                ,ITEM_TRANSFORM),
            (i%3*100+450,i//3*150+170))
                draw_font(self.surface,ITEM_NUM_FONT,
                'x'+str(self.shop_dict[list(self.shop_dict.keys())[i]][2]),i%3*100+480,i//3*150+170)
                self.surface.blit(\
            pygame.transform.scale(IMAGE[list(self.shop_dict.keys())[i]],ITEM_TRANSFORM),
                (i%3*100+450,i//3*150+220))
                draw_font(self.surface,ITEM_NUM_FONT,
                'x'+str(self.shop_dict[list(self.shop_dict.keys())[i]][1]),i%3*100+480,i//3*150+220)
                pygame.draw.line(self.surface,'#000096',(i%3*100+450,i//3*150+210),
            (i%3*100+510,i//3*150+210),3)
        return 

    def player_collision_detection(self) -> None:
        for i,bls in enumerate(self.block_sprites.sprites()):
            if pygame.sprite.spritecollideany(bls,self.player_sprites):
                self.player_class.do_left_right()
                if pygame.sprite.spritecollideany(bls,self.player_sprites):
                    self.player_class.return_left_right()
                self.player_class.do_up_down()

                if pygame.sprite.spritecollideany(bls,self.player_sprites):
                    self.player_class.return_up_down(self.block_sprites.sprites()[i])
                break
        else:
            self.player_class.do_left_right()
            for bls in self.block_sprites.sprites():
                if pygame.sprite.spritecollideany(bls, self.player_sprites):
                    self.player_class.return_left_right()
                    break
            self.player_class.do_up_down()
            for i,bls in enumerate(self.block_sprites.sprites()):
                if pygame.sprite.spritecollideany(bls, self.player_sprites):
                    self.player_class.return_up_down(self.block_sprites.sprites()[i])
                    break

class Mouse(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image:pygame.Surface = IMAGE['mouse']
        self.rect:pygame.Rect = self.image.get_rect()

    def update(self) -> None:
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]

class Button():
    def __init__(self,left,top,width,height,color,text,font,text_color,command,r=0) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.command = command
        self.r = r
    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.top+self.height>=mouse_pos[1]>=self.top and\
            self.left<=mouse_pos[0]<=self.left+self.width and\
                pygame.mouse.get_pressed()[0]:
            self.command()
    def draw(self,surface) -> None:
        draw_rounded_square(surface,self.left,self.top,
        self.width,self.height,self.r,self.color)
        draw_font(surface,self.font,self.text,
        self.left,self.top,self.text_color)