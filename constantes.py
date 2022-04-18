# -*- coding: utf-8 -*-
#############################
#########constantes##########
#############################

from os import popen, name
from sys import path
from math import pi
from pygame.locals import *
from enumerations import *
try:
	from ctypes import windll
except ImportError:
	print("Importation non possible de windll.")

def getSystemResolutionOnLin():
	screen = popen("xrandr -q -d :0").readlines()[0]
	tmp = screen.split()
	return int( tmp[7] ), int( tmp[9][:-1] )

def getSystemResolutionOnWin():
        return windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

if name == "nt" :
        WIN_WIDTH, WIN_HEIGH = getSystemResolutionOnWin()
elif name == "posix" :
        WIN_WIDTH, WIN_HEIGH = getSystemResolutionOnLin()
else:
        WIN_WIDTH = 500
        WIN_HEIGH = 380
        
WIN_WIDTH = WIN_WIDTH * 8 // 10
WIN_HEIGH = WIN_HEIGH * 8 // 10

TITRE = "Game of life"
SCRIPT_PATH=path[0]

FPS = 10

TOPOLOGY = TORUS

#L = 80
#C = 100
#L = 4
#C = 4
#L = 40
#C = 50
L = 80
C = 100

BLOC_W = WIN_WIDTH // C
BLOC_H = WIN_HEIGH // L

STEP = ( BLOC_W + BLOC_H ) // 2

#Mouse Button, Scroll Wheel
MB_LEFT, MB_MIDDLE, MB_RIGHT, MBSW_UP, MBSW_DOWN = 1, 2, 3, 4, 5

#              R    G    B
WHITE      = (250, 250, 250)
BLACK      = ( 10,  10,  10)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (155,   0,   0)
YELLOW     = (255, 255,   0)
CYAN       = (208, 251, 249)
