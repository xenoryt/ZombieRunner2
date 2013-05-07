import gui
import game

class State():
	"""
	This class is a base class.
	Game states are derived from this class.
	Everything a game state does will be contained
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

class MessageboxState(State):
	def __init__(this, text):
		this.text = text
		
		this.box = gui.Container()
		this.box.rect.center = (game.screensize[0]/2, game.screensize[1]/2)
		this.box.add(button)
		this.button = gui.Button("OK")
		
		# Create label for messagebox and put it into this.box
	
	def update(this):
		this.box.update()
		return None
	
	def draw(this, screen):
		this.box.draw(screen)
		pass
	
