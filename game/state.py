import gui
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
	Everything a this.game state does will be contained
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
		
		raise NotImplementedError("Used default draw function in state class")


## Some game states ##

def btnMsgboxClick():
	this.game.revertState()
	return 0

class MessageboxState(State):
	def __init__(this, game, text):
		print "Entered messagebox state"
		print text
		print ""
		
		this.game = game
		
		this.text = text
		
		this.box = gui.Container()
		this.box.rect.center = (this.game.screensize[0]/2, this.game.screensize[1]/2)
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
				this.game.running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.game.running = False
				elif event.key == K_2:
					this.game.revertState()
		this.box.update()
	
	def draw(this, screen):
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))
		screen.blit(background, (0, 0))
		
		this.box.draw(screen)
		

class MainMenuState(State):
	def __init__(this, world = None):
		this.btnStart = gui.Button("Start")
		this.btnExit = gui.Button("Exit")
		
		this.btnStart.onClick = lambda: this.game.assignState(GameState())
		this.btnExit.onClick = lambda: this.game.revertState()
	
	def update(this):
		this.btnStart.update()
		this.btnExit.update()


class PauseState(State):
	def __init__(this, game, world = None):
		this.game = game
		
		this.btnResume = gui.Button("Resume")
		this.btnExit = gui.Button("Exit")
		this.box = gui.Container()
		
		this.box.add(this.btnResume, 1,1)
		this.box.add(this.btnExit, 2,1)
		
		this.btnResume.onClick = lambda: this.game.revertState()
		this.btnExit.onClick = lambda: this.game.Exit()
		
		this.box.center((this.game.screensize[0]/2,this.game.screensize[1]/2))
		
	def update(this):
		for event in pygame.event.get():
			if event.type == QUIT:
				this.game.running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.game.revertState()
		this.box.update()
	
	def draw(this, screen):
		this.box.draw(screen)

class GameState(State):
	def __init__(this, game, level = 1):
		this.game = game
		
		this.world = None
		this.level = level
		this.camera = Camera(this.game.screensize)
		this.keys = Keys()
		
		# Allows player to pan camera across the map
		this.scrollamt = 6
		this.mapmode = False
		
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
				this.game.Exit()
				this.world.save()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.world.save()
					this.game.assignState(PauseState(this.game))
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
				elif event.key == K_m:
					this.mapmode = not this.mapmode
				elif event.key == K_F11:
					this.game.fullscreen = not this.game.fullscreen
					if this.game.fullscreen:
						pygame.display.set_mode(this.game.screensize, pygame.FULLSCREEN)
					else:
						pygame.display.set_mode(this.game.screensize)
				
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
			if not this.mapmode:
				this.world.player.move("up")
			else:
				this.camera.rect.y -= this.scrollamt
				if this.camera.rect.top < 0:
					this.camera.rect.top = 0;
		if this.keys.down:
			if not this.mapmode:
				this.world.player.move("down")
			else:
				this.camera.rect.y += this.scrollamt
				if this.camera.rect.bottom > this.world.mapsize[1]:
					this.camera.rect.bottom = this.world.mapsize[1];
		if this.keys.right:
			if not this.mapmode:
				this.world.player.move("right")
			else:
				this.camera.rect.x += this.scrollamt
				if this.camera.rect.right > this.world.mapsize[0]:
					this.camera.rect.right = this.world.mapsize[0]
		if this.keys.left:
			if not this.mapmode:
				this.world.player.move("left")
			else:
				this.camera.rect.x -= this.scrollamt
				if this.camera.rect.left < 0:
					this.camera.rect.left = 0
		
		turn = False
		if this.world.player.actions == 0:
			this.world.player.turn()
			turn = True
		
		this.world.player.update()
		
		for m in this.world.monsters:
			if turn:
				m.turn()
			m.update()
		
		if not this.mapmode:
			# Center the camera on the player
			this.camera.rect.center = this.world.player.rect.center
		
		#print this.camera.rect.left, this.camera.rect.top
		#TODO: Update world entities here
	
	def draw(this, screen):
		this.world.draw(screen, this.camera)
		this.world.player.draw(screen, this.camera)
		for m in this.world.monsters:
			m.draw(screen, this.camera)
