import os

os.chdir(os.path.split(__file__)[0])

import pygame
import random
import math

pygame.init()
pygame.mixer.init()

BACKGROUND_SIZE = (360, 720)
screen = pygame.display.set_mode(BACKGROUND_SIZE)

character = pygame.image.load("res/i.png").convert_alpha()
character_rect = character.get_rect()
class Character(pygame.sprite.Sprite):
    def __init__(self):
        self.image = character  # 小人原图
        self.image = pygame.surface.Surface((200,200), pygame.SRCALPHA)
        self.image.blit(character, (100-character_rect.width/2, 200-character_rect.height))
        self.temp_image = self.image  # 临时存放压缩后的图

        self.img_rect = self.image.get_rect()  # 原图方块
        self.temp_rect = self.temp_image.get_rect()  # 压缩后的图方块

        self.origin_width = int(self.img_rect.height)
        self.origin_height = int(self.img_rect.height)  #压缩前原始高度
        self.temp_width = self.origin_width
        self.temp_height = self.origin_height  #压缩后高度
        
        self.pressed = False  # 判断是否准备跳跃
        self.pressing = 0  # 按压深度
        self.jumped = False  # 是否处于跳起状态
        self.jumping = 0  # 跳起高度
        # self.jumping_time = 0  # 跳起时间

        self.direction = 1 # 跳起旋转方向，0逆时针，1顺时针
        
        self.speed = 0
        self.timer = -15
    def press(self):
        if self.jumping: return
        if self.pressed:
            if self.temp_height > self.origin_height/2:
                self.temp_height -= 1
                self.temp_width += 0.2
                self.temp_image = pygame.transform.scale(self.image, (int(self.temp_width), self.temp_height))
                self.pressing += 1
        else:
            if self.pressing:
                self.jumped = True
                self.speed = self.pressing/5
    def _turn_left(self):   # 逆时针跳
        if -12 < self.timer < 12:
            self.temp_image = pygame.transform.rotate(self.image, 360/22*(self.timer+11))
        if self.timer == 12:
            self.temp_image = self.image
    def _turn_right(self):
        if -12 < self.timer < 12:
            self.temp_image = pygame.transform.rotate(self.image, -360/22*(self.timer+11))
            self.temp_rect = self.temp_image.get_rect()
        if self.timer == 12:
            self.temp_image = self.image
    def jump(self):
        if self.jumped:
            if self.temp_height < self.origin_height:
                self.temp_height = self.origin_height if self.temp_height+5 > self.origin_height else self.temp_height+5
                self.temp_image = self.image
                self.temp_width = self.origin_width
            else:
                self.temp_image = self.image
            if self.timer <= 15:
                self.jumping -= self.speed * self.timer / 5
                self.timer += 1
            else:
                self.timer = -15
                self.jumping = 0
                self.jumped = False
                self.speed = 0
                self.pressing = 0
                return True
            if self.direction:
                self._turn_left()
            else:
                self._turn_right()
    def printscreen(self, screen):
        # pygame.draw.rect(self.temp_image, (0,0,0), (0,0,200,200), 3)
        self.temp_rect = self.temp_image.get_rect()
        screen.blit(self.temp_image, (180-self.temp_rect.w/2, 600-self.jumping-self.temp_height-self.temp_rect.h/2))
chara = Character()

def _HSLtoRGB(H,S,L):
    def _HUEtoRGB(v1,v2,vH):
        while vH<0: vH+=1
        while vH>1: vH-=1
        if 6*vH<1: return v1+(v2-v1)*6*vH
        if 2*vH<1: return v2
        if 3*vH<2: return v1+(v2-v1)*(2/3-vH)*6
        return v1
    if S==0:
        R=G=B=int(L*255)
    else:
        if L<0.5: v2=L*(1+S)
        else: v2=L+S-S*L
        v1=2*L-v2
        R=255*_HUEtoRGB(v1,v2,H+1/3)
        G=255*_HUEtoRGB(v1,v2,H)
        B=255*_HUEtoRGB(v1,v2,H-1/3)
    return (int(R),int(G),int(B))

class Square(pygame.sprite.Sprite):
    def __init__(self, size=random.randint(50,200)):
        self.surf = pygame.surface.Surface((400, 400), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surf.get_rect()
        self.pressed = False
        self.temp_surf = self.surf
        self.pressing = 0
        self.temp_height = self.rect.height
        self.reflected = False
        self.trample = False
        self.hue = random.random()
        self.saturation = random.random()
        self.draw(size)
    def draw(self, size):
        pygame.draw.polygon(self.surf, 
                            _HSLtoRGB(self.hue,self.saturation,0.8), 
                            (
                                (200,300),
                                (int(200+size*math.cos(math.pi/6)), int(300-size*math.sin(math.pi/6))),
                                (200, 300-size),
                                (int(200-size*math.cos(math.pi/6)), int(300-size*math.sin(math.pi/6)))
                            ), 
                            )
        pygame.draw.polygon(self.surf,
                            _HSLtoRGB(self.hue,self.saturation,0.75), 
                            (
                                (200,300),
                                (int(200+size*math.cos(math.pi/6)), int(300-size*math.sin(math.pi/6))),
                                (int(200+size*math.cos(math.pi/6)), int(400-size*math.sin(math.pi/6))),
                                (200,400)
                            ),
                            )
        pygame.draw.polygon(self.surf,
                            _HSLtoRGB(self.hue,self.saturation,0.7), 
                            (
                                (200,300),
                                (int(200-size*math.cos(math.pi/6)), int(300-size*math.sin(math.pi/6))),
                                (int(200-size*math.cos(math.pi/6)), int(400-size*math.sin(math.pi/6))),
                                (200,400)
                            ),
                            )
    # 测试用
    def _change_color(self):
        self.hue = random.random()
        self.saturation = random.random() 
        self.draw(random.randint(50,200)) 
    def press(self):
        if self.pressed:
            if self.temp_height > self.rect.height-100:
                self.temp_height -= 1
                self.temp_surf = pygame.transform.scale(self.surf, (400, self.temp_height))
                self.pressing += 1
        else:
            if self.pressing:
                self.reflected = True
    def reflect(self):
        if self.reflected:
            self.temp_height += 5
            if self.temp_height > 400:
                self.temp_height = 400
                self.reflected = False
            self.temp_surf = pygame.transform.scale(self.surf, (400, self.temp_height))
    def printscreen(self, screen):
        screen.blit(self.temp_surf, (-20, 245+self.rect.height-self.temp_height))
s = Square()
    
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    mouse_pressed = pygame.mouse.get_pressed()
    chara.pressed = True if mouse_pressed[0] else False
    s.pressed = chara.pressed
    chara.press()
    s.press()
    chara.jump()
    s.reflect()

    screen.fill((255,255,255))
    s.printscreen(screen)
    chara.printscreen(screen)

    pygame.display.update()
    clock.tick(60)
    
