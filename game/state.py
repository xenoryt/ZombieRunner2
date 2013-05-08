import gui
import game
import pygame
from pygame.locals import *

class State():
	"""
	This class is a base class.
	Game states are derived from this class.
	Everything a game.game state does will be contained
	in a class derived from this State class.
	"""
	isCurrent = False
	def update(this):
		# This is just a place holder #
		
		# The real update function should contain
		# - event checking and handling
		# - update objects related to the state
		# - some error checking to make sure the current
		#	state is active (you never know...)
		#
		# Note: This should only calls update functions of the 
		#		objects within this state. It does not manage FPS.
		
		raise NotImplementedError
		if not isCurrent:
			Game.Error("Updating an inactive state")
	
	
	def draw(this,screen):
		# This is just a place holder #
		
		# The real draw function should contain
		# - rendering images
		# - displaying onto screen
		# - other display related stuff
		# This should not handle FPS (that is handled auto-magically)
		
		raise NotImplementedError


## Some game states ##

def btnMsgboxClick():
	game.game.revertState()
	return 0

class MessageboxState(State):
	def __init__(this, text):
		print "Entered messagebox state"
		print text
		print ""
		this.text = text
		
		this.box = gui.Container()
		this.box.rect.center = (game.game.screensize[0]/2, game.game.screensize[1]/2)
		#~ this.box.rect.organize()
		
		this.button = gui.Button("OK")
		this.button.onClick = btnMsgboxClick
		this.label = gui.Label(text)
		this.box.add(this.label,1,1)
		this.box.add(this.button,2,1)
		
		# Create label for messagebox and put it into this.box
	
	def update(this):
		# Get input
		for event in pygame.event.get():
			if event.type == QUIT:
				game.game.running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					game.game.running = False
				elif event.key == K_2:
					game.game.revertState()
		this.box.update()
		return 0 # should return something to indicate action
	
	def draw(this, screen):
		this.box.draw(screen)
		
	

