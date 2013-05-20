import gui
import game
import pygame
from pygame.locals import *
import world
import mapgenerator

from camera import Camera
from keys import Keys

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
	
	def draw(this, screen):
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))
		screen.blit(background, (0, 0))
		
		this.box.draw(screen)
		
def assignState(state):
	""" 
	This function is needed since you can't assign
	in a lambda
	"""
	game.state = state

class MainMenuState(State):
	def __init__(this):
		this.btnStart = gui.Button("Start")
		this.btnExit = gui.Button("Exit")
		
		this.btnStart.onClick = lambda: game.assignState(GameState())
		this.btnExit.onClick = lambda: game.revertState()
	
	def update(this):
		this.btnStart.update()
		this.btnExit.update()

class GameState(State):
	def __init__(this, level = 1):
		this.world = None
		this.level = level
		this.camera = Camera(game.game.screensize)
		this.keys = Keys()
		this.scrollamt = 6
		
		# TODO: Add checking for continues
		
		this.loadWorld("map")
		
	def newWorld(this):
		if this.world != None:
			this.world.savemap()
		this.loadWorld(mapgenerator.generate("map"+str(level)+".txt"))
	
	def loadWorld(this, mapname):
		if this.world != None:
			this.world.savemap()
		this.world = world.World()
		this.world.load(mapname)
		this.camera.rect.center = this.world.player.rect.center
		#TODO: LOAD WORLD ENTITIES HERE
	
	def update(this):
		
		# Get input 
		for event in pygame.event.get():
			if event.type == QUIT:
				game.game.running = False
				this.world.save()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					game.game.running = False
					this.world.save()
				elif event.key == K_UP:
					this.keys.up = True
				elif event.key == K_DOWN:
					this.keys.down = True
				elif event.key == K_LEFT:
					this.keys.left = True
				elif event.key == K_RIGHT:
					this.keys.right = True
				
				elif event.key == K_EQUALS:
					this.scrollamt += 2
				elif event.key == K_MINUS:
					this.scrollamt -= 2
				
			if event.type == KEYUP:
				if event.key == K_UP:
					this.keys.up = False
				elif event.key == K_DOWN:
					this.keys.down = False
				elif event.key == K_LEFT:
					this.keys.left = False
				elif event.key == K_RIGHT:
					this.keys.right = False
		
		
		#~ if this.keys.up:
			#~ this.camera.rect.y -= this.scrollamt
			#~ if this.camera.rect.top < 0:
				#~ this.camera.rect.top = 0;
		#~ if this.keys.down:
			#~ this.camera.rect.y += this.scrollamt
			#~ if this.camera.rect.bottom > this.world.mapsize[1]:
				#~ this.camera.rect.bottom = this.world.mapsize[1]
		#~ if this.keys.left:
			#~ this.camera.rect.x -= this.scrollamt
			#~ if this.camera.rect.left < 0:
				#~ this.camera.rect.left = 0
		#~ if this.keys.right:
			#~ this.camera.rect.x += this.scrollamt
			#~ if this.camera.rect.right > this.world.mapsize[0]:
				#~ this.camera.rect.right = this.world.mapsize[0]
				
		if this.keys.up:
			this.world.player.move("up")
		elif this.keys.down:
			this.world.player.move("down")
		elif this.keys.right:
			this.world.player.move("right")
		elif this.keys.left:
			this.world.player.move("left")
		
		this.world.player.update()
		
		for m in this.world.monsters:
			m.update()
		
		# Center the camera on the player
		this.camera.rect.center = this.world.player.rect.center
		
		#print this.camera.rect.left, this.camera.rect.top
		#TODO: Update world entities here
	
	def draw(this, screen):
		this.world.draw(screen, this.camera)
		this.world.player.draw(screen, this.camera)
		for m in this.world.monsters:
			m.draw(screen, this.camera)
