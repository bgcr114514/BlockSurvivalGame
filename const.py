from math import *
import tomllib
import pygame
import os

pygame.init()


FPS:int = 60

BLOCK_NAME:list[str] = [
    "grass_block",
    "soil_block",
    "stone",
    'wood',
    "iron_block",
    "gold_block",
    'sand_block',
    'coal_block',
    'lucky_block'
]


TILE_NAME:list[str] = [
    "flower_1",
    "flower_2",
    "grass_1",
    "grass_2",
    "grass_3",
    'workbench',
    'glass_bottle',
    'furnace',
    'water_purifier',
    'torch',
    "tile_firecraker"
]

TILE_PUT:list[tuple[int,int]] = [
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40),
    (0,40)
]


BLOCK_DIG_TIME:list[int] = [
    500,
    500,
    1500,
    1000,
    2000,
    1750,
    1000,
    1550 ,
    1000   
]
TILE_DIG_TIME:list[int] = [
    1,
    1,
    1,
    1,
    1,
    1300,
    100,
    1500,
    2000,
    1,
    114514
]


MINERAL_LIST:list[str] = [
    'iron_block',
    'gold_block',
    'coal_block'
]

ENEMY_NAME:list[str] = [
    'cow',
    'dog',
    'hen',
    'worm'
]

#ENEMY_TYPE 排列顺序 {敌人名字:(血量,伤害,frame)}
ENEMY_TYPE:dict[str,tuple[int,int,int]]={
    'hen':(3,0,0),
    'dog':(10,3,0),
    'cow':(20,5,0),
    'worm':(1,0,2)
}
#ENEMY_SPOILS 排列顺序 {敌人名字:([掉落物名],[(掉落最小值,掉落最大值)])}
ENEMY_SPOILS = {
    'hen':(['chicken','feathers'],[(1,2),(1,3)]),
    'dog':(['meat'],[(1,2)]),
    'cow':(['meat','milk'],[(3,10),(1,3)]),
    'worm':(['worm_stive'],[(1,2)])
}

ENEMY_AI_TYPE = {
    'hen':'jog',
    'dog':'run',
    'cow':'jog_neutral',
    'worm':"wrigg"
}

ENEMY_FRAME = {
    'worm':(0.5,0.5)
}

BOSS_TYPE = {
    'big_hen':(3000,5),
    'worm_king':(2000,5),
    'biggest_hen':(4795,8)
}



BOSS_IMAGE_TRANSFORM = {
    'big_hen':('hen',(130,130)),
    'worm_king':('worm_king',(180,80)),
    "biggest_hen":('hen',(200,200))
}

BOSS_SPOILS = {
    'big_hen':(['chicken_leg_bar','chicken','feathers'],[(1,1),(20,50),(50,100)]),
    'worm_king':(['gold_ore'],[(5,8)]),
    'biggest_hen':(['egg_cane','chicken','feathers',"egg"],[(1,1),(20,50),(50,100),(1,10)]),
}

BOSS_FRAME = {
    'worm_king':(0.5,0.5)
}

WIDTH = 1200
HEIGHT = 800

BGCOLOR_ADD = (3/864)*(60/FPS)

CRACK_RATE = 5
CRAFT_SPEED = 3.3
CAN_REACH_LENGTH = 148
CAN_PUT_LENGTH = 160
MOVE_ARM_TIME = 100
MOVE_ARM_SLEEP_TIME = 300
PUT_BLOCK_SLEEP_TIME = 100
FODD_SLEEP_TIME = 30

NUM = float|int

GRAVITY = 1

try:
    username_os = os.getlogin()
except OSError:
    username_os = os.environ['USER']

FILE_STORAGE_ADDRESS:str  = f'C:/Users/{username_os}/AppData/Local/a_block/'
FILE_NAME:str = 'a_block.a_block_file'


ITEM_TRANSFORM:tuple[int,int] = (25,25)
COULD_TRANSFROM = (20,10)
MISSILE_TRANSFROM = (20,20)
EFF_TRANSFORM = (40,40)

BOSS_LIFE_HEIGHT = 25


ITEM_NUM_FONT = pygame.font.Font(pygame.font.match_font('得意黑斜体'),20)
BOSS_FONT = pygame.font.Font(pygame.font.match_font("得意黑斜体"), floor(BOSS_LIFE_HEIGHT/0.9))
PLAYER_FONT = pygame.font.Font(pygame.font.match_font("得意黑斜体"), 15)
INTRODUCE_FONT = pygame.font.Font(pygame.font.match_font('得意黑斜体'), 20)
INFORMATION_FONT = pygame.font.Font(pygame.font.match_font('得意黑斜体'), 20)

INTRODUCE_ROW_NUM = 7

BLOCK_SAVE_NUM = 9
TILE_SAVE_NUM = 5

WHITE = (255,255,255)

KEY_1_TO_0 = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
    pygame.K_0

]

#SYNTHESIS_FORMULA : {合成物:([用来合成的物品],[要合成的数量],合成数量,在哪里合成)}
with open("./toml/syn_table.toml", 'br') as f:
    SYNTHESIS_FORMULA = tomllib.load(f)
with open("./toml/item_introduce.toml", 'br') as f:
    ITEM_INTRODUCE = tomllib.load(f)




EFF_INTRODUCE ={
    'eat_food':'吃饱啦!',
    'antigravity':"轻飘飘的",
    "life_add":"流失的体力正在恢复"
}
with open("./toml/ch_en.toml", 'br') as f:
    CH_EN = tomllib.load(f)

DRAFTS_DIG_MUTIPLE = {
    'hand':1,
    'wood_draft':1.5,
    'stone_draft':2.5,
    'gold_draft':5,
    'iron_draft':3.5
}

FIGHT_MUTIPLE = {
    'hand':1,
    'chicken_leg_bar':3.5,
    'wood_sword':1.5,
    'stone_sword':2,
    'iron_sword':3,
    'gold_sword':2.5,
    'wood_yoyo':1,
    'stone_yoyo':1.5,
    'iron_yoyo':2,
    "egg_cane":0,
}

MISSILE_MUTIPLE = {
    "arrow":1,
    "firecraker":20
}

BARRGE_MUTIPLE = {
    "egg_cane":5,
}

WEAPON_BARRGE = {
    "egg_cane":["drop","egg"]
}

FOOD_GIVE_HP = {
    'chicken':20,
    'meat':25,
    'sugar':5,
    'apple':18,
    'orange':18,
    'sugar_cane':15,
    'tea_bottle':20,
    'milk':21,
    'milk_with_tea':38,
    'worm_stive':6,
}




