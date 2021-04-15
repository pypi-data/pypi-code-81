from base64 import b64decode
import pygame
import keyboard
import os
import math

clock = pygame.time.Clock()

pygame.font.init()

playerX = 0
playerY = 0
playerZ = 0

camRot = [0,0,0]
camVel = [0,0,0]
camSens = 6

mouseRightDown = False
mouseLeftDown = False

mouseSpeed = 0

lockMouse = False
showMouse = True

playerSpeed = 0

playerVel = [0,0,0]

def pgEvents():
    global playerZ,playerVel
    global camSens,camVel,camRot
    global mouseSpeed,lockMouse
    global mouseRightDown,mouseLeftDown
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.MOUSEMOTION:
            dx,dy = event.rel
            mouseSpeed = (dx ** 2 + dy ** 2) ** (1/2)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                playerVel[2] = playerSpeed
                return "K_w"
            if event.key == pygame.K_s:
                playerVel[2] = -playerSpeed
                return "K_s"
            if event.key == pygame.K_a:
                playerVel[0] = playerSpeed
                return "K_a"
            if event.key == pygame.K_d:
                playerVel[0] = -playerSpeed
                return "K_d"
            #if event.key == pygame.K_LEFT:
            #    camVel[0] = camSens
            #    return "K_LEFT"
            #if event.key == pygame.K_RIGHT:
            #   camVel[0] = -camSens
            #   return "K_RIGHT"
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                playerVel[2] = 0
                return "K_w2"
            if event.key == pygame.K_s:
                playerVel[2] = 0
                return "K_s2"
            if event.key == pygame.K_a:
                playerVel[0] = 0
                return "K_a2"
            if event.key == pygame.K_d:
                playerVel[0] = 0
                return "K_d2"
            #if event.key == pygame.K_LEFT:
            #    camVel[0] = 0
            #    return "K_LEFT2"
            #if event.key == pygame.K_RIGHT:
            #    camVel[0] = 0
            #    return "L_RIGHT2"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            if event.button == 3:
                mouseRightDown = True
                return "RIGHTMOUSEDOWN"
            if event.button == 1:
                mouseLeftDown = True
                return "LEFTMOUSEDOWN"
            return "MOUSEDOWN"
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                mouseRightDown = False
                return "RIGHTMOUSEDOWN1"
            if event.button == 1:
                mouseLeftDown = False
                return "LEFTMOUSEDOWN1"
            return "MOUSEUP"

            

class Win:
    def __init__(self,w,h,cap,icon=None,hz=144):
        self.w = w
        self.h = h
        self.hz = hz
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(cap)
        if icon == None:
            iconDataUri = "data:image/png;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANAIpP8P3sak7cyUXx0AAAAASUVORK5CYII="
            header,encoded = iconDataUri.split(",",1)
            iconDataUri = b64decode(encoded)
            open("image.png","wb").write(iconDataUri)
            pygame.display.set_icon(pygame.image.load("image.png"))
            os.remove("image.png")
        else:
            pygame.display.set_icon(pygame.image.load(icon[0]))
    def update(self):
        global showMouse
        if pgEvents() == "QUIT":
            quit()

        if showMouse == False:
            pygame.mouse.set_visible(False)
        if showMouse == True:
            pygame.mouse.set_visible(True)
            
        pygame.display.update()
        clock.tick(self.hz)

class Sky:
    def __init__(self,win,color):
        self.color = color
        self.win = win
    def draw(self):
        self.win.screen.fill(self.color)
        
class ImgSky:
    def __init__(self,win,img):
        self.win = win
        self.img = pygame.image.load(img)
    def draw(self):
        self.img = pygame.transform.scale(self.img,(self.win.w,self.win.h))
        self.win.screen.blit(self.img,(0,0))

class Ground:
    def __init__(self,win,color,h):
        self.win = win
        self.color = color
        self.h = h
    def draw(self):
        pygame.draw.rect(self.win.screen,self.color,(0,self.win.h-self.h,self.win.w,self.h))

class Obj:
    def __init__(self,win,x,y,z,w,h,img,fixy=1,collision=False,hboxsize=1):
        self.win = win
        self.x = x
        self.y = y
        self.imga = img
        self.fixy = fixy
        self.z = z
        self.w = w
        self.h = h
        self.y = self.y/fixy
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(self.w,self.h))
        self.collision = collision
        self.enabled = True
        self.hboxsize = hboxsize
    def draw(self):
        if self.enabled:
            global playerZ,playerX,camRot,playerSpeed

            self.x += camVel[0]
            
            if self.w+playerZ-self.z < 1:
                return
            if self.h+playerZ-self.z < 1:
                return
            if self.w+playerZ-self.z > 799:
                return
            if self.h+playerZ-self.z > 799:
                return

            if self.x > self.win.w + self.win.w/2:
                self.x = 0 - self.win.w - self.win.w/2
            if self.x < 0 - self.win.w - self.win.w/2:
                self.x = self.win.w + self.win.w/2

            if self.collision:
                dis = math.sqrt(math.pow(self.x-int(playerZ)+playerX-playerZ,2))
                if dis < self.hboxsize:
                    playerZ -= playerSpeed

            self.img = pygame.image.load(self.imga)
            self.img = pygame.transform.scale(self.img,(self.w+playerZ-self.z,self.h+playerZ-self.z))
            
            self.win.screen.blit(self.img,(self.x-int(playerZ)+playerX,self.win.h-self.h-self.y-playerZ))
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False
    def getDistance(self):
        global playerX,playerZ
        return math.sqrt(math.pow(self.x-int(playerZ)+playerX-playerZ,2))

class FPPlayer:
    def __init__(self,win,speed=5):
        global lockMouse
        self.win = win
        self.speed = speed
        lockMouse = True
    def work(self):
        global playerZ,playerX
        global playerSpeed
        global camRot,camVel,camSens
        global lockMouse,mouseSpeed,mouseRightDown

        mx,my = pygame.mouse.get_pos()
        
        playerSpeed = self.speed
        playerZ += playerVel[2]
        playerX += playerVel[0]

        camRot[0] += camVel[0]
        camRot[1] += camVel[1]
        camRot[2] += camVel[2]

        if camRot[0] < -360:
            camRot[0] = 360
        if camRot[0] > 360:
            camRot[0] = -360

        if mouseSpeed < 1:
            mouseSpeed = 0

        if mx < 400:
            camVel[0] = int(mouseSpeed/10-1)
        if mx > 400:
            camVel[0] = -int(mouseSpeed/10-1)

        #camVel[0] = int(mouseSpeed/10-1)
        

        if lockMouse == True:
            pygame.mouse.set_pos(self.win.w/2,self.win.h/2)
            pygame.event.set_grab(True)
            
    def unlockMouse(self):
        global lockMouse
        lockMouse = False
        pygame.event.set_grab(False)
    def lockMouse(self):
        global lockMouse
        lockMouse = True
        pygame.event.set_grab(True)
    def setSens(self,sens):
        global camSens
        camSens = sens

class TPPlayer:
    def __init__(self,win,speed,charimg,w,h,x,y):
        self.win = win
        self.speed = speed
        self.charimg = pygame.image.load(charimg)
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.charimg = pygame.transform.scale(self.charimg,(self.w,self.h))
    def work(self):
        self.win.screen.blit(self.charimg,(self.win.w/2-self.w/2-self.x,self.win.h-self.y))
        
        global playerZ,playerX
        global playerSpeed
        global camRot,camVel,camSens
        global lockMouse,mouseSpeed,mouseRightDown
        
        playerSpeed = self.speed
        playerZ += playerVel[2]
        playerX += playerVel[0]

        camRot[0] += camVel[0]
        camRot[1] += camVel[1]
        camRot[2] += camVel[2]

        if camRot[0] < -360:
            camRot[0] = 360
        if camRot[0] > 360:
            camRot[0] = -360

        if mouseSpeed < 1:
            mouseSpeed = 0

        if mouseRightDown:
            mx,my = pygame.mouse.get_pos()
            if mx < 400:
                camVel[0] = int(mouseSpeed/2-1)
            if mx > 400:
                camVel[0] = -int(mouseSpeed/2-1)

        if lockMouse == True:
            pygame.mouse.set_pos(self.win.w/2,self.win.h/2)
            pygame.event.set_grab(True)
    def lockMouse(self):
        global lockMouse
        lockMouse = True
        pygame.event.set_grab(True)
    def unlockMouse(self):
        global lockMouse
        lockMouse = False
        pygame.event.set_grab(False)
    def setSens(self,sens):
        global camSens
        camSens = sens

class Text:
    def __init__(self,win,x,y,text="Sample Text",size=30,font="Comic Sans MS",color=(255,255,255)):
        self.text = text
        self.size = size
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.win = win
        self.enabled = True
    def draw(self):
        if self.enabled:
            font = pygame.font.SysFont(self.font,self.size)
            text = font.render(self.text,False,self.color)
            self.win.screen.blit(text,(self.x,self.y))
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False

class Button:
    def __init__(self,win,x=100,y=100,fg=(255,255,255),bg=(40,40,40),text="Button",w=150,h=75,size=30,font="Comic Sans MS"):
        self.win = win
        self.x = x
        self.y = y
        self.fg = fg
        self.bg = bg
        self.text = text
        self.size = size
        self.w = w
        self.h = h
        self.font = font
        self.enabled = True
    def draw(self):
        if self.enabled:
            pygame.draw.rect(self.win.screen,self.bg,(self.x,self.y,self.w,self.h))
            font = pygame.font.SysFont(self.font,self.size)
            text = font.render(self.text,False,self.fg)
            self.win.screen.blit(text,(self.x,self.y))
    def onclick(self,function):
        global mouseLeftDown
        if self.enabled:
            if mouseLeftDown:
                mx,my = pygame.mouse.get_pos()
                if mx > self.x and mx < self.x + self.w and my > self.y and my < self.y + self.h:
                    function()
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False

class Frame:
    def __init__(self,win,x,y,w,h,color=(40,40,40)):
        self.win = win
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.enabled = True
    def draw(self):
        if self.enabled:
            pygame.draw.rect(self.win.screen,self.color,(self.x,self.y,self.w,self.h))
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False

class Crosshair:
    def __init__(self,win,img,w,h,followmouse=False,showmouse=False):
        self.win = win
        self.w = w
        self.h = h
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(self.w,self.h))
        self.fmouse = followmouse
        self.x = self.win.w/2-w/2
        self.y = self.win.h/2-h/2
        self.smouse = showmouse
        self.enabled = True
    def draw(self):
        if self.enabled:
            if self.smouse == False:
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            if self.fmouse == True:
                mx,my = pygame.mouse.get_pos()
                self.x = mx - self.w/2
                self.y = my - self.h/2
            else:
                self.x = self.win.w/2-self.w/2
                self.y = self.win.h/2-self.h/2
            self.win.screen.blit(self.img,(self.x,self.y))
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False

class Image:
    def __init__(self,win,img,x,y,w,h):
        self.win = win
        self.img = img
        self.w = w
        self.h = h
        self.img = pygame.image.load(self.img)
        self.img = pygame.transform.scale(self.img,(self.w,self.h))
        self.x = x
        self.y = y
        self.enabled = True
    def draw(self):
        if self.enabled:
            self.win.screen.blit(self.img,(self.x,self.y))
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False

class KeyboardListener:
    def __init__(self,key):
        self.key = key
        self.enabled = True
    def listen(self):
        if self.enabled:
            if keyboard.is_pressed(self.key):
                return True
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False
