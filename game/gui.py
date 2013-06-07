import pygame
from pygame.locals import *
import os # for loading fonts

class Control(pygame.sprite.Sprite, object):
	"""
	This is the base class for all the GUI controls.
	"""
	
	layer = 5
	controls = []
	def __init__(this):
		pygame.sprite.Sprite.__init__(this)
		#~ super(type(this), this).__init__()
		this.rect = pygame.Rect(0,0,0,0)
		this.image = None
		
		this.static = False
		
		this._bgColor = Color('black')
		this._fgColor = Color('white')
		
		this.requireUpdate = True
		
		this.visible = True
	
	@property
	def bgColor(this):
		return this._bgColor
	
	@bgColor.setter
	def bgColor(this, color):
		this._bgColor = color
		this.requireUpdate = True
	
	@property
	def fgColor(this):
		return this._fgColor
	
	@fgColor.setter
	def fgColor(this, color):
		this._fgColor = color
		this.requireUpdate = True
	

class Container(Control):
	"""
	The Container class is a control that stores other controls.
	The stored controls will be updated/drawn when this
	control is updated/drawn. This class also organises the 
	child controls and places them depending on which 
	row and column they are on.
	"""
	
	def __init__(this, locx = 0, locy = 0):
		super(Container, this).__init__()
		
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
		if not this.visible:
			return 
		if len(this.ctrls) == 0:
			return 
		
		screen.blit(this.image, this.rect)
		
		for ctrl in this.ctrls:
			ctrl.draw(screen)
	
	def font(this, size, f="pix.ttf"):
		this._font = pygame.font.Font(os.path.join("data/font",f), size)
		this.requireUpdate = True
		
		for ctrl in this.ctrls:
			ctrl.font(size,f)
	
	# Functions that alter the container's geometry
	def center(this, loc):
		this.rect.center = loc
		this.organize()
	
	def resize(this, w,h):
		#initialize the background image
		
		this.image = pygame.Surface((w, h), pygame.SRCALPHA)
		if this.bgColor == None:
			this.image.set_alpha(0)
		else:
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
	
	def empty(this):
		del this.ctrls[:]
		this.cols = 0
		this.rows = 0
	
	def organize(this):
		"""
		This function refreshes the container and all its children.
		It also reorganizes all the children so they are in their 
		proper positions
		"""
		
		# Calculate the height of each row and overall height
		height = 0
		starth = [0 for i in range(this.rows)]
		for i in range(this.rows):
			for ctrl in this.ctrls:
				# If the control is in the this row
				if ctrl.row-1 == i:
					if ctrl.rect.h > this.rowh[i]:
						this.rowh[i] = ctrl.rect.h
			
			height += this.rowh[i]
			starth[i] = height - this.rowh[i]/2
		
		# Calculate the width of each column and overall width
		width = 0
		startw = [0 for i in range(this.cols)]
		for i in range(this.cols):
			for ctrl in this.ctrls:
				if ctrl.col-1 == i:
					if ctrl.rect.w > this.colw[i]:
						this.colw[i] = ctrl.rect.w
			
			width += this.colw[i]
			startw[i] = width - this.colw[i]/2
		
		# Resize according to overall width and height
		this.resize(width, height)
		
		#TODO: Possibly do some checking to remove unused rows and columns
		
		
		# Position the controls
		for ctrl in this.ctrls:
			#~ locx = this.rect.left + (startw[ctrl.col-1]) + ctrl.rect.w/2
			#~ locy = this.rect.top + (starth[ctrl.row-1]) + ctrl.rect.h/2
			locx = this.rect.left + (startw[ctrl.col-1])
			locy = this.rect.top + (starth[ctrl.row-1]) 

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
		super(_Label, this).__init__()
		
		this._font = pygame.font.Font(os.path.join("data/font","pix.ttf"), 15)
		this._text = text
		
		# initialize the background image
		# set the size to the required size of the text
		
		this.image = pygame.Surface(this._font.size(text))
		this.image.fill(this.bgColor)
		
		this.rect = this.image.get_rect(topleft=(locx,locy))
		
		this.requireUpdate = True # False means text is up to date
		this.layer = 6
	
	def font(this, size, f="pix.ttf"):
		this._font = pygame.font.Font(os.path.join("data/font",f), size)
		this.requireUpdate = True
	
	def resize(this, w = -1,h = -1):
		# Set width and height if none given
		w,h = this._font.size(this.text)
		
		# Create background image
		this.image = pygame.Surface((w, h))
		#~ this.image = this.image.convert_alpha()
		if this.bgColor != None:
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
			this.image = pygame.Surface(textpos.size,pygame.SRCALPHA)
			if this.bgColor == None:
				this.image.set_alpha(0)
			else:
				this.image.fill(this.bgColor)
			this.image.blit(text,(0,0))
			this.image.blit(text, textpos)
			this.requireUpdate = False
	
	def draw(this,surface):
		if this.visible:
			surface.blit(this.image, this.rect)

class Label(Container):
	"""
	The real Label class.
	Can create multiple lines of text by combining the 
	Container class and the _Label class.
	"""
	def __init__(this, text, locx=0, locy=0):
		super(Label, this).__init__(locx, locy)
		this._text = ""
		this.text = text
		
	
	@property
	def bgColor(this):
		return this._bgColor
	
	@bgColor.setter
	def bgColor(this, color):
		this._bgColor = color
		for lbl in this.ctrls:
			lbl.bgColor = color
	
	@property
	def text(this):
		return this._text
	
	@text.setter
	def text(this, text):
		if this._text == text:
			return
		
		this.empty()
		this._text = text
		this.lines = text.split('\n')
		
		# Create _labels for each line of text and place 
		# them into the container class
		for i in range(len(this.lines)):
			lbl = _Label(this.lines[i])
			this.add(lbl, i+1, 1)
		


class Button(Control):
	"""
	The Button class is the only class that handles mouse clicks.
	What the button does when clicked can be set by assigning
	the onClick method to another delegate. 
	The Button class can also be used as a picturebox
	"""
	
	mouseup = False
	images = []
	def __init__(this, text="", locx = 0, locy = 0, width=0,height=0):

		super(Button, this).__init__()
		
		this._font = pygame.font.Font(os.path.join("data/font","pix.ttf"), 15)
		this._text = text
		
		# This is for mouse over text (if set)
		this.label = None
		
		# initialize the background image
		# set the size to the required size of the text
		
		this.static = True
		
		# which state the button is in
		# e.g. normal, hover, click
		this.state = 0
		
		this.image = this.images[this.state]
		this.resize(this.image.get_size())
		
		this.requireUpdate = True # False means text is up to date
		this.layer = 6
		
	
	def font(this, size, f="pix.ttf"):
		this._font = pygame.font.Font(os.path.join("data/font",f), size)
		this.requireUpdate = True
	
	def resize(this, size = (-1,-1)):
		# Set width and height if none given
		if not this.static:
			size = this._font.size(this.text)
			size[0]+=4
			size[1]+=4
		elif size[0] == -1 or size[1] == -1:
			size = this.rect.size
		
		# Create background image
		this.image = pygame.transform.scale(this.images[this.state], size)
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
		if msg == this._text:
			return
		
		this._text = msg
		this.requireUpdate = True
	
	def update(this):
		# Update the button image/size if necessary
		if this.requireUpdate:
			this.resize()
			text = this._font.render(this.text, True, this.fgColor)
			textpos = text.get_rect()
			textpos.centerx = this.rect.size[0]/2
			textpos.centery = this.rect.size[1]/2
			
			this.image.blit(text, textpos)
			this.requireUpdate = False
		
		if this.visible:
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
				return this.onClick(this)

	def draw(this,surface):
		if this.visible:
			surface.blit(this.image, this.rect)
		
	def onClick(this, sender):
		return 0

class Bar(Control):
	"""
	The Bar class is a progress bar and fills up 
	according to the value and maxvalue given
	"""
	
	images = None
	
	def __init__(this, size = (100,20), value = 0):
		super (Bar, this).__init__()
		this.resize(size)
		this._maxvalue = 100
		this._value = value
		
		
		this._font = pygame.font.Font(os.path.join("data/font","pix.ttf"), 12)
		this._text = ""
		
		this.requireUpdate = True
	
	@property
	def text(this):
		return this._text
	
	@text.setter
	def text(this, txt):
		if txt == this._text:
			return
		this._text = txt
		text = this._font.render(this._text+": "+str(this.value), True, this.bgColor)
		textpos = text.get_rect()
		textpos.centerx = this.rect.size[0]/2
		textpos.centery = this.rect.size[1]/2
		
		this.image.blit(text, textpos)
	
	@property
	def value(this):
		return this._value
	
	@value.setter
	def value(this, val):
		if val == this._value:
			return
		
		this.image = this.images.copy()
		
		# Padding used in the background image
		pad = 2
		barw = int(round((this.rect.size[0]-pad*2)* float(val)/this.maxvalue))
		bar = pygame.Rect(pad,pad, barw, this.rect.h-pad*2)
		
		this.image.fill(this.fgColor,bar)
		
		this._value = val
		
		text = this._font.render(this.text+": "+str(this.value), True, this.bgColor)
		textpos = text.get_rect()
		textpos.centerx = this.rect.size[0]/2
		textpos.centery = this.rect.size[1]/2
		
		this.image.blit(text, textpos)
		
	@property
	def maxvalue(this):
		return this._maxvalue
	
	@maxvalue.setter
	def maxvalue(this, val):
		if val == this._maxvalue:
			return
		
		this._maxvalue = val
		
		this.image = this.images.copy()
		
		# Padding used in the background image
		pad = 2
		barw = int(round((this.rect.size[0]-pad*2)* float(val)/this.maxvalue))
		bar = pygame.Rect(pad,pad, barw, this.rect.h-pad*2)
		
		this.image.fill(this.fgColor,bar)
		
		this._value = val
		
		text = this._font.render(this.text+": "+str(this.value), True, this.bgColor)
		textpos = text.get_rect()
		textpos.centerx = this.rect.size[0]/2
		textpos.centery = this.rect.size[1]/2
		
		this.image.blit(text, textpos)
	
	def resize(this, size):
		if this.rect.size != size:
			this.image = pygame.transform.scale(this.images, size)
			this.rect = this.image.get_rect(topleft = this.rect.topleft)
	
	def update(this):
		pass
		
	
	def draw(this, screen):
		if this.visible:
			screen.blit(this.image, this.rect)

