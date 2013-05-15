import pygame
from pygame.locals import *
import os # for loading fonts

class Control(pygame.sprite.Sprite, object):
	layer = 5
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		this.rect = pygame.Rect(0,0,0,0)
		this.image = None
		
		this.bgColor = Color((255,255,0))
		this.fgColor = Color('white')
	

class Container(Control):
	def __init__(this, locx = 0, locy = 0):
		pygame.sprite.Sprite.__init__(this)
		
		this.bgColor = Color("#646464")
		
		#initialize the background image
		this.image = pygame.Surface((5,5))
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		# Number of rows and columns
		this.rows = 1
		this.cols = 1
		
		this.rowh = [0]
		this.colw = [0]
		
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
		
		this.organize()
	
	def draw(this, screen):
		"""
		Draws teh container and all of its children
		"""
		screen.blit(this.image, this.rect)
		
		for ctrl in this.ctrls:
			ctrl.draw(screen)
	
	# Functions that alter the container's geometry
	def center(this, loc):
		this.rect.center = loc
		this.organize()
	
	def resize(this, w,h):
		#initialize the background image
		this.image = pygame.Surface((w, h))
		this.image.fill(this.bgColor)
		this.rect = this.image.get_rect(center=this.rect.center)
	
	# Functions that manage controls and their positions
	def add (this,ctrl, row, col):
		if row > this.rows:
			this.rows = row
		if col > this.cols:
			this.cols = col
		
		ctrl.row = row
		ctrl.col = col
		
		this.ctrls.append(ctrl)
		this.organize()
		#this.rect = #some algorithm
	
	def organize(this):
		"""
		This function refreshes the container and all its children.
		It also reorganizes all the children so they are in their 
		proper positions
		"""
		
		# Calculate the height of each row and overall height
		height = 0
		for i in range(this.rows):
			for ctrl in this.ctrls:
				# If the control is in the this row
				if ctrl.row-1 == i:
					if ctrl.rect.h > this.rowh[i]:
						this.rowh[i] = ctrl.rect.h
		
			height += this.rowh[i]
		
		# Calculate the width of each column and overall width
		width = 0
		for i in range(this.cols):
			for ctrl in this.ctrls:
				if ctrl.col-1 == i:
					if ctrl.rect.w > this.colw[i]:
						this.colw[i] = ctrl.rect.w
			
			width += this.colw[i]
		
		# Resize according to overall width and height
		this.resize(width, height)
		
		#TODO: Possibly do some checking to remove unused rows and columns
		
		
		
		# Position the controls
		for ctrl in this.ctrls:
			locx = this.rect.left + (ctrl.col * this.colw[ctrl.col-1]) - this.colw[ctrl.col-1]/2
			locy = this.rect.top + (ctrl.row * this.rowh[ctrl.row-1]) - this.rowh[ctrl.row-1]/2
			ctrl.rect.center = (locx, locy)
	
	
	
	# Properties
	@property
	def rows(this):
		return this._rows
	
	@rows.setter
	def rows(this, rows):
		this._rows = rows
		this.rowh = [0 for i in range(this.rows)]
		# TODO: Do something to organize controls #
		
	@property
	def cols(this):
		return this._cols
	
	@cols.setter
	def cols(this, cols):
		this._cols = cols
		this.colw = [0 for i in range(this.cols)]
		# TODO: Do something to organize controls #




class _Label(Control):
	"""
	Creates a single line block of text. 
	This is only used by the actual Label class in order to create 
	multiline labels
	"""
	def __init__(this, text="", locx = 0, locy = 0):
		pygame.sprite.Sprite.__init__(this)
		
		#set default colors
		this.bgColor = Color('#646464')
		this.fgColor = Color('black')
		
		this._font = pygame.font.Font(os.path.join("data/font","pix.ttf"), 15)
		this._text = text
		
		
		# initialize the background image
		# set the size to the required size of the text
		
		this.image = pygame.Surface(this._font.size(text))
		this.image.fill(this.bgColor)
		
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this.requireUpdate = True # False means text is up to date
		this.layer = 6
	
	def font(this, f, size):
		this._font = pygame.font.Font(f, size)
		this.requireUpdate = True
	#TODO: Change resize function to button's?
	def resize(this, w = -1,h = -1):
		# Set width and height if none given
		w,h = this._font.size(this.text)
		
		# Create background image
		this.image = pygame.Surface((w, h))
		this.image = this.image.convert()
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
		# Update the button image/size if necessary
		if this.requireUpdate:
			this.resize()
			text = this._font.render(this.text, True, this.fgColor)
			textpos = text.get_rect()
			textpos.centerx = this.rect.centerx - this.rect.left
			textpos.centery = this.rect.centery - this.rect.top
			this.image.blit(text, textpos)
			this.requireUpdate = False
			print "label",this.text,this.rect.size,this.rect.center
	
	def draw(this,surface):
		#~ print "drawing button"
		surface.blit(this.image, this.rect)

class Label(Control):
	"""
	The real Label class.
	Can create multiple lines of text by combining the 
	Container class and the _Label class.
	"""
	def __init__(this, text, locx=0, locy=0):
		this.box = Container(locx, locy)
		this.text = text
		
		this.layer = 6
		
	@property
	def text(this):
		return this._text
	
	@text.setter
	def text(this, text):
		this._text = text
		this.lines = text.split('\n')
		
		# Create _labels for each line of text and place 
		# them into the container class
		for i in range(len(this.lines)):
			lbl = _Label(this.lines[i])
			this.box.add(lbl, i+1, 1)
	
	@property
	def rect(this):
		return this.box.rect
	
	def update(this):
		#~ print this.rect.topleft
		#~ for lbl in this.box.ctrls:
			#~ print "label",lbl.text,lbl.rect.topleft
		this.box.update()
	
	def draw(this, screen):
		this.box.draw(screen)
		


class Button(Control):
	mouseup = False
	images = []
	def __init__(this, text="", locx = 0, locy = 0):
		pygame.sprite.Sprite.__init__(this)
		
		#set default colors
		this.bgColor = Color('red')
		this.fgColor = Color('black')
		
		this._font = pygame.font.Font(os.path.join("data/font","pix.ttf"), 15)
		this._text = text
		
		# This is for mouse over text (if set)
		this.label = None
		
		# initialize the background image
		# set the size to the required size of the text
		
		this.image = pygame.transform.scale(this.images[0], this._font.size(text))
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this.requireUpdate = True # False means text is up to date
		this.layer = 6
	
	def font(this, f, size):
		this._font = pygame.font.Font(f, size)
		this.requireUpdate = True
	
	def resize(this, w = -1,h = -1):
		# Set width and height if none given
		w,h = this._font.size(this.text)
		
		# Create background image
		this.image = pygame.transform.scale(this.images[0], this._font.size(this.text))
		this.rect = this.image.get_rect(topleft=this.rect.topleft)
	
	def setMouseover(this, text = ""):
		"""
		Sets the text that appears when the mouse hovers over the button.
		When called with no arguments (or empty string), it removes the 
		mouseover text.
		"""
		
		
	
	@property
	def text(this):
		return this._text
	
	@text.setter
	def text(this, msg):
		this._text = msg
		this.requireUpdate = True
	
	def update(this):
		# Update the button image/size if necessary
		if this.requireUpdate:
			this.resize()
			text = this._font.render(this.text, True, this.fgColor)
			textpos = text.get_rect()
			textpos.centerx = this.rect.centerx - this.rect.left
			textpos.centery = this.rect.centery - this.rect.top
			this.image.blit(text, textpos)
			this.requireUpdate = False
			print "button",this.text,this.rect.size,this.rect.center
		
		# Check for mouse events
		mpos = pygame.mouse.get_pos()
		
		# If the mouse is NOT on the button, do nothing
		if mpos[0] < this.rect.left or mpos[0] > this.rect.right:
			return 0
		if mpos[1] < this.rect.top or mpos[1] > this.rect.bottom:
			return 0
		
		# Check if the left mouse button is being pressed
		if this.mouseup:
			print "button",this.text,"was clicked"
			return this.onClick()

	def draw(this,surface):
		#~ print "drawing button"
		surface.blit(this.image, this.rect)
		
	def onClick(this):
		return 0


	
class gui(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		this.font = pygame.font.Font(None, 20)
	
	#def 
