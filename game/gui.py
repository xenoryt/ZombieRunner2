import pygame
from pygame.locals import *

class Control(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		
		this.rect = pygame.Rect(0,0,0,0)
		
		this.fgColor = Color('black')
		this.bgColor = Color('white')
		
		this._font = pygame.font.Font(None, 20)
		
	def font(f, size):
		this._font = pygame.font.Font(f, size)
	
	def pos(x,y):
		this.x = x
		this.y = y
	def dim(w,h):
		this.w = w
		this.h = h
		
	
class Container(Control):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this) #possible error?
		this.rect = pygame.Rect(0,0,0,0)
		this.bgColor = Color('black')
		
		this._font = pygame.font.Font(f, size)
		
		this.ctrls = []
	
	def add (ctrl):
		this.ctrls.append(ctrl)
		this.rect = #some algorithm


class gui(pygame.sprite.Sprite):
	
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		this.font = pygame.font.Font(None, 20)
	
	def 
