import pygame
from pygame.locals import *

class Control(pygame.sprite.Sprite, object):
	this.layer = 5
	def __init__(this):
		pygame.sprite.Sprite.__init__(this, this.containers)
		this.rect = pygame.Rect(0,0,0,0)
		this.image = None
		
		this.bgColor = Color((255,255,0))
		this.fgColor = Color('white')
	
		


class Container(Control):
	def __init__(this, locx = 0, locy = 0, sizex = 2, sizey = 2):
		pygame.sprite.Sprite.__init__(this, this.containers)
		
		this.bgColor = Color("red")
		
		#initialize the background image
		this.image = pygame.Surface(sizex, sizey)
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		# Number of rows and columns
		this.rows = 1
		this.cols = 1
		
		
		this.ctrls = []
		
		this.layer = 5
	
	
	# Functions that are called by the game
	def update(this):
		"""
		Updates the container and all of its children
		"""
		for ctrl in this.ctrls:
			ctrl.update()
			ctrlwidth = ctrl.rect.width
			ctrlheight = ctrl.rect.height
			# Check if the child has exceeded size limits
			if ctrlwidth > this.cellw or ctrlheight > this.cellh:
				# If it has, resize this container
				newWidth = ctrlwidth*this.cols if ctrlwidth > cellw else this.rect.width
				newHeight = ctrlheight*this.rows if ctrlheight > cellh else this.rect.height
				this.resize(newWidth, newHeight)
		
		this.organize()
	
	def draw(this, screen):
		"""
		Draws teh container and all of its children
		"""
		this.image.blit(screen, this.rect)
		
		for ctrl in this.ctrls:
			ctrl.draw(screen):
	
	# Functions that alter the container's geometry
	def center(this, loc):
		this.rect.center = loc
	
	def resize(this, w,h):
		#initialize the background image
		this.image = pygame.Surface((w, h))
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(center=this.rect.center)
	
	# Functions that manage controls and their positions
	def add (this,ctrl, row, col):
		ctrl.row = row
		ctrl.col = col
		this.ctrls.append(ctrl)
		#this.rect = #some algorithm
	
	def organize(this):
		"""
		This function refreshes the container and all its children.
		It also reorganizes all the children so they are in their 
		proper positions
		"""
		
		# Position the controls
		for ctrl in this.ctrls:
			locx = this.rect.left + (ctrl.col * this.cellw) - this.cellw/2
			locy = this.rect.top + (ctrl.row * this.cellh) - this.cellh/2
			ctrl.rect.center = (locx, locy)
	
	
	
	# Properties
	@property
	def rows(this):
		return this._rows
	
	@rows.setter
	def rows(this, rows):
		this._rows = rows
		this.cellh = int(this.rect.h/this.rows)
		# TODO: Do something to organize controls #
		
	@property
	def cols(this):
		return this._cols
	
	@cols.setter
	def cols(this, cols):
		this._cols = cols
		this.cellw = int(this.rect.w/this.cols)
		# TODO: Do something to organize controls #
	
	
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
		this.requireUpdate = False # True means text is up to date
		
		this.layer = 6
	
	def font(this, f, size):
		this._font = pygame.font.Font(f, size)
	
	def resize(this, w,h):
		#initialize the background image
		this.image = pygame.Surface((w, h))
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=this.rect.topleft)
	
	@property
	def text(this):
		return this._text
	
	@text.setter
	def text(this, msg):
		this._text = msg
		this.requireUpdate = True
	
	def update(this):
		if this.requireUpdate:
			img = this._font.render(this.text, True, this.fgColor)
			this.image.blit(img, (this.rect.w/2-img.get_rect().w/2,this.rect.h/2-img.get_rect().h/2))
			this.requireUpdate = False

	def draw(this,surface):
		this.image.blit(surface, this.rect)
		
	def onClick(this):
		return 0

class gui(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		this.font = pygame.font.Font(None, 20)
	
	#def 
