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
		
		
		this.state = state()
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
	
	def revertState(this):
		print "- Reverting state -"
		this._state = this.state.prevState
	
	
	def Pause(this):
		""" Pause the game """
		this.state = MessageboxState("Paused: Press OK to unpause")
	
	def msgbox(this, text = "Message"):
		""" Renders a messagebox and pauses the game """
		this.state = state.MessageboxState(text)
		
	def Error(this, err, errtype=1):
		""" 
		Similar to messagebox but with specific message for 
		errors and exits game after displaying message
		"""
		print "Error %d: %s" % (errtype, err)
		this.msgbox("Error %d: %s" % (errtype, err))
		# Application.Exit()
	
	
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
