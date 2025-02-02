import os
import pathlib
import time
from math import sqrt

import cv2
import pygame

from const import *

folder = pathlib.Path(__file__).parent.resolve()
pygame.init()
def get_all_image() -> dict[str, pygame.Surface]:
    image_dic:dict[str, pygame.Surface] = {}
    for image in os.listdir(str(folder)+'/image'):
        name = os.path.splitext(image)[0]
        path = os.path.join(str(folder)+'/image', image)
        image_dic[name] = pygame.image.load(path)
        if name in BLOCK_NAME or name in TILE_NAME:
            image_dic[name+'alpha'] = pygame.image.load(path)
            image_dic[name+'alpha'].set_alpha(128)
    return image_dic

def get_all_audio() -> dict:
    audio_dic = {}
    for audio in os.listdir(str(folder)+'/audio'):
        name, extension = os.path.splitext(audio)
        path = os.path.join(str(folder)+'/audio', audio)
        audio_dic[name] = pygame.mixer.Sound(path)
    return audio_dic

def get_all_bgsound() -> dict:
    bgsound_dic = {}
    for bgsound in os.listdir(str(folder)+'/bgsound'):
        name, extension = os.path.splitext(bgsound)
        path = os.path.join(str(folder)+'/bgsound', bgsound)
        bgsound_dic[name] = pygame.mixer.Sound(path)
    return bgsound_dic
def find_block_tile(find_type:str, find_num:int) -> str|None:
    if find_type == 'block' or find_type == 'tile':
        if find_type == 'block':
            if find_num <= len(BLOCK_NAME):
                return BLOCK_NAME[find_num-1]
        else:
            if find_num <= len(TILE_NAME):
                return TILE_NAME[find_num-1]
    return
def get_current_time():
    t = time.time()
    return int(t*1000)


calculate_fractions = lambda numerator, denominator: numerator/denominator

#两值分别为(分子,分母)

def draw_font(surface:pygame.Surface,
                font:pygame.font.Font,
                text:str,
                x:NUM,
                y:NUM,
                color:tuple[int,int,int]|str|pygame.Color=(255,255,255),
                antialias:bool=True,
                ):

    lines = text.splitlines()
    for i, line in enumerate(lines):
        text_surface = font.render(line, antialias, color)
        add_y = i * font.get_linesize()
        surface.blit(text_surface, (x, y+add_y))
def draw_rect(surface:pygame.Surface,
                top:NUM,
                left:NUM,
                width:NUM,
                heigth:NUM,
                color:tuple[int,int,int]|str|pygame.Color,) -> None:
    pygame.draw.rect(surface,color,pygame.Rect(left,top,width,heigth))
def set_block_crack(block_dig_time:NUM,dig_time:NUM):
    if block_dig_time * 0.2 >= dig_time >= block_dig_time * 0.1:
        return block_crack_image('1')
    elif block_dig_time * 0.4 >= dig_time >= block_dig_time * 0.2:
        return block_crack_image('2')
    elif block_dig_time * 0.6 >= dig_time >= block_dig_time * 0.4:
        return block_crack_image('3')
    elif block_dig_time >= dig_time >= block_dig_time * 0.6:
        return block_crack_image('4')
    elif dig_time >= block_dig_time:
        return False
        
    else:
        return 'not have crack'
calculate_hypotenuse_length = lambda a, b:sqrt(a*a+b*b)
def get_crack_image():
    image_dic = {}
    for image in os.listdir(str(folder)+'/block_crack'):
        name, extension = os.path.splitext(image)
        path = os.path.join(str(folder)+'/block_crack', image)
        image_dic[name] = pygame.image.load(path)
    return image_dic
get_crack_image_ = get_crack_image()

block_crack_image = lambda num:get_crack_image_[num]





def get_velue_position(list:list, velue, nat_return=None):
    position = 1
    for k in list:
        if k == velue:
            return position
        position += 1
    return nat_return

def frame_time_to_time(s:NUM) -> float | int:
    return s*FPS

def time_to_frame_time(frame:NUM,round_num:int) -> float:
    return round(frame/FPS,round_num)

def is_boss_in_group(boss_group:pygame.sprite.Group,boss_name:str) -> bool:
    things = [not boss_name in i.boss_name for i in boss_group.sprites()]
    k = True
    for j in things:
        k = k and j
    return k
def pygame_set_alpha(image_path,alpha) -> pygame.Surface:
    
    image = cv2.imread(image_path)
    
    # 调整图片亮度
    brightness_factor = alpha # 亮度调整因子，可以根据需要进行调整
    adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor)
    adjusted_image = cv2.cvtColor(adjusted_image,cv2.COLOR_BGR2RGB)
    return pygame.image.frombuffer\
        (adjusted_image.tobytes(), adjusted_image.shape[1::-1], "RGB")
def get_alpha(h,m):
    return (-(h+m/60-12)*(h+m/60-12)+250)/250

def draw_rounded_square(surface:pygame.Surface,
                        left:NUM,
                        top:NUM,
                        width:NUM,
                        height:NUM,
                        r:int,
                        color:tuple|str|pygame.Color) -> None:
    if r*2<min(width,height):
        pygame.draw.rect(surface,color,(left,top,width,height),border_radius=r)

import threading


def set_volume(sound, volume):
    sound.set_volume(volume)

def fade_out(sound, duration, steps=100):
    start_volume = sound.get_volume()
    for step in range(steps):
        volume = start_volume * (1 - step / steps)
        threading.Timer(steps/duration, set_volume, args=(sound, volume)).start()
    

def fade_in(sound, duration, steps=100):
    for step in range(steps):
        volume = step / steps
        threading.Timer(steps/duration, set_volume,
                        args=(sound, volume)).start()
        
def format_number(value:NUM) -> str:
    if value >=1_000_000_000_000:
        return f'{value:.2e}'

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value}"
'''def hsl_to_rgb(h,s,l):
    h = h/360.0
    if s == 0:
        r = g = b = int(l*255)
    else:
        def hue2rgb(p,q,t):
            t+=1 if t<0 else 0
            t-=1 if t>1 else 0
            if t<1/6:
                return p+(q-p)*6*t
            if t<1/2:
                return q
            if t<2/3:
                return p+(q-p)*(2/3-t)*6
            return p
        q = l*(1+s) if l < 0.5 else l+s-l*s
        p = 2*l-q
        r = hue2rgb(p,q,h+1/3)
        g = hue2rgb(p,q,h)
        b = hue2rgb(p,q,h-1/3)
    return (int(r*255),int(g*255),int(b*255))'''
def hsl_to_rgb(h, s, l):
    """
    将 HSL 转换为 RGB（精确匹配在线工具结果）
    :param h: 色相（0-360）
    :param s: 饱和度（0.0-1.0）
    :param l: 亮度（0.0-1.0）
    :return: (R, G, B) 范围 0-255
    """
    h = h / 360.0
    if s == 0:
        r = g = b = int(l * 255)
    else:
        def hue_to_rgb(p, q, t):
            t += 1 if t < 0 else 0
            t -= 1 if t > 1 else 0
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return (int(r * 255), int(g * 255), int(b * 255))
