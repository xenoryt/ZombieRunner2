import pygame
from pygame.locals import *

class Control(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		
		this.rect = pygame.Rect(0,0,0,0)
		
		this.fgColor = Color('black')
		this.bgColor = Color('white')
		
		
	def color(fg, bg):
		this.bgColor = fg
		this.bgColor = bg
	
	
	
	## Properties ##
	
	
	
		


class Container(Control):
	def __init__(this, locx = 0, locy = 0, sizex = 2, sizey = 2):
		pygame.sprite.Sprite.__init__(this)
		
		#initialize the background image
		this.image = pygame.Surface(sizex, sizey)
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this._font = pygame.font.Font(f, size)
		
		this.ctrls = []
	
	def add (ctrl):
		this.ctrls.append(ctrl)
		#this.rect = #some algorithm

class Label(Control):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		

class Button(Control):
	def __init__(this, locx = 0, locy = 0, sizex = 2, sizey = 2):
		pygame.sprite.Sprite.__init__(this)
		
		#initialize the background image
		this.image = pygame.Surface((sizex, sizey))
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this._font = pygame.font.Font(None, 20)
		
	
	def font(this):
		return this._font
	
	def font(this, f, size):
		this._font = pygame.font.Font(f, size)
	
	def text(msg):
		this.image = this._font.render(msg, 0, self.color)

class gui(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		this.font = pygame.font.Font(None, 20)
	
	#def 
