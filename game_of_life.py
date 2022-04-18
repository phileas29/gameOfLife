#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

###################################
#                                 #
#      CONWAY'S GAME OF LIFE      #
#                                 #
#                                 #
#                                 #
#      langage : Python 2.7       #
#          API : Pygame           #
#         date : 27/07/17         #
#          version : 1.0          #
#     auteur : Philéas PERON      #
#                                 #
###################################

#Pour les matrices !
# i : n° ligne
# j : n° colonne
# A[i][j]
# point de coord (x,y) -> A[y][x]

#Pour les vecteurs !
# i : n° ligne
# transpose(u[i]) = U[i][0]

import pygame as pg
from pygame.locals import *
from pygame.draw import *
from math import *
from random import *
from constantes import *
from dictionnaires import *
from enumerations import *
from os import path, environ
import time

class Pos(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		
class Dim(object):
	def __init__(self, w=0, h=0):
		self.w = w
		self.h = h
		
class Time(object):
	def __init__(self):
		self.past = 0.
		self.pres = 0.
	def delay(self):
		return self.pres - self.past
	def update(self):
		self.pres = pg.time.get_ticks()
	def switch(self):
		self.past = self.pres

class World_Map(object):
	def __init__(self):
		#self.map1 = [ [ [ randint(0,1) * ( -k + 1 ) for j in range(C) ] for i in range(L) ] for k in range(2) ]
		self.map1 = [ [ [ [ DEAD for j in range(C) ] for i in range(L) ] for k in range(2) ] for t in range(TOPOLOGY//2+1-TOPOLOGY//4) ]
		
		#self.clown(Pos(C//4*3,L//2))
		#self.gosper_glider_gun(Pos(C//4-15,L//2-4))
		
		#self.rectangle(Pos(C//2-1,L//2-1),Dim(2,2))
		
		#torus
		#self.glider(Pos(C-5,2*L//3))
		self.gosper_glider_gun(Pos(C//2-15,1))
		#self.clown(Pos(C//2-1,L//2-2))
		
		#self.gosper_glider_gun(Pos(C//2-21,5))
		#self.gosper_glider_gun(Pos(C//2-20,L-11),VERSO)
		
		#self.glider(Pos(C-10,2*L//8-2),VERSO)
		#self.glider(Pos(C-10,4*L//8),VERSO)
		
		#moebius
		#self.LWSS(Pos(C-10,2*L//8-2),VERSO)
				
	def rectangle(self, pos, dim, side=RECTO):
		for i in range(dim.h) :
			for j in range(dim.w) :
				self.map1[side][PRES][pos.y+i][pos.x+j] = ALIVE
				
	def LWSS(self, pos, side=RECTO):
		self.rectangle( Pos(pos.x+1,pos.y+3) , Dim(3,1) , side )
		self.rectangle( Pos(pos.x+4,pos.y+1) , Dim(1,3) , side )
		self.map1[side][PRES][pos.y][pos.x] = ALIVE
		self.map1[side][PRES][pos.y+2][pos.x] = ALIVE
		self.map1[side][PRES][pos.y][pos.x+3] = ALIVE
				
	def glider(self, pos, side=RECTO):
		for i in range(2) :
			for j in range(2) :
				self.map1[side][PRES][pos.y+i][pos.x+j+i] = ALIVE
		self.map1[side][PRES][pos.y+2][pos.x] = ALIVE
				
	def reflection_symmetry(self, pos, dim, side=RECTO, axis=X):
		for i in range(1,dim.h) :
			for j in range(dim.w) :
				if self.map1[side][PRES][pos.y+i][pos.x+j] == ALIVE :
					self.map1[side][PRES][pos.y-i][pos.x+j] = ALIVE
				if self.map1[side][PRES][pos.y-i][pos.x+j] == ALIVE :
					self.map1[side][PRES][pos.y+i][pos.x+j] = ALIVE
		
	def clown(self, pos, side=RECTO):
		for i in range(3) :
			self.map1[side][PRES][pos.y+i][pos.x+1] = ALIVE
			self.map1[side][PRES][pos.y+i][pos.x+3] = ALIVE
		self.map1[side][PRES][pos.y][pos.x+2] = ALIVE
				
	def gosper_glider_gun(self, pos, side=RECTO):
		self.rectangle( Pos(pos.x,pos.y+4) , Dim(2,2) , side )
		self.rectangle( Pos(pos.x+34,pos.y+2) , Dim(2,2) , side )
		#(10,2)
		self.map1[side][PRES][pos.y+2][pos.x+12] = ALIVE
		self.map1[side][PRES][pos.y+2][pos.x+13] = ALIVE
		self.map1[side][PRES][pos.y+3][pos.x+11] = ALIVE
		self.map1[side][PRES][pos.y+4][pos.x+10] = ALIVE
		self.map1[side][PRES][pos.y+5][pos.x+10] = ALIVE
		#(15,3)
		self.map1[side][PRES][pos.y+5][pos.x+14] = ALIVE
		self.map1[side][PRES][pos.y+3][pos.x+15] = ALIVE
		self.map1[side][PRES][pos.y+4][pos.x+16] = ALIVE
		self.map1[side][PRES][pos.y+5][pos.x+17] = ALIVE
		self.map1[side][PRES][pos.y+5][pos.x+16] = ALIVE
		self.reflection_symmetry(Pos(pos.x+10,pos.y+5), Dim(10,6),side)
		#(20,0)
		self.rectangle( Pos(pos.x+20,pos.y+2) , Dim(2,2) , side )
		self.map1[side][PRES][pos.y+1][pos.x+22] = ALIVE
		self.rectangle( Pos(pos.x+24,pos.y) , Dim(1,2) , side )
		self.reflection_symmetry(Pos(pos.x+20,pos.y+3), Dim(5,5) , side )
		
	def evolution(self):
		nb = 0
		for k in range(TOPOLOGY//2+1-TOPOLOGY//4):
			for i in range(L) :
				for j in range(C) :
					nb = self.count_neighbours( Pos(j,i), k )
					if self.map1[k][PAST][i][j] == ALIVE :
						if nb == 2 or nb == 3 :
							self.map1[k][PRES][i][j] = ALIVE
					elif nb == 3 :
							self.map1[k][PRES][i][j] = ALIVE
					
	def count_neighbours(self, pos, side):
		nb = 0
		if TOPOLOGY == PLAIN :#?
			for i in range(-1,2) :
				for j in range(-1,2) :
					if pos.x + j < C and pos.y + i < L and 0 <= pos.x + j and 0 <= pos.y + i and ( i != j or j != 0 ) and self.map1[0][PAST][pos.y+i][pos.x+j] == ALIVE :
						nb += 1
		elif TOPOLOGY == TORUS :
			for i in range(-1,2) :
				for j in range(-1,2) :
					if ( i != j or j != 0 ) and self.map1[0][PAST][ ( pos.y + i ) % L ][ ( pos.x + j ) % C ] == ALIVE :
						nb += 1
		elif TOPOLOGY == UNKNOW :
			for i in range(-1,2) :
				for j in range(-1,2) :
					if i != j or j != 0 :
						u = pos.x + j
						v = pos.y + i
						if 0 <= u and u <= C-1 and 0 <= v and v <= L-1 :
							if self.map1[side][PAST][v][u] == ALIVE :
								nb += 1
						elif ( u == -1 and v == -1 ) or ( u == -1 and v == L ) or ( u == C and v == -1 ) or ( u == C and v == L ) :
							if u == -1 and v == -1 :
								if self.map1[(side+1)%2][PAST][L-1][C-1] == ALIVE :
									nb += 1
							elif u == -1 and v == L :
								if self.map1[(side+1)%2][PAST][0][C-1] == ALIVE :
									nb += 1
							elif u == C and v == -1 :
								if self.map1[(side+1)%2][PAST][L-1][0] == ALIVE :
									nb += 1
							elif u == C and v == L :
								if self.map1[(side+1)%2][PAST][0][0] == ALIVE :
									nb += 1
						else:
							if u < 0 :
								if self.map1[(side+1)%2][PAST][L-1-v][C-1] == ALIVE :
									nb += 1
							elif C <= u :
								if self.map1[(side+1)%2][PAST][L-1-v][0] == ALIVE :
									nb += 1
							elif v < 0 :
								if self.map1[(side+1)%2][PAST][L-1][C-1-u] == ALIVE :
									nb += 1
							elif L <= v :
								if self.map1[(side+1)%2][PAST][0][C-1-u] == ALIVE :
									nb += 1
		elif TOPOLOGY == KLEIN_BOTTLE :#klein
			for i in range(-1,2) :
				for j in range(-1,2) :
					if i != j or j != 0 :
						u = pos.x + j
						v = pos.y + i
						if 0 <= u and u <= C-1 and 0 <= v and v <= L-1 :
							if self.map1[side][PAST][v][u] == ALIVE :
								nb += 1
						elif ( u == -1 and v == -1 ) or ( u == -1 and v == L ) or ( u == C and v == -1 ) or ( u == C and v == L ) :
							if u == -1 and v == -1 :
								if self.map1[(side+1)%2][PAST][L-1][C-1] == ALIVE :
									nb += 1
							elif u == -1 and v == L :
								if self.map1[(side+1)%2][PAST][0][C-1] == ALIVE :
									nb += 1
							elif u == C and v == -1 :
								if self.map1[(side+1)%2][PAST][L-1][0] == ALIVE :
									nb += 1
							elif u == C and v == L :
								if self.map1[(side+1)%2][PAST][0][0] == ALIVE :
									nb += 1
						else:
							if u < 0 :
								if self.map1[side][PAST][v][C-1] == ALIVE :
									nb += 1
							elif C <= u :
								if self.map1[side][PAST][v][0] == ALIVE :
									nb += 1
							elif v < 0 :
								if self.map1[(side+1)%2][PAST][L-1][C-1-u] == ALIVE :
									nb += 1
							elif L <= v :
								if self.map1[(side+1)%2][PAST][0][C-1-u] == ALIVE :
									nb += 1
		elif TOPOLOGY == MOEBIUS_BAND :
			for i in range(-1,2) :
				for j in range(-1,2) :
					if i != j or j != 0 :
						u = pos.x + j
						v = pos.y + i
						if 0 <= u and u <= C-1 and 0 <= v and v <= L-1 :
							if self.map1[side][PAST][v][u] == ALIVE :
								nb += 1
						elif ( u == -1 or u == C ) and v != -1 and v != L :
							if u == -1 :
								if self.map1[(side+1)%2][PAST][L-1-v][C-1] == ALIVE :
									nb += 1
							else :
								if self.map1[(side+1)%2][PAST][L-1-v][0] == ALIVE :
									nb += 1
							#if u == -1 :
								#if self.map1[(side+1)%2][PAST][L-1-v][0] == ALIVE :
									#nb += 1
							#else :
								#if self.map1[(side+1)%2][PAST][L-1-v][C-1] == ALIVE :
									#nb += 1
		return nb
					
	def copy_map(self):
		for k in range(TOPOLOGY//2+1-TOPOLOGY//4):
			for i in range(L) :
				for j in range(C) :
					self.map1[k][PAST][i][j] = self.map1[k][PRES][i][j]
					self.map1[k][PRES][i][j] = DEAD

class Game_Of_Life(object):
	def __init__(self):
		"""Init game"""
		self.worldMap = World_Map()
		self.zoom = 6e-1
		self.focus = Pos(BLOC_W * C // 2, BLOC_H * L // 2)
		self.pause = False
		self.time = Time()
		self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGH), pg.DOUBLEBUF | pg.HWSURFACE)
		self.bg = pg.Surface(self.screen.get_size())
		self.exitGame = False
		
		self.bloc = pg.Surface( (WIN_WIDTH // 2 , WIN_HEIGH // 2) )
		self.bloc.fill(WHITE)
		self.bloc.set_alpha(128)
		self.blocc = pg.Surface( (WIN_WIDTH // 2 , WIN_HEIGH // 2) )
		self.blocc.fill(BRIGHTBLUE)
		self.blocc.set_alpha(128)
		
	def main_loop(self):
		"""Main loop"""
		while not self.exitGame :
			self.time.update()
			self.event_loop()
			if self.pause == False and 1e3 / FPS < self.time.delay() :
				self.time.switch()
				self.update()
			self.draw()
			pg.display.flip()
	
	def event_loop(self):
		"""Récupération des événements utilisateur"""
		for event in pg.event.get():
			if event.type == pg.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				self.exitGame = True
			elif event.type == KEYDOWN and event.key == K_p:
				self.pause = ( self.pause + 1 ) % 2
			elif ( event.type == MOUSEBUTTONDOWN and event.button ) == MBSW_UP :
				self.zoom *= 1.41
			elif ( event.type == MOUSEBUTTONDOWN and event.button ) == MBSW_DOWN :
				self.zoom /= 1.41
			elif event.type == KEYDOWN and event.key == K_s:
				self.focus.x += STEP
			elif event.type == KEYDOWN and event.key == K_w:
				self.focus.y -= STEP
			elif event.type == KEYDOWN and event.key == K_q:
				self.focus.x -= STEP
			elif event.type == KEYDOWN and event.key == K_a:
				self.focus.y += STEP
	
	def update(self):
		"""Actualisation positions corps"""
		self.worldMap.copy_map()
		self.worldMap.evolution()

	def draw(self):
		"""Dessine l'interface."""
		self.bg.fill(BLACK)
		line( self.bg, BRIGHTBLUE, change_basis(Pos(0,0), self.focus, self.zoom), change_basis(Pos(0,BLOC_H * L - 1), self.focus, self.zoom) )
		line( self.bg, BRIGHTBLUE, change_basis(Pos(0,0), self.focus, self.zoom), change_basis(Pos(BLOC_W * C - 1,0), self.focus, self.zoom) )
		line( self.bg, BRIGHTBLUE, change_basis(Pos(BLOC_W * C - 1,BLOC_H * L - 1), self.focus, self.zoom), change_basis(Pos(0,BLOC_H * L - 1), self.focus, self.zoom) )
		line( self.bg, BRIGHTBLUE, change_basis(Pos(BLOC_W * C - 1,BLOC_H * L - 1), self.focus, self.zoom), change_basis(Pos(BLOC_W * C - 1,0), self.focus, self.zoom) )
		for k in range(TOPOLOGY//2+1-TOPOLOGY//4):
			for i in range(L) :
				for j in range(C) :
					if k == RECTO and self.worldMap.map1[RECTO][PRES][i][j] == ALIVE :
						self.bg.blit( self.bloc , change_basis(Pos(BLOC_W * j, BLOC_H * i), self.focus, self.zoom), (0,0,ceil(BLOC_W * self.zoom) , ceil(BLOC_H * self.zoom)) )
					elif k == VERSO and self.worldMap.map1[VERSO][PRES][i][j] == ALIVE :
						self.bg.blit( self.blocc , change_basis(Pos(BLOC_W * j, BLOC_H * i), self.focus, self.zoom), (0,0,ceil(BLOC_W * self.zoom) , ceil(BLOC_H * self.zoom)) )
		self.screen.blit(self.bg, (0, 0))

def change_basis(e, ref, zoom):#from map basis to window basis
	return ( int( ( e.x - ref.x ) * zoom ) + WIN_WIDTH // 2 , int( ( e.y - ref.y ) * zoom ) + WIN_HEIGH // 2 )

def sign(x):
	if x < 0 :
		return -1
	else:
		return 1

if __name__ == '__main__' :
	pg.init()
	environ['SDL_VIDEO_CENTERED'] = '1'
	pg.display.set_caption(TITRE)
	icon_32x32 = pg.image.load( path.join(SCRIPT_PATH, "logo.png") )
	pg.display.set_icon(icon_32x32)
	pg.key.set_repeat(500, 100)
	
	game_of_life = Game_Of_Life()
	game_of_life.main_loop()
	
	pg.quit()
