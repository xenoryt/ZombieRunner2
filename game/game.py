import pygame
from pygame.locals import *


## This is a singleton class ##
class Game(object):
	running = False
	_paused = False
	_state = None
	_prevState = None
	
	def __init__(this):
		# Shouldnt need to be inited... #
		raise NotImplementedError
	
	
	
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
		
		this.state = state
		
		# create clock for timing
		clock = pygame.time.Clock()
		
		while this.running:
			# call state.update()
			# manage fps
			
			if this.state != None:
				this.state.update()
				this.state.draw()
			else:
				this.Error("No state selected")
			
			# possibly handle AI here as well?
			
			#cap fps to 60
			clock.tick(60)

	
	def msgbox(this, text): #TODO: render a messagebox - high priority
		""" Renders a messagebox and pauses the game """
		raise NotImplementedError
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
		return _state
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
		
	
	###  Classes  ###
	class State():
		"""
		This class is a base class
		Game states are derived from this class
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
			# This should not handle FPS
			
			raise NotImplementedError
		
