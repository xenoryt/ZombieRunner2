import pygame
from pygame.locals import *

class Control(pygame.sprite.Sprite, object):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this, this.containers)
		this.rect = pygame.Rect(0,0,0,0)
		this.image = None
		
		this.bgColor = Color((255,255,0))
		this.fgColor = Color('white')
		
	def move(this,x,y):
		this.rect = this.image.get_rect(topleft=(x,y)) #rect.move() doesnt seem to work?
	
	def moveip(this,x,y):
		this.rect.move_ip((x,y))
	
	def resize(this,w,h):
		this.image = pygame.Surface((w,h))
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=this.rect.topleft)
		


class Container(Control):
	def __init__(this, locx = 0, locy = 0, sizex = 2, sizey = 2):
		pygame.sprite.Sprite.__init__(this, this.containers)
		
		#initialize the background image
		this.image = pygame.Surface(sizex, sizey)
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this._font = pygame.font.Font(f, size)
		
		this.ctrls = []
	
	def add (ctrl):
		this.ctrls.append(ctrl)
		#this.rect = #some algorithm

class Button(Control):
	def __init__(this, text=""):
		pygame.sprite.Sprite.__init__(this, this.containers)
		
		#set default colors
		this.bgColor = Color('white')
		this.fgColor = Color('black')
		
		#initialize the background image
		this.image = pygame.Surface((sizex, sizey))
		this.image.fill(this.bgColor)
		
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this._font = pygame.font.Font(None, 22)
		this._text = text
		this.updatedText = False
		
	
	def font(this, f, size):
		this._font = pygame.font.Font(f, size)
	
	@property
	def text(this):
		return this._text
	
	@text.setter
	def text(this, msg):
		this._text = msg
		this.updatedText = False
	
	def update(this):
		if not this.updatedText:
			img = this._font.render(this.text, True, this.fgColor)
			this.image.blit(img, (this.rect.w/2-img.get_rect().w/2,this.rect.h/2-img.get_rect().h/2))
			this.updatedText = True

	def draw(this,surface):
		this.image.blit(surface, this.rect)

class gui(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		this.font = pygame.font.Font(None, 20)
	
	#def 
