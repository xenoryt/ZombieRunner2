import pygame
import state
from state import State
import gui

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
		#~ if this.running:
			#~ print "Game is already running"
		#~ else:
			#~ #start game
			#~ raise NotImplementedError
		
		
		this.state = state(this)
		this.running = True
		
		# create clock for timing
		clock = pygame.time.Clock()
		
		while this.running:
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
					
				this.state.draw(this.screen)
				pygame.display.flip()
			else:
				this.Error("No state selected")
			
			#cap fps to 60
			clock.tick(30)
		
		# TODO: Handle cleanup here #
		#############################
	
	def assignState(this, state):
		this.state = state
		this.stateChange = True
	
	def revertState(this):
		print "- Reverting state -"
		this._state = this.state.prevState
		this.stateChange = True
	
	
	def Pause(this):
		""" Pause the game """
		this.state = MessageboxState(this, "Paused: Press OK to unpause")
		this.stateChange = True
	
	def msgbox(this, text = "Message"):
		""" Renders a messagebox and pauses the game """
		this.state = state.MessageboxState(this, text)
		this.stateChange = True
		
	def Error(this, err, errtype=1):
		""" 
		Similar to messagebox but with specific message for 
		errors and exits game after displaying message
		"""
		print "Error %d: %s" % (errtype, err)
		this.msgbox(this, "Error %d: %s" % (errtype, err))
		this.stateChange = True
		this.Exit()
	
	def toggle_fullscreen(this):
		this.fullscreen = not this.fullscreen
		if this.fullscreen:
			pygame.display.set_mode(this.screensize, pygame.FULLSCREEN)
		else:
			pygame.display.set_mode(this.screensize)
	
	def Exit(this):
		this.running = False
	
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
	
	##################
	
	
# Declares a singleton
# Warning: Do not ever create another object of Game ever again
game = Game() 
