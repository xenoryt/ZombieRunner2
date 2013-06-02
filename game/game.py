import pygame
import state
from state import State
import gui
import copy

## This is a singleton class ##
class Game(object):
	def __init__(this, screensize = (800,600), caption = "ZombieRunner 2: Survival of Tears"):
		this.running = False
		this._paused = False
		this._state = None
		this._prevState = None
		this.screensize = screensize
		this.fullscreen = False
		this.stateChange = False
		
		this.world = None
		
		# initialize pygame stuff
		pygame.init()
		this.screen = pygame.display.set_mode(screensize)
		pygame.display.set_caption(caption)
		
	### Public Fn  ###
	def run(this, state):
		""" 
		Starts the game.
		The mainloop is located here.
		"""
		if not this.stateChange:
			this.state = state
		
		this.running = True
		
		# create clock for timing
		clock = pygame.time.Clock()
		
		while this.running or this.state != None :
			# call state.update()
			# manage fps
			
			# Handle mouse events
			gui.Button.mouseup = False
			for event in pygame.event.get(pygame.locals.MOUSEBUTTONUP):
				if event.button == 1:
					gui.Button.mouseup = True
			
			if this.state != None:
				this.state.update()
				if this.stateChange:
					this.stateChange = False
					continue
					
				dirty = this.state.draw(this.screen)
				if type(dirty) == type([]):
					pygame.display.update(dirty)
				else:
					pygame.display.flip()
			else:
				this.Error("No state selected")
				
			
			#cap fps to 60
			clock.tick(30)
		
		# TODO: Handle cleanup here #
		#############################
	
	def assignState(this, state):
		if not this.stateChange:
			this.state = state
	
	def revertState(this):
		print "- Reverting state -"
		prevstate = copy.copy(this.state.prevState)
		del this._state
		this._state = prevstate
		this.stateChange = True
		
	
	
	def Pause(this):
		""" Pause the game """
		this.state = MessageboxState(this, "Paused: Press OK to unpause")
	
	def msgbox(this, text = "Message"):
		""" Renders a messagebox and pauses the game """
		this.state = state.MessageboxState(this, text)
		
	def Error(this, err, errtype=1):
		""" 
		Similar to messagebox but with specific message for 
		errors and exits game after displaying message
		"""
		print "Error %d: %s" % (errtype, err)
		this.msgbox( ("Error %d: %s" % (errtype, err)))
		this.Exit(False)
		
	
	def toggle_fullscreen(this):
		this.fullscreen = not this.fullscreen
		if this.fullscreen:
			pygame.display.set_mode(this.screensize, pygame.FULLSCREEN)
		else:
			pygame.display.set_mode(this.screensize)
	
	def Exit(this, now = True):
		this.running = False
		this._state.prevState = None
		this.stateChange = True
		if now:
			this._state = None
		
		if this.world.loaded:
			this.world.save()
	
	### Properties ###
	@property
	def state(this):
		return this._state
	@state.setter
	def state(this, state):
		if this._state != None:
			this._state.isCurrent = False
		
		state.prevState = this._state
		this._state = state
		this._state.isCurrent = True
		this.stateChange = True
	
	##################
	
	
# Declares a singleton
# Warning: Do not ever create another object of Game ever again
game = Game() 
