import pygame.transform
#from loguru import logger

from const import *
from game import *
from utils import *
from ctypes import *

IMAGE = get_all_image()

BGSOUND = get_all_bgsound()
SKY = IMAGE["sky"]
def run() -> None:
    #logger.debug('do main.run()')
    global game,clock,game_bgcolor,t,SCREEN,d,\
    item_choice_num,is_opening,page,information_dict,hour,miun,g_bg
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SRCALPHA)#十分有九分得好
    hwnd = pygame.display.get_wm_info()['window'] 
    windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)
    os.makedirs(FILE_STORAGE_ADDRESS,exist_ok=True)
    pygame.display.set_caption('方块生存')

    pygame.init()
    
    pygame.display.set_icon(IMAGE['grass_block'])


    clock = pygame.time.Clock()
    running:bool = True
    item_choice_num = 0
    is_open_information = False


    read_game_progress()
    if files == '':
        game = Game(SCREEN,item_dict_file,tile_files = tiles_files)

    else:
        game = Game(SCREEN,item_dict_file,files,tiles_files)
    with open('./aaa.kpa','r') as file:
        exec(file.read())
    
    is_opening = 0
    page = 1 

    hour = floor(t/60//60)+12 if t<=150/BGCOLOR_ADD else floor(t/60//60)-12
    miun = floor(t/60%60)

    night_or_day = 'day' if 19>=hour>=6 else 'night'
    
    information_dict = {}
    if night_or_day == 'day':
        sound:pygame.mixer.Sound = BGSOUND['day']
    else:
        sound:pygame.mixer.Sound = BGSOUND['night']
    last_time = night_or_day
    last_have_boss = True if len(game.boss_group)!=0 else False 
    if last_have_boss :
        sound:pygame.mixer.Sound = BGSOUND['boss1']
    
    #sound.play(-1)
    pygame.mouse.set_visible(False)
    yoyo_rotate = 0
    yoyo_x = game.player_class.rect.x
    yoyo_y = game.player_class.rect.y
    lh = hour
    g_bg = 1
    
    while running:
        #固定FPS
        game.player_class.is_x_gone = False if (game.player_class.rect.right<=WIDTH and g_bg == 1)\
             or (game.player_class.rect.right<=0 and g_bg == 2) else True
        mouse_pos = pygame.mouse.get_pos()
        
        clock.tick(FPS)
        night_or_day = 'day' if 19>=hour>=6 else 'night'
        if last_time!=night_or_day or  \
            last_have_boss != (True if len(game.boss_group)!=0 else False) and \
                len(game.boss_group) == 0:
            fade_out(sound, 1000) 
            last_time = night_or_day
            
            
            time.sleep(0.1)
            #sound.stop()
            sound = BGSOUND[last_time]
            sound.play(-1)
            fade_in(sound, 1000)
            last_have_boss =  True if len(game.boss_group)!=0 else False
        if last_have_boss != (True if len(game.boss_group)!=0 else  False) and \
            len(game.boss_group)!=0:
            pygame.mixer.music.load('./bgsound/boss1.mp3')
            pygame.mixer.music.play(-1)
            last_have_boss =  True if len(game.boss_group)!=0 else False
    
        #last_time = night_or_day
        #侦测 keyswhile running:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                for i in range(10): 
                    if event.key == KEY_1_TO_0[i]:
                        item_choice_num = i
                if event.key == pygame.K_e:
                    game.is_open_shop = bool(abs(int(game.is_open_shop)-1))
                if event.key == pygame.K_k:
                    command = write_command()
                    if command!='' and command[0]=='/':
                        do_command(command)
                    else:
                        if command!='':
                            information_dict[f'<{name}>'+command] = get_current_time()
                        
                        


                if event.key == pygame.K_ESCAPE:
                    is_opening = bool(abs(int(is_opening)-1))
                    if is_opening:
                        page=1
                if event.key == pygame.K_F3:
                    is_open_information = bool(abs(int(is_open_information)-1))
                
                if is_opening:
                    if event.key == pygame.K_DOWN and page*10<len(game.can_synthesis_list):
                        page +=1
                    elif event.key == pygame.K_UP and page>1:
                        page -=1
                if event.key == pygame.K_q and len(game.item_dict)-1>=item_choice_num:
                    game.item_group.add(Item(list(game.item_dict.keys())[item_choice_num],
                                                game.player_class.rect.left-20 if game.player_class.dir == 'left' else game.player_class.rect.right+20,
                                                game.player_class.rect.bottom))
                    game.item_dict[list(game.item_dict.keys())[item_choice_num]]-=1
                    if game.item_dict[list(game.item_dict.keys())[item_choice_num]]==0:
                        del game.item_dict[list(game.item_dict.keys())[item_choice_num]]


        #update all things and fill background
        #SCREEN.fill(hsl_to_rgb(210+((hour+miun/60)%24)*15,0.7,0.5))





        #move window code
        if game.player_class.is_x_gone:
            if g_bg == 1:
                g_bg = 2
                if game.player_class.is_x_gone==game.player_class.l_x:
                    for i in game.block_sprites.sprites():
                        i.rect.x-=WIDTH
                    for i in game.tile_group.sprites():
                        i.rect.x-=WIDTH
                    for i in game.item_group.sprites():
                        i.rect.x-=WIDTH
                    for i in game.enemy_group.sprites():
                        i.rect.x-=WIDTH
                    for i in game.boss_group.sprites():
                        i.rect.x-=WIDTH
                    for i in game.barrage_group.sprites():
                        i.rect.x-=WIDTH
                    for i in game.missile_group.sprites():
                        i.rect.x-=WIDTH
                    for i in game.smoke_list:
                        for j in i.particles:                        
                            j.x-=WIDTH
                    
                    
                    
                    
                    game.player_class.rect.x-=WIDTH
                    SCREEN = pygame.display.set_mode((920,HEIGHT))
                    game.player_class.l_x = not game.player_class.is_x_gone
                    
                    
                windll.user32.MoveWindow(hwnd, 990, 0, 920, HEIGHT, False)
        else:
            
            if game.player_class.is_x_gone==game.player_class.l_x and g_bg ==2:
                g_bg = 1
                for i in game.block_sprites.sprites():
                        i.rect.x+=WIDTH
                for i in game.tile_group.sprites():
                        i.rect.x+=WIDTH
                for i in game.item_group.sprites():
                        i.rect.x+=WIDTH
                for i in game.enemy_group.sprites():
                        i.rect.x+=WIDTH
                for i in game.boss_group.sprites():
                        i.rect.x+=WIDTH
                for i in game.barrage_group.sprites():
                        i.rect.x+=WIDTH
                for i in game.missile_group.sprites():
                        i.rect.x+=WIDTH
                for i in game.smoke_list:
                        for j in i.particles:                        
                            j.x+=WIDTH
                game.player_class.rect.x+=WIDTH
                SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
                game.player_class.l_x =  not game.player_class.is_x_gone
                
                    
                windll.user32.MoveWindow(hwnd,-10, 0, WIDTH, HEIGHT, False)





        SCREEN.fill(SKY.get_at((0,20*hour+miun%3)))
        game.update(is_opening,item_choice_num,page,hour,miun)
        
        game.draw(is_opening,page)
        try:
            if 'yoyo' in list(game.item_dict.keys())[item_choice_num] and \
                    pygame.mouse.get_pressed()[0]:
                    
                    yoyo_image:pygame.Surface = pygame.transform.rotate(
                            IMAGE[list(game.item_dict.keys())[item_choice_num]+'_pic'],
                            yoyo_rotate)
                    yoyo_rect = yoyo_image.get_rect()
                    yoyo_x += (mouse_pos[0]-yoyo_x)/5
                    yoyo_y += (mouse_pos[1]-yoyo_y)/5
                    '''if calculate_hypotenuse_length(game.player_class.rect.centerx-yoyo_x,
                    game.player_class.rect.centery-yoyo_y) >=\
                        100+(FIGHT_MUTIPLE[list(game.item_dict.keys())[item_choice_num]]*50):
                        x1,y1 = sympy.symbols('x y')
                        if yoyo_y !=0:
                            eq1 = sympy.Eq(x1/y1,yoyo_x/yoyo_y)
                        else:
                            eq1 = sympy.Eq(x1/y1,yoyo_x)
                        eq2 = sympy.Eq(sympy.sqrt(x1**2+y1**2),
                        100+(FIGHT_MUTIPLE[list(game.item_dict.keys())[item_choice_num]]*50))
                        e = sympy.solve((eq1,eq2),(x1,y1))
                        if len(e) == 2:
                            if game.player_class.rect.centerx-yoyo_x>0 and e[1][0] >0\
                            and game.player_class.rect.centery-yoyo_y>0 and e[1][1] >0:
                                yoyo_x = game.player_class.rect.centerx-e[1][0]
                                yoyo_y = game.player_class.rect.centery-e[1][1]
                            else:
                                yoyo_x = game.player_class.rect.centerx-e[0][0]
                                yoyo_y = game.player_class.rect.centery-e[0][1]'''
                    '''yoyo_length = (100+(((FIGHT_MUTIPLE[list(game.item_dict.keys())[item_choice_num]])-0.5)*60))
                    x = game.player_class.rect.centerx-yoyo_x
                    y = game.player_class.rect.centery-yoyo_y
                    if abs(x)>=yoyo_length:
                        yoyo_x = game.player_class.rect.centerx-(x/abs(x))*yoyo_length
                    if abs(y)>=yoyo_length:
                        yoyo_y = game.player_class.rect.centery-(y/abs(y))*yoyo_length'''

                    yoyo_rect.center = (int(yoyo_x),int(yoyo_y))
                    '''a = game.player_class.rect.centery-((yoyo_y-game.player_class.rect.centery)-100)
                    if a == 0:
                        a = 1
                    num = 5
                    for i in range(0,abs(game.player_class.rect.centerx-yoyo_rect.centerx),num):
                        
                        if yoyo_rect.centerx>game.player_class.rect.centerx:
                            x = game.player_class.rect.centerx+i
                            pygame.draw.line(SCREEN,'white',
                            (x,(x*x/a)),
                            (x+num,((x+num)*(x+num)/a)))
                        else:
                            x = game.player_class.rect.centerx-i
                            pygame.draw.line(SCREEN,'white',
                            (x,game.player_class.rect.centerx-((x*x)/a)+a),
                            (x+num,game.player_class.rect.centerx-(((x+num)*(x+num))/a)+a))'''
                    pygame.draw.line(SCREEN,'white',game.player_class.rect.center,\
                        (yoyo_rect.centerx+(cos(yoyo_rotate)*10),
                        yoyo_rect.centery+(sin(yoyo_rotate)*10)),1)
                    yoyo_rotate+=63
                    #yoyo_rotate %=360
                    SCREEN.blit(yoyo_image,yoyo_rect)
            else:
                    yoyo_x = game.player_class.rect.x
                    yoyo_y = game.player_class.rect.y
                    yoyo_rotate = 0
        except IndexError:

            pass

    #draw item dict things
        draw_rect(SCREEN,38,10,500,47,"#999999")
        for i in range(10):
            if i == item_choice_num:
                draw_rect(SCREEN,42,15+i*50,40,40,"#b9b9b9")#SCREEN.blit(IMAGE['big_item_bg'], (10+i*50,37))
            else:
                draw_rect(SCREEN,42,15+i*50,40,40,"#7e7e7e")
                #SCREEN.blit(IMAGE['item_bg'], (15+i*50,42))
        for _ in range(len(game.item_dict)):
            draw_item_grid(list(game.item_dict.keys())[_],
            game.item_dict[list(game.item_dict.keys())[_]],23+_*50,50)
        if len(game.item_dict)-1>=item_choice_num and len(game.item_dict) != 0:
            if game.player_class.image_name == 'player':
                if game.player_class.dir == 'left':
                    item_image_pic((game.player_class.rect.left,
                    game.player_class.rect.centery)
                                ,list(game.item_dict.keys())[item_choice_num],'left'
                                ,)
                else:
                    item_image_pic((game.player_class.rect.right,
                    game.player_class.rect.centery),
                                list(game.item_dict.keys())[item_choice_num],'right',
                                True)
            else:
                if game.player_class.dir == 'left':
                    item_image_pic((game.player_class.rect.left+20,
                    game.player_class.rect.centery-10),
                                list(game.item_dict.keys())[item_choice_num],'left',
                                )
                else:
                    item_image_pic((game.player_class.rect.right-20,
                    game.player_class.rect.centery-10),
                                list(game.item_dict.keys())[item_choice_num],'right',
                                True)


        # update the bgcolor


        if t<=150/BGCOLOR_ADD:
                game_bgcolor = (153-BGCOLOR_ADD*t,242-BGCOLOR_ADD*t,255-BGCOLOR_ADD*t)
        elif t<=300/BGCOLOR_ADD:
                game_bgcolor = (3 + BGCOLOR_ADD*(t-150/BGCOLOR_ADD), 
                92+ BGCOLOR_ADD*(t-150/BGCOLOR_ADD), 
                105+ BGCOLOR_ADD*(t-150/BGCOLOR_ADD))
        else:
                t = 0

        t += 1
        hour = floor(t/FPS//60)+12 if t<=150/BGCOLOR_ADD else floor(t/FPS//60)-12
        miun = floor(t/FPS%60)
        
        if t == 300/BGCOLOR_ADD/2:
            d +=1
            lh = 0
        else:
            lh = hour
        
        
        draw_things = '0'*(2-len(str(hour)))+str(hour)+':'+'0'*(2-len(str(miun)))+str(miun)

        

        if 37<mouse_pos[1]<77 and 10<mouse_pos[0]<510 and len(game.item_dict)-1 >= mouse_pos[0]//50:
            draw_item_introduce(mouse_pos[0]//50)
        try:
            if get_current_time()%500 <= 20 and pygame.mouse.get_pressed()[0] and list(game.item_dict.keys())[item_choice_num] in BARRGE_MUTIPLE.keys():
                if WEAPON_BARRGE[list(game.item_dict.keys())[item_choice_num]][0] == "drop":
                    game.barrage_group.add(Barrage("drop_item",
                                                WEAPON_BARRGE[list(game.item_dict.keys())[item_choice_num]][1] ,
                                                pygame.mouse.get_pos()[0],
                                                -40,
                                                game.player_class,
                                                friendly = True,
                                                aggression=True,
                                                hurt = BARRGE_MUTIPLE.get(list(game.item_dict.keys())[item_choice_num]),
                                                retention_time=inf))
        except IndexError:
            pass

        if 10<mouse_pos[0]<10+len(game.effect_dict)*50 and 87<mouse_pos[1]<127 and \
            len(game.effect_dict)>0 and len(game.effect_dict)-1 >= mouse_pos[0]//50:
            draw_eff_introduce(mouse_pos[0]//50)
        if 37<mouse_pos[1]<77 and 10<mouse_pos[0]<500 and pygame.mouse.get_pressed()[0]:
            item_choice_num = mouse_pos[0]//50
        if is_open_information:
            draw_information()
        text_surface = ITEM_NUM_FONT.render(draw_things, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centery = 100
        text_rect.right = WIDTH-30
        SCREEN.blit(text_surface, text_rect)
        # border_surface = pygame.Surface((text_surface.get_width() + 2 * 2, text_surface.get_height() + 2 * 2), pygame.SRCALPHA)
        # for dx, dy in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
        #     border_surface.blit(text_surface, (dx, dy))
        # text_surface = ITEM_NUM_FONT.render(draw_things, True, (255,255,255))
        # border_surface.blit(text_surface, (2, 2))
        # SCREEN.blit(border_surface, text_rect)
        

        #SCREEN.blit(text_surface, text_rect)

        draw_font(SCREEN,PLAYER_FONT,name,game.player_class.rect.centerx-(len(name)/2*5),
        game.player_class.rect.top-PLAYER_FONT.get_linesize())
        i = 1
        del_list_i = []
        for k,v in information_dict.items():
            draw_font(SCREEN,INFORMATION_FONT,k,10,HEIGHT-70-20*(len(information_dict)-i))
            i+=1
            if get_current_time()-v>=10000 or i>10:
                del_list_i.append(k)
        for h1 in del_list_i:
            del information_dict[h1]
        
        SCREEN.blit(IMAGE['mouse'],game.mouse.rect)
        
        #update
        pygame.display.update()

    save_and_exit()
    #logger.debug('end all')
    pygame.quit()

def do_command(command:str) -> None:
    global t
    if command[1:4] =='eff':
            if command[4] == ' ':
                c = command[5]
                j = 5
                while c != ' ':
                    j+=1
                    c = command[j]
                    if j==len(command)-1:
                        if command[5:] in list(EFF_INTRODUCE.keys()):
                            game.effect_dict[command[5:]] = 30*FPS
                            game.last_eat_food = get_current_time()
                            break
                        else:
                            information_dict['错误:没有这个效果'] = get_current_time()
                            break
                                        
                else:
                    if command[5:j] in list(EFF_INTRODUCE.keys()):
                        k = True
                        for c in command[j+1:]:
                            k= k and c in '0123456789'
                        if k: 
                            game.last_eat_food = get_current_time()
                            game.effect_dict[command[5:j]] = int(command[j+1:])/1000*FPS
                        else:
                            information_dict['错误:效果后应跟数字'] = get_current_time()
                    else:
                        information_dict['错误:没有这个效果'] = get_current_time()
    elif len(command)>=9 and command[1:9] =='time_set':
        if t>300/BGCOLOR_ADD:
            information_dict[f'错误:时间应小于等于{300/BGCOLOR_ADD}'] = get_current_time()
        else:
            try:
                t = int(command[10:])
            except ValueError:
                information_dict['错误:后面应带整数'] = get_current_time()
    elif len(command) == 14 and command[1:8] == 'weather':
            if command[9] in '01' and command[11] in '01' and command[13] in '01':
                if command[9] =='1':
                    game.next_rain = get_current_time()
                else:
                    game.rain_end_time = get_current_time()
                if command[11] == '1':
                    game.next_hail = get_current_time()
                else:
                    game.hail_end_time = get_current_time()
                if command[13] == '1':
                    game.next_wind = get_current_time()
                else:
                    game.wind_end_time = get_current_time()
            else:
                information_dict['错误:后面三个参数应带0或1'] = get_current_time()
    elif len(command)>=13 and command[1:11] == 'wind_speed':
            try:
                game.wind_speed = int(command[12:])
            except ValueError:
                information_dict['错误:后面应带整数'] = get_current_time()
    elif len(command)>=5 and command[1:5] == 'give':
        if len(game.item_dict)<10:
            c = command[7]
            j = 7
            while c != ' ':
                j+=1
                c = command[j]
                if j==len(command)-1:
                    if command[6:] in list(CH_EN.keys()):
                        try:
                            if game.item_dict.get(command[6:]) != None:
                                    game.item_dict[command[6:]] +=1 
                            else:
                                    game.item_dict[command[6:]] =1 
                        except ValueError:
                            information_dict['错误:后面应带整数'] = get_current_time()
                        break
                    else:
                        information_dict['错误:没有这个物品'] = get_current_time()
                        break
            else:
                if command[6:j] in list(CH_EN.keys()):
                    try:
                        if game.item_dict.get(command[6:j]) != None:
                            game.item_dict[command[6:j]] += int(command[j:])
                        else:
                            game.item_dict[command[6:j]] = int(command[j:])
                    except ValueError:
                        information_dict['错误:后面应带整数'] = get_current_time()
                else:
                    information_dict['错误:没有这个物品'] = get_current_time()
    elif command[1:4] == 'aCE':
        if command[5:].replace(" ","_") in CH_EN.keys():
            information_dict[f'错误:这个名字已经被使用过了'] = get_current_time()
        else:
            CH_EN[command[5:].replace(" ","_")] = \
                hex(int(bin((len(CH_EN))**2+1).replace('0b','')))[2:].upper()
                        
def draw_information() -> None:
    #logger.debug('do main.draw_information()')
    thing = f'FPS:{round(clock.get_fps())}\n\
wind_speed:{game.wind_speed}px/s\n\
is_rain_hail_wind:{str(game.is_rain)},{str(game.is_hail)},{str(game.is_have_wind)}\n\
have_tiles(en):{str(game.have_tile)}\n\
player_speed_y:{str(game.player_class.speed_y)}\n\
Day:{d}\n\
mouse_pos:{pygame.mouse.get_pos()}\n\
'
    draw_font(SCREEN,INFORMATION_FONT,thing,10,10)

def draw_item_introduce(item_choice_num:int) -> None:
    #logger.debug('do main.draw_item_introduce()')
    try:item_name = list(game.item_dict.keys())[item_choice_num]
    except IndexError:item_name='hand'

    introduce = ITEM_INTRODUCE.get(item_name,'')
    if len(introduce)>INTRODUCE_ROW_NUM and len(introduce)%INTRODUCE_ROW_NUM!=0:
        height = (len(introduce)//INTRODUCE_ROW_NUM+3)*25
    elif introduce == '':
        height = 50
    else:
        height = 75
    introduce_rect = pygame.Rect(10+item_choice_num*50,90,150,height)
    pygame.draw.rect(SCREEN,'#5a60af',introduce_rect)
    
    
    if len(introduce)>INTRODUCE_ROW_NUM and introduce!='':
        for i in range(len(introduce)//INTRODUCE_ROW_NUM):
            introduce = introduce[:i*INTRODUCE_ROW_NUM+INTRODUCE_ROW_NUM]+'\n'+\
                introduce[i*INTRODUCE_ROW_NUM+INTRODUCE_ROW_NUM:]
    draw_font(SCREEN,INTRODUCE_FONT,
        f'{CH_EN[item_name]},\n伤害: {FIGHT_MUTIPLE.get(item_name,1)+BARRGE_MUTIPLE.get(item_name,0)},\n'+introduce
        ,12+item_choice_num*50,92)

def draw_eff_introduce(num:int) -> None:
    #logger.debug('do main.draw_eff_introduce()')
    name = list(game.effect_dict.keys())[num]
    introduce = ITEM_INTRODUCE.get(name,'')
    if len(introduce)>INTRODUCE_ROW_NUM and len(introduce)%INTRODUCE_ROW_NUM!=0:
        height = (len(introduce)//INTRODUCE_ROW_NUM+3)*25
    elif introduce == '':
        height = 50
    else:
        height = 75
    introduce_rect = pygame.Rect(10+num*50,160,150,height)
    pygame.draw.rect(SCREEN,'#5a60af',introduce_rect)
    
    
    if len(introduce)>INTRODUCE_ROW_NUM and introduce!='':
        for i in range(len(introduce)//INTRODUCE_ROW_NUM):
            introduce = introduce[:i*INTRODUCE_ROW_NUM+INTRODUCE_ROW_NUM]+'\n'+introduce[i*INTRODUCE_ROW_NUM+INTRODUCE_ROW_NUM:]
    draw_font(SCREEN,INTRODUCE_FONT,
        EFF_INTRODUCE[name]
                ,12+num*50,162)

def save_and_exit() -> None:
        #logger.debug('save and exit')
        open(FILE_STORAGE_ADDRESS + FILE_NAME, 'w') .write('')
        open(FILE_STORAGE_ADDRESS + 'tile.a_block_file', 'w').write('')
        for blk in range(len(game.block_sprites.sprites())):

            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(game.block_sprites.sprites()[blk].block_num) + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(game.block_sprites.sprites()[blk].block_name + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(game.block_sprites.sprites()[blk].dig_time) + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(game.block_sprites.sprites()[blk].rect.x+( 0 if g_bg == 1 else WIDTH)) + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(game.block_sprites.sprites()[blk].rect.y) + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(game.block_sprites.sprites()[blk].last_block + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(game.block_sprites.sprites()[blk].last_x) + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(game.block_sprites.sprites()[blk].last_y) + '\n')
            open(FILE_STORAGE_ADDRESS + FILE_NAME, 'a').write(str(int(game.block_sprites.sprites()[blk].is_player_put)) + '\n')
        open(FILE_STORAGE_ADDRESS + 'item_dict.a_block_file', 'w').write(str(game.item_dict))
        open(FILE_STORAGE_ADDRESS + 'game.a_block_file', 'w').\
            write(str(t)+'\n'+str(game_bgcolor)+'\n'+str(d)+'\n')
        for til in range(len(game.tile_group.sprites())):
            open(FILE_STORAGE_ADDRESS + 'tile.a_block_file', 'a').write(str(game.tile_group.sprites()[til].tile_num) + '\n')
            open(FILE_STORAGE_ADDRESS + 'tile.a_block_file', 'a').write(str(game.tile_group.sprites()[til].tile_name) + '\n')
            open(FILE_STORAGE_ADDRESS + 'tile.a_block_file', 'a').write(str(game.tile_group.sprites()[til].dig_time) + '\n')
            open(FILE_STORAGE_ADDRESS + 'tile.a_block_file', 'a').write(str(game.tile_group.sprites()[til].rect.x) + '\n')
            open(FILE_STORAGE_ADDRESS + 'tile.a_block_file', 'a').write(str(game.tile_group.sprites()[til].rect.y) + '\n')

def write_user_name() -> str:
    #logger.debug('do main.write_uaer_name()')
    running = True
    username = ''
    while running:
    # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果点击关闭按钮
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 如果按下键盘按键
                if event.key == pygame.K_RETURN:  # 如果按下回车键
                    # 开始文本输入
                    pygame.key.start_text_input()
                elif event.key == pygame.K_BACKSPACE:  # 如果按下退格键
                    # 删除用户名的最后一个字符
                    username = username[:-1]
            elif event.type == pygame.KEYUP:  # 如果释放键盘按键
                if event.key == pygame.K_RETURN:  # 如果释放回车键
                    # 停止文本输入
                    if username!='':
                        pygame.key.stop_text_input()
                        running = False
            elif event.type == pygame.TEXTINPUT:  # 如果有文本输入
                # 将文本追加到用户名
                if len(username)<=10:
                    username += event.text
    
        # 清除屏幕并重绘
        SCREEN.fill((255, 255, 255))
        
    
        # 在屏幕上显示用户名
        font = pygame.font.SysFont('得意黑斜体', 20)
        text = font.render('用户名: ' + username, True, (255,255,255))
        SCREEN.blit(text, (10, 10))
    
        # 更新屏幕显示
        pygame.display.flip()
    open(FILE_STORAGE_ADDRESS + 'user.a_block_file','w').write(username)
    return username

def write_command()->str:
    #logger.debug('do main.write_command()')
    running = True
    command = ''
    pygame.key.start_text_input()
    while running:
    # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果点击关闭按钮
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 如果按下键盘按键
                '''if event.key == pygame.K_RETURN:  # 如果按下回车键
                    # 开始文本输入
                    pygame.key.start_text_input()'''
                if event.key == pygame.K_ESCAPE:
                    return ''
                if event.key == pygame.K_BACKSPACE:  # 如果按下退格键
                    # 删除用户名的最后一个字符
                    command = command[:-1]
            elif event.type == pygame.KEYUP:  # 如果释放键盘按键
                if event.key == pygame.K_RETURN:  # 如果释放回车键
                    # 停止文本输入
                    pygame.key.stop_text_input()
                    running = False
            elif event.type == pygame.TEXTINPUT:  # 如果有文本输入
                # 将文本追加到用户名
                command += event.text
        SCREEN.fill(game_bgcolor)
        game.draw(is_opening,page)


        draw_things = '0'*(2-len(str(hour)))+str(hour)+':'+'0'*(2-len(str(miun)))+str(miun)
        text_surface = ITEM_NUM_FONT.render(draw_things, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centery = 100
        text_rect.right = WIDTH-30
        SCREEN.blit(text_surface, text_rect)
        
        draw_font(SCREEN,PLAYER_FONT,name,game.player_class.rect.centerx-(len(name)/2*5),
        game.player_class.rect.top-PLAYER_FONT.get_linesize())
        #draw item dict things
        for i in range(10):
            if i == item_choice_num:
                SCREEN.blit(IMAGE['big_item_bg'], (10+i*50,37))
            else:
                SCREEN.blit(IMAGE['item_bg'], (15+i*50,42))
        for _ in range(len(game.item_dict)):
            draw_item_grid(list(game.item_dict.keys())[_],game.item_dict[list(game.item_dict.keys())[_]],23+_*50,50)
        if len(game.item_dict)-1>=item_choice_num and len(game.item_dict) != 0:
            if game.player_class.image_name == 'player':
                if game.player_class.dir == 'left':
                    item_image_pic((game.player_class.rect.left,game.player_class.rect.centery)
                                ,list(game.item_dict.keys())[item_choice_num],'left')
                else:
                    item_image_pic((game.player_class.rect.right,game.player_class.rect.centery),
                                list(game.item_dict.keys())[item_choice_num],'right',True)
            else:
                if game.player_class.dir == 'left':
                    item_image_pic((game.player_class.rect.left+20,game.player_class.rect.centery-10),
                                list(game.item_dict.keys())[item_choice_num],'left')
                else:
                    item_image_pic((game.player_class.rect.right-20,game.player_class.rect.centery-10),
                                list(game.item_dict.keys())[item_choice_num],'right',True)
        for i,(k) in enumerate(information_dict.keys()):
            draw_font(SCREEN,INFORMATION_FONT,k,10,HEIGHT-70-20*(len(information_dict)-i))
            information_dict[k] += 1/clock.get_fps()
        introduce_rect = pygame.Rect(0,HEIGHT-52,WIDTH,24)
        pygame.draw.rect(SCREEN,'#7c7c7c',introduce_rect)
        if time.time()*1000%1000<500:
            introduce_rect = \
        pygame.Rect(10+INFORMATION_FONT.render(command,True,"#000000").get_width(),HEIGHT-50,3,20)
            pygame.draw.rect(SCREEN,'#000000',introduce_rect)
        # 在屏幕上显示用户名
        font = pygame.font.SysFont('得意黑斜体', 20)
        text = font.render(command, True, (255,255,255))
        SCREEN.blit(IMAGE['mouse'],pygame.mouse.get_pos())
        SCREEN.blit(text, (10, HEIGHT-50))
        
        # 更新屏幕显示
        pygame.display.flip()
    return command

def read_game_progress() -> None:
        global files,item_dict_file,game_bgcolor,t,tiles_files,name,d
        try:
            name=open(FILE_STORAGE_ADDRESS + 'user.a_block_file','r').readlines()[0]
        except FileNotFoundError:
            
            
            name = write_user_name()
        try:
            files=open(FILE_STORAGE_ADDRESS + FILE_NAME,'r').readlines()
        except FileNotFoundError:
            files = ''

        try:
            item_dict_file = eval(eval(str(open(FILE_STORAGE_ADDRESS + 'item_dict.a_block_file', 'r').readlines()).split('\n')[0])[0])
        except FileNotFoundError:
            item_dict_file = {}
        try:
            d = int(open(FILE_STORAGE_ADDRESS + 'game.a_block_file', 'r').readlines()[2].split('\n')[0])
            
            game_bgcolor = eval(open(FILE_STORAGE_ADDRESS + 'game.a_block_file', 'r').readlines()[1].split('\n')[0]) #153, 242, 255

            t = int(open(FILE_STORAGE_ADDRESS + 'game.a_block_file', 'r').readlines()[0].split('\n')[0])
        except FileNotFoundError:
            game_bgcolor = 153, 242, 255
            t = 0
            d = 0
            y = 0
        try:
            tiles_files=open(FILE_STORAGE_ADDRESS + 'tile.a_block_file','r').readlines()
        except FileNotFoundError:
            tiles_files= ''
            
def draw_item_grid(name:str,num:int,x:int,y:int) -> None:
        #draw item image  
        SCREEN.blit(pygame.transform.scale(IMAGE[name],ITEM_TRANSFORM),(x,y))
        
        #draw item number
        text_surface = ITEM_NUM_FONT.render(format_number(num), True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = x+ITEM_TRANSFORM[0]
        text_rect.top = y+ITEM_TRANSFORM[1]
        SCREEN.blit(text_surface, text_rect)
        # border_surface = pygame.Surface((text_surface.get_width() + 2 * 2, text_surface.get_height() + 2 * 2), pygame.SRCALPHA)
        # for dx, dy in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
        #     border_surface.blit(text_surface, (dx, dy))
        # text_surface = ITEM_NUM_FONT.render(format_number(num), True, (255,255,255))
        # border_surface.blit(text_surface, (2, 2))
        # SCREEN.blit(border_surface, text_rect)

def item_image_pic(rect:tuple,name:str,left_right:str,is_filp:bool=False) -> None:
        if is_filp:
            image_surface = pygame.transform.flip(\
            pygame.transform.scale(IMAGE[name],ITEM_TRANSFORM),True,False)
        else:
            image_surface = pygame.transform.flip(\
                pygame.transform.scale(IMAGE[name], ITEM_TRANSFORM), False, False)
        image_rect = image_surface.get_rect()
        if left_right == 'left':
            image_rect.right = rect[0]
        else:
            image_rect.left = rect[0]
        image_rect.bottom = rect[1]
        SCREEN.blit(image_surface,image_rect)

if __name__ == '__main__':
    run()