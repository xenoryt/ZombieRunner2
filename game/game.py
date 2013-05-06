import pygame
from pygame.locals import *
from state import State

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
			
			if this.state != None:
				this.state.update()
				this.state.draw(this.screen)
			else:
				this.Error("No state selected")
			
			#cap fps to 60
			clock.tick(60)

	
	def msgbox(this, text = "Message"): #TODO: render a messagebox - high priority
		""" Renders a messagebox and pauses the game """
		this.state = msgboxState()
		#raise NotImplementedError
		# possibly create a specific messagebox state?
		
	
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
	def isPaused(this): #TODO safely access global variable (for threading)
		return _paused
	@isPaused.setter
	def isPaused(this, p):
		_Pause(p) # call a Pause state maybe?
	
	@property
	def state(this):
		return this._state
	@state.setter
	def state(this, state):
		if this._state != None:
			this._state.isCurrent = False
		
		this._prevState = this._state
		this._state = state
		this._state.isCurrent = True
	
	##################
	
	### Private Fn ###
	def _Pause(this, pause):
		""" Pause the game """
		raise NotImplementedError
		
		# code under construction #
		#~ if pause:
			#~ 
		#~ else:
			
		_paused = not pause
	
	def _Update(this):
		"""
		A thread that calls the update function in the current state.
		Also manages fps
		"""
		while this.running:
			
			# pause the state if Game.isPaused
			while this.isPaused:
				pygame.time.wait(10) 
			
			_state.update()
		
	
	

# Declares a singleton
# Do not ever create another object of Game ever again
game = Game() 
