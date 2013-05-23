import gui
import pygame
from pygame.locals import *
import world
import mapgenerator
import math
from camera import Camera
from keys import Keys
import sprite
import random

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
		this.button.onClick = lambda: this.game.revertState()
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
	def __init__(this, game):
		this.game = game
		this.game.world = world.World()
		this.hasSaves = this.game.world.load("map")
		
		this.btnStart = gui.Button("New Game")
		this.btnCont = gui.Button("Continue")
		this.btnExit = gui.Button("Exit")
		
		this.btnStart.onClick = lambda: this.game.assignState(GameState(this.game))
		this.btnCont.onClick = lambda: this.game.assignState(GameState(this.game))
		this.btnExit.onClick = lambda: this.game.revertState()
		
		centerx = this.game.screensize[0]/2
		centery = this.game.screensize[1]/2
		#~ this.btnStart.rect.center = (centerx, centery-30)
		#~ this.btnCont.rect.center = (centerx,centery)
		#~ this.btnExit.rect.center = (centerx, centery+30)
		
		this.btnStart.rect.bottomright =(770,30)
		this.btnCont.rect.bottomright = (770,60)
		this.btnExit.rect.bottomright = (770,90)
		
		generator = mapgenerator.MapGenerator()
		this.world = generator.create("map_menu",1,(80,80),8)
		
		# Create a camera and set it to a random position on map
		this.camera = Camera(this.game.screensize)
		x = random.randint(0,this.world.mapsize[0]-this.camera.rect.size[0])
		y = random.randint(0,this.world.mapsize[1]-this.camera.rect.size[1])
		this.camera.rect.x = x
		this.camera.rect.y = y
		
		
	def update(this):
		
		for event in pygame.event.get():
			if event.type == QUIT:
				this.world.terminate()
				this.game.Exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.world.terminate()
					this.game.Exit()
			elif event.type == MOUSEMOTION:
				if event.buttons[0] == 1:
					x,y = event.rel
					this.camera.rect.x -= x
					this.camera.rect.y -= y
					if this.camera.rect.top < 0:
						this.camera.rect.top = 0;
					elif this.camera.rect.bottom > this.world.mapsize[1]:
						this.camera.rect.bottom = this.world.mapsize[1];
					if this.camera.rect.right > this.world.mapsize[0]:
						this.camera.rect.right = this.world.mapsize[0]
					elif this.camera.rect.left < 0:
						this.camera.rect.left = 0
		
		
		this.btnStart.update()
		this.btnExit.update()
		if this.game.world.loaded:
			this.btnCont.update()
		
	def draw(this, screen):
		this.world.draw(screen, this.camera, False)
		for m in this.world.monsters:
			m.draw(screen, this.camera, False)
		for obj in this.world.objects:
			obj.draw(screen, this.camera, False)
		
		this.btnStart.draw(screen)
		this.btnExit.draw(screen)
		if this.game.world.loaded:
			this.btnCont.draw(screen)

class PauseState(State):
	def __init__(this, game, world = None):
		this.game = game
		
		this.btnResume = gui.Button("Resume")
		this.btnFullscreen = gui.Button("Toggle Fullscreen")
		this.btnExit = gui.Button("Exit")
		this.box = gui.Container()
		
		this.box.add(this.btnResume, 1,1)
		this.box.add(this.btnFullscreen,2,1)
		this.box.add(this.btnExit, 3,1)
		
		this.btnResume.onClick = lambda: this.game.revertState()
		this.btnFullscreen.onClick = lambda: this.game.toggle_fullscreen()
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

class InventoryState(State):
	btnImages = []
	def __init__(this, game):
		this.game = game
		
		# Create a reference to the actual inventory
		this.inv = this.game.world.inventory
		size = len(this.inv)
		
		
		this.label = gui._Label("Inventory")
		this.label.bgColor = None
		this.label.fgColor = Color("#731E7A")
		this.label.rect.topleft = (50,50)
		
		
		this.box = gui.Container()
		
		
		this.drawbg = True
		
		#TODO: add resume/exit buttons at y:640+
		
		for col in range(8):
			for row in range(4):
				btn = gui.Button("")
				btn.static = True
				btn.images = this.btnImages
				btn.rect.w = 48
				btn.rect.h = 48
				this.box.add(btn, row+1,col+1)
		this.box.rect.topleft = (50,120)
	
	def update(this,):
		for event in pygame.event.get():
			if event.type == QUIT:
				this.game.running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.drawbg = True
					this.game.revertState()
		this.box.update()
		this.label.update()
		
	def draw(this,screen):
		if this.drawbg:
			background = pygame.Surface(screen.get_size())
			background = background.convert()
			background.fill(Color('black'))
			background.set_alpha(100)
			screen.blit(background, (0, 0))
			this.drawbg = False
		
		this.box.draw(screen)
		this.label.draw(screen)

class GameState(State):
	def __init__(this, game):
		this.game = game
		
		this.world = None
		this.camera = Camera(this.game.screensize)
		this.keys = Keys()
		
		this.turn = 1
		
		# Allows player to pan camera across the map
		this.scrollamt = 16
		this.mapmode = False
		
		# TODO: Add checking for continues
		
		this.loadWorld("map")
		
	
	def loadWorld(this, mapname):
		if this.world != None:
			this.world.save()
		this.world = world.World()
		this.world.load(mapname)
		this.game.world = this.world
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
					this.game.assignState(InventoryState(this.game))
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
					this.game.toggle_fullscreen()
				
			if event.type == KEYUP:
				if event.key == K_UP:
					this.keys.up = False
				elif event.key == K_DOWN:
					this.keys.down = False
				elif event.key == K_LEFT:
					this.keys.left = False
				elif event.key == K_RIGHT:
					this.keys.right = False
		
		# check for gameover situations
		if this.world.player.hp <= 0:
			msg = "Game Over\n"
			msg+= "Died on floor: " + str(this.world.level)
			this.world.terminate()
			this.game.msgbox(msg)
			this.game.Exit()
			return 
		
		# Check for key events
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
		
		
		if this.world.player.actions == 0 and not this.world.player.animating:
			# Check if player is standing on chest or staircase
			obj = this.world.player.tile.getObject()
			if obj != None and obj.name == "stair":
				generator = mapgenerator.MapGenerator()
				this.world = generator.create("map", this.world.level+1)
			
		
		this.world.player.update()
		newturn = True
		for m in this.world.monsters:
			m.update()
			if m.curturn == 2:
				newturn = False
				#~ print m, m.curturn
		
		if newturn:
			this.world.player.curturn = 1
			#~ sprite.Monster.curturn = 1
		
		if not this.mapmode:
			# Center the camera on the player
			this.camera.rect.center = this.world.player.rect.center
		
		#print this.camera.rect.left, this.camera.rect.top
		#TODO: Update world entities here
	
	def draw(this, screen):
		this.world.draw(screen, this.camera)
		for obj in this.world.objects:
			obj.draw(screen, this.camera)
		this.world.player.draw(screen, this.camera)
		for m in this.world.monsters:
			m.draw(screen, this.camera)
		
