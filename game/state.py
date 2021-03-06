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
import os

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
		this.button.onClick = lambda x: this.game.revertState()
		this.label = gui.Label(text)
		this.box.add(this.label,1,1)
		this.box.add(this.button,2,1)
		
		# Create label for messagebox and put it into this.box
	
	def update(this):
		# Get input
		for event in pygame.event.get():
			if event.type == QUIT:
				this.game.Exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.game.Exit()
		
		this.box.update()
	
	def draw(this, screen):
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))
		screen.blit(background, (0, 0))
		
		this.box.draw(screen)
		

class MainMenuState(State):
	def startmenu(this, sender):
		this.world.terminate()
		this.game.world.terminate()
		this.game.assignState(GameState(this.game))
	def contmenu(this, sender):
		this.game.assignState(GameState(this.game))
		this.world.terminate()
	def exitmenu(this, sender):
		this.world.terminate()
		this.game.Exit()
	
	def __init__(this, game):
		this.game = game
		this.game.world = world.World()
		this.hasSaves = this.game.world.load("map")
		this.err = ""
		
		this.btnStart = gui.Button("New")
		this.btnCont = gui.Button("Continue")
		this.btnExit = gui.Button("Exit")
		
		this.btnStart.onClick = this.startmenu
		this.btnCont.onClick = this.contmenu
		this.btnExit.onClick = this.exitmenu
		
		centerx = this.game.screensize[0]/2
		centery = this.game.screensize[1]/2
		#~ this.btnStart.rect.center = (centerx, centery-30)
		#~ this.btnCont.rect.center = (centerx,centery)
		#~ this.btnExit.rect.center = (centerx, centery+30)
		
		this.btnStart.rect.bottomright =(770,30)
		this.btnCont.rect.bottomright = (770,60)
		this.btnExit.rect.bottomright = (770,90)
		
		generator = mapgenerator.MapGenerator()
		this.world = generator.create("map_menu",4, 8)
		if this.world == None:
			this.err = "Something went wrong with map generation...\nPlease try running the game again"
			
		
		# Create a camera and set it to a random position on map
		this.camera = Camera(this.game.screensize)
		x = random.randint(0,this.world.mapsize[0]-this.camera.rect.size[0])
		y = random.randint(0,this.world.mapsize[1]-this.camera.rect.size[1])
		this.camera.rect.x = x
		this.camera.rect.y = y
		
		
	def update(this):
		if this.err != "":
			this.game.Error(this.err)
			return
		
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
					this.camera.clip(this.world)
		
		if this.game.world.loaded:
			this.btnCont.update()
		
		this.btnStart.update()
		this.btnExit.update()
		
		
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
		
		this.btnResume.onClick = lambda x: this.game.revertState()
		this.btnFullscreen.onClick = lambda x: this.game.toggle_fullscreen()
		this.btnExit.onClick = lambda x: this.game.Exit()
		
		this.box.center((this.game.screensize[0]/2,this.game.screensize[1]/2))
		
	def update(this):
		for event in pygame.event.get():
			if event.type == QUIT:
				this.game.Exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.game.revertState()
		this.box.update()
	
	def draw(this, screen):
		this.box.draw(screen)

class InventoryState(State):
	btnImages = []
	invImages = []
	def __init__(this, game):
		this.game = game
		
		# Create a reference to the actual inventory
		this.inv = this.game.world.inventory
		size = len(this.inv)
		
		# Create background wallpaper
		img = pygame.image.load(os.path.join("data","wall.png"))
		this.bg = pygame.Surface(this.game.screensize)
		this.bg = this.bg.convert()
		for row in range(this.game.screensize[1]/48+1):
			for col in range(this.game.screensize[0]/48+1):
				r = pygame.Rect(col*48, row*48, 48,48)
				this.bg.blit(img,r)
		
		# Label for state title
		this.label = gui._Label("Inventory")
		this.label.bgColor = None
		this.label.fgColor = Color("#2CF3DB")
		this.label.rect.topleft = (50,100)
		
		# HP Bar to display Player's HP
		this.hpbar = gui.Bar()
		this.hpbar.rect.topleft = (15,50)
		this.hpbar.fgColor = Color("red")
		this.hpbar.bgColor = Color("#B0DA87")
		this.hpbar.text = "HP"
		
		
		# Buttons for switching states
		this.btnResume = gui.Button("Resume")
		this.btnResume.onClick = lambda x: this.game.revertState()
		
		this.btnExit = gui.Button("Exit")
		this.btnExit.onClick = lambda x: this.game.Exit()
		
		this.btnResume.rect.bottomleft = (50,540)
		this.btnExit.rect.bottomleft = (50,570)
				
		
		
		# The function that is called when an item is selected
		def select(btn):
			this.selected = btn
			
			this.btnImage.images = [this.invImages[btn.item.ID]]
			this.btnImage.requireUpdate = True
			this.lblDesc.text = str(btn.item)
			this.lblDesc.rect.midtop = (600,275)
			
			if btn.item.ID != 0:
				this.lblDesc.visible = True
				this.btnDrop.visible = True
				if btn.item.ID != 5:
					this.btnUse.visible = True
				else:
					this.btnUse.visible = False
					
				
				if btn.item.Type == 2:
					if not btn.item.equipped:
						this.btnUse.text = "Equip"
					else:
						this.btnUse.text = "Unequip"
				else:
					this.btnUse.text = "Use"
			else:
				this.lblDesc.visible = False
				this.btnUse.visible = False
				this.btnDrop.visible = False
				
			this.drawbg = True
		
		# Functions for handling items
		def use(btn):
			if this.selected.item.Type == 2:
				if this.selected.item.equipped:
					# unequip weapon
					this.game.world.player.weapon = None
					this.selected.text = ""
					this.btnUse.text = "Equip"
				else:
					# equip weapon
					for btn in this.inv.ctrls:
						if btn.item == this.game.world.player.weapon:
							btn.text = ""
							break
					this.game.world.player.weapon = this.selected.item
					this.selected.text = "E"
					this.btnUse.text = "Unequip"
			else:
				if this.selected.item.Type == 3:
					this.game.world.player.setBuff(this.selected.item.attributes)
				else:
					this.game.world.player.setAtt(this.selected.item.attributes)
				this.game.world.removeitem(this.selected)
				#~ this.selected.item.delete()
				this.selected.images = [this.invImages[this.selected.item.ID]]
				this.selected.requireUpdate = True
				select(this.selected)
		
		def drop(btn):
			this.game.world.removeitem(this.selected)
			#~ this.selected.item.delete()
			this.selected.images = [this.invImages[this.selected.item.ID]]
			this.selected.requireUpdate = True
			select(this.selected)
		
		
		# Controls to display item info on sides and handle items
		this.btnImage = gui.Button("")
		this.btnImage.rect.size = (100,100)
		this.btnImage.static = True
		this.btnImage.rect.midtop = (600,150)
		
		this.lblDesc = gui.Label("")
		this.lblDesc.static = False
		this.lblDesc.rect.midtop = (600,275)
		this.lblDesc.font(12)
		
		this.btnUse = gui.Button("Use")
		this.btnUse.static = True
		this.btnUse.rect.midtop = (600,425)
		this.btnUse.visible = False
		this.btnUse.onClick = use
		
		this.btnDrop = gui.Button("Discard")
		this.btnDrop.rect.midtop = (600,455)
		this.btnDrop.visible = False
		this.btnDrop.onClick = drop
		
		
		# The inventory 
		this.inv = gui.Container()
		
		this.drawbg = True
		
		#TODO: add resume/exit buttons at y:640+
		
		for col in range(8):
			for row in range(4):
				btn = gui.Button("")
				btn.fgColor = Color("#02A900")
				btn.static = True
				#~ btn.images = this.btnImages
				btn.rect.w = 48
				btn.rect.h = 48
				# TODO: load items
				btn.item = this.game.world.inventory[col + row*8]
				btn.images = [this.invImages[btn.item.ID]]
				btn.onClick = select
				
				if btn.item.equipped:
					btn.text = "E"
				
				this.inv.add(btn, row+1,col+1)
				
				
		this.inv.rect.topleft = (25,160)
	
	def update(this,):
		for event in pygame.event.get():
			if event.type == QUIT:
				this.game.Exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					this.drawbg = True
					this.game.revertState()
		this.inv.update()
		this.label.update()
		this.btnResume.update()
		this.btnExit.update()
		
		this.btnImage.update()
		this.lblDesc.update()
		this.btnUse.update()
		this.btnDrop.update()
		this.hpbar.value = int(this.game.world.player.hp)
		this.hpbar.maxvalue = this.game.world.player.maxhp
		
	def draw(this,screen):
		if this.drawbg:
			#~ background = pygame.Surface(screen.get_size())
			#~ background = background.convert()
			#~ background.fill(Color('#BBBBBB'))
			#~ background.set_alpha(5)
			screen.blit(this.bg, (0, 0))
			this.drawbg = False
		
		
		this.inv.draw(screen)
		this.label.draw(screen)
		this.btnResume.draw(screen)
		this.btnExit.draw(screen)
		
		this.btnImage.draw(screen)
		this.lblDesc.draw(screen)
		this.btnUse.draw(screen)
		this.btnDrop.draw(screen)
		this.hpbar.draw(screen)

class GameState(State):
	def __init__(this, game):
		this.game = game
		
		this.world = None
		this.camera = Camera(this.game.screensize)
		this.keys = Keys()
		
		this.turn = 1
		this.err = ""
		
		# if character died
		this.died = False
		
		# Allows player to pan camera across the map
		this.scrollamt = 16
		this.mapmode = False
		
		# The hp bar
		this.hpbar = gui.Bar()
		this.hpbar.rect.topleft = (15,50)
		this.hpbar.fgColor = Color("red")
		this.hpbar.bgColor = Color("#B0DA87")
		this.hpbar.text = "HP"
		
		if not this.game.world.loaded:
			generator = mapgenerator.MapGenerator()
			this.game.world = generator.create("map",1)
			if this.game.world == None:
				this.err = "Something went wrong with map generation...\nPlease try running the game again"
				this.game.Error(this.err)
		
		this.world = this.game.world
		
		lvl = 0
		if this.world != None:
			lvl = this.world.level
		# The label
		this.lblDungeon = gui.Label("Dungeon: "+str(lvl))
		this.lblDungeon.bgColor = None
		this.lblDungeon.fgColor = Color("#565656")
		this.lblDungeon.rect.topleft = (15,15)
		
	
	#~ def loadWorld(this, mapname):
		#~ if this.world != None:
			#~ this.world.save()
		#~ this.world = world.World()
		#~ this.world.load(mapname)
		#~ this.game.world = this.world
		#~ this.camera.rect.center = this.world.player.rect.center
		#~ #TODO: LOAD WORLD ENTITIES HERE
	
	def update(this):
		#~ if this.err != "":
			#~ this.game.Error(this.err)
			#~ return 
		
		if this.died:
			this.game.revertState()
			this.died = False
			return
		
		# Get input 
		for event in pygame.event.get():
			if event.type == QUIT:
				this.world.save()
				this.game.Exit()
				
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
				
				elif event.key == K_s:
					this.world.player.move("none")
				
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
		if this.world.player.hp < 1:
			msg = "Game Over\n"
			msg+= "Died on floor: " + str(this.world.level)
			this.world.terminate()
			del this.world
			this.game.world.loaded = False
			this.game.msgbox(msg)
			this.died = True
			return 
		
		# Check for key events
		if this.keys.up:
			if not this.mapmode:
				this.world.player.move("up")
			else:
				this.camera.rect.y -= this.scrollamt
		if this.keys.down:
			if not this.mapmode:
				this.world.player.move("down")
			else:
				this.camera.rect.y += this.scrollamt
		if this.keys.right:
			if not this.mapmode:
				this.world.player.move("right")
			else:
				this.camera.rect.x += this.scrollamt
		if this.keys.left:
			if not this.mapmode:
				this.world.player.move("left")
			else:
				this.camera.rect.x -= this.scrollamt
		
		
		this.world.player.update()
		
		if not this.world.player.animating:
			# Check if player is standing on staircase
			obj = this.world.player.tile.getObject()
			if obj != None and obj.name == "stair":
				if this.world.level >= 10:
					this.game.msgbox("You Win!")
					del this.world
					this.game.world.loaded = False
					this.game.msgbox(msg)
					this.died = True
					return 
					
				playerhp = this.world.player.hp
				
				generator = mapgenerator.MapGenerator()
				
				
				this.world = generator.create("map", this.world.level+1,6,this.world.inventory, this.world.player.buffs)
				this.game.world = this.world
				this.lblDungeon.text = "Dungeon: " + str(this.world.level)
				this.world.player.hp = playerhp
			
		
		
		newturn = True
		for m in this.world.monsters:
			m.update()
			if m.curturn == 2:
				newturn = False
		
		if newturn:
			this.world.player.curturn = 1
		
		if not this.mapmode:
			# Center the camera on the player
			this.camera.rect.center = this.world.player.rect.center
		
		# Make sure the camera's view stays on the map
		this.camera.clip(this.world)
		
		hp = this.world.player.hp
		this.hpbar.value = int(hp)
		this.hpbar.maxvalue = this.game.world.player.maxhp
		this.lblDungeon.update()
	
	def draw(this, screen):
		this.world.draw(screen, this.camera)
		for obj in this.world.objects:
			obj.draw(screen, this.camera)
		this.world.player.draw(screen, this.camera)
		for m in this.world.monsters:
			m.draw(screen, this.camera)
		
		this.lblDungeon.draw(screen)
		this.hpbar.draw(screen)
		
		
