import pygame
from ai import AI
import os
import random

directions = {"up":[0,-1], "down":[0,1], "left":[-1,0], "right":[1,0], "none":[0,0]}

def move(loc, dir):
	nloc = list(loc) # make nloc a list of loc
	nloc[0] += directions[dir][0]
	nloc[1] += directions[dir][1]
	return tuple(nloc)


def loadImages(sprite, imagefile, d):
	sheet = pygame.image.load(os.path.join("data",imagefile))
	sheetrect = sheet.get_rect()
	images = []
	#~ print imagefile, d, range(sheetrect.width/48)
	for x in range(sheetrect.width/48):
		rect = pygame.Rect(x*48,0, 48,48)
		image = pygame.Surface((48,48))
		image.blit(sheet, (0,0),rect)
		image.set_colorkey((255,0,255))
		images.append(image)
	sprite.images[d] = images


class Sprite(pygame.sprite.Sprite, object):
	"""
	The main sprite class.
	It is intended to be used to store data on the player,
	however the Monster class is derived from this class.
	"""
	images = {}
	def __init__(this, world = None):
		pygame.sprite.Sprite.__init__(this)
		
		this.rect = this.images["up"][0].get_rect()
		
		# Carry a reference to the world
		this.world = world
		
		# The tile the sprite is standing on
		this._tile = None 
		
		this.name = "player"
		this.type= "player"
		
		# Stats
		this.maxhp = 100
		this.hp = this.maxhp
		this.atk = 8
		
		# This is how many actions per turn the sprite gets to perform
		# 0.5 means 1 action every 2 turns
		this.spd = 1
		
		# This var stores how many actions are left to perform
		this.actions = 1
		
		# how far the sprite can see 
		# 5 is slightly less than half the screen height
		this.sight = 6
		
		# This var sets the radius of the area that is lit up 
		# around this sprite
		this.brightness = 0
		
		# This var is used to store whether or not the sprite
		# is in the middle of an animation
		this.animating = False
		
		# Stores the current animation frame
		this.aniframe = 0
		this.atkframe = 0
		
		# Stores how much to increment/decrement animation frame
		this.nextframe = 0.2
		
		this._moving = False
		this._attacking = False
		
		# Stores the direction the sprite is facing/moving
		this.direction = "down"
		
		# Stores the tile the sprite is walking towards
		this.nextTile = None
		
	
	@property
	def tile(this):
		return this._tile
	
	@tile.setter
	def tile(this, tile):
		if this._tile != None:
			this._tile.contains.remove(this)
		
		this._tile = tile
		
		if tile != None:
			this._tile.contains.append(this)
			this._tile.passable = False
		
		# Update tile distance values 
		this.markTiles()
	
	@property
	def moving(this):
		return this._moving
	
	@moving.setter
	def moving(this, isMoving):
		"""
		Sets whether or not it is currently performing the moving
		animation. If it is still attacking when moving is set to false,
		the animating boolean will remain True.
		"""
		if not isMoving:
			this.animating = True if this.attacking else False
		else:
			this.animating = True
		this._moving = isMoving
	
	@property
	def attacking(this):
		return this._attacking
	
	@attacking.setter
	def attacking(this, isAtk):
		if not isAtk:
			this.animating = True if this.moving else False
		else:
			this.animating = True
		this._attacking = isAtk
	
	
	def markTiles(this):
		"""
		Use breadth first search to mark all tiles around the 
		player with a value of how far away it is from the player
		"""
		for tile in this.world.markedtiles:
			tile.distance = 99
			tile.lighting = 0
		
		this.tile.lighting = this.sight
		marked = [] # Stores tiles that have already been marked
		queue = [this.tile] # Stores tiles that have not yet been marked
		
		for dist in range(15):
			newqueue = []
			for tile in queue:
				tile.distance = dist
				
				for d in directions:
					loc = move(tile.gridloc, d)
					if this.world.outBound(loc):
						continue
					nexttile = this.world.map[loc[1]][loc[0]]
					if tile.type == 0 and tile.lighting > 0:
						if nexttile.lighting < this.sight-dist-1:
							nexttile.lighting = this.sight-dist-1
							nexttile.explored = True
					if nexttile.type == 0 and (nexttile not in marked):
						newqueue.append(nexttile)
				
			marked += queue
			queue = list(set(newqueue))
		
		this.world.markedtiles = marked
	
	def turn(this):
		if this.actions < 1:
			this.actions += this.spd
	
	def update(this):
		#TODO: updating animation frames
		
		# Check for animations
		if this.moving:
			this.rect.x += directions[this.direction][0]*4
			this.rect.y += directions[this.direction][1]*4
			
			if this.rect.center == this.nextTile.rect.center:
				this.moving = False
				this.tile = this.nextTile
				this.nextTile = None
				
			# Update animation
			this.aniframe += this.nextframe
			nimages = len(this.images[this.direction])
			if round(this.aniframe,1) == nimages-1 or round(this.aniframe,1) == 0:
				this.nextframe = -this.nextframe
		if this.attacking:
			this.atkframe += 1
			if this.atkframe == 12:
				this.attacking = False
			
			offsetx = this.tile.rect.centerx
			offsety = this.tile.rect.centery
			
			if this.attacking:	
				offsetx = this.tile.rect.centerx + directions[this.direction][0]*16
				offsety = this.tile.rect.centery + directions[this.direction][1]*16
				
			this.rect.center = (offsetx, offsety)
			
			
		
	
	def getCurrentTile(this):
		"""
		Gets the current tile the sprite is standing on.
		This function should only be called when the sprite first spawns
		since it will automagically keep track of the current tile
		after the initial spawn.
		
		Note: 
		This function requires this.world to be set to 
		the current instance of the world else this function fails.
		This function can also be very processor intensive.
		
		Note 2:
		This function is kinda obsolete since the world usually sets the 
		tile the sprite is standing on when a new sprite is loaded. 
		But this function will be used in case it was not set.
		"""
		if this.world == None:
			raise ValueError("World instance in sprite not set!")
		
		# ATTN: Hard coded in tile size (48,48)
		loc = this.rect.center
		gridloc = (loc[0]/48, loc[1]/48) 
		this.tile = map[gridloc[1]][gridloc[0]]
		#~ 
		#~ found = False
		#~ for row in this.world.map:
			#~ for tile in row:
				#~ if tile.rect.right < this.rect.left or tile.rect.left > this.rect.right:
					#~ continue
				#~ if tile.rect.top < this.rect.bottom or tile.rect.bottom > this.rect.top:
					#~ continue
				#~ 
				#~ this.tile = tile
				#~ found = True
				#~ break
			#~ if found:
				#~ break
	
	def move(this, direction):
		""" 
		This function moves the sprite in place
		Note: Direction is a string such as "up" 
		"""
		
		# If there isn't enough action points to perform a move
		if this.actions < 1:
			return False
		
		# If the sprite is currently in the process of moving
		if this.moving:
			return False
		
		d = direction
		# If its not moving in any direction, do nothing
		if directions[d][0] == 0 and directions[d][1] == 0:
			return False
		
		
		if this.tile == None:
			this.getCurrentTile()
		
		# Check if the tile the sprite is moving to is passable
		loc = this.tile.gridloc
		nextTile = this.world.map[loc[1] + directions[d][1]][loc[0] + directions[d][0]]
		if nextTile.passable:
			# Set this sprite to move
			this.direction = d
			this.moving = True
			
			this.nextTile = nextTile
			this.nextTile.passable = False
			this.tile.passable = True
			this.actions -= 1
		else:
			# check if the next tile contains an attackable object
			if len(nextTile.contains) == 0:
				return True
			
			obj = None
			if this.type == "player":
				obj = nextTile.getMonster()
			if this.type == "monster":
				obj = nextTile.getPlayer()
			
			if obj != None:
				print "attacking"
				this.direction = d
				this.attacking = True
				this.atkframe = 0
				atklo = round(this.atk*0.8)
				atkhi = round(this.atk*1.2)
				obj.hp -= random.randint(atklo, atkhi)
				this.actions -= 1
		
		return True
		
	
	def draw(this, screen, camera):
		if this.tile.lighting > 0 or (this.nextTile != None and this.nextTile.lighting > 0):
			screen.blit(this.images[this.direction][int(round(this.aniframe))], camera.getrect(this.rect))
		


class Monster(Sprite):
	"""
	Very similar to the Sprite class with less stats and an AI.
	Monsters are also automagically recorded in a list in the current
	world. This is just to be used as a base class for a variety of 
	different monsters though.
	"""
	images = {}
	
	def __init__(this, level=1, world = None):
		#~ pygame.sprite.Sprite.__init__(this, this.groups)
		
		# Call the parent constructor
		super(Monster, this).__init__(world)
		this.name = "monster"
		this.type = "monster"
		this.spd = 0.7
		this.actions = 0
		
		this.atk = 5
		
		this.ai = AI(this)
		this.sight = 4
		
		# Add this monster to list of monsters
		#~ world.monsters.append(this)
	
	@property
	def tile(this):
		return this._tile
	
	@tile.setter
	def tile(this, tile):
		if this._tile != None:
			this._tile.contains.remove(this)
			this._tile.passable = True
		this._tile = tile
		if tile != None:
			this._tile.contains.append(this)
			this._tile.passable = False
	
	def update(this):
		# If dead, kill self
		if this.hp <= 0:
			this.tile = None
			this.world.monsters.remove(this)
			#TODO: place a chest
			return False
		
		if this.actions >= 1 and not this.moving:
			this.move(this.ai.nextStep())
		
		if this.moving:
			# Move the monster
			this.rect.x += directions[this.direction][0]*4
			this.rect.y += directions[this.direction][1]*4
			
			if this.rect.center == this.nextTile.rect.center:
				this.moving = False
				this.tile = this.nextTile
				this.nextTile = None
				
			# Update animation
			this.aniframe += this.nextframe
			nimages = len(this.images[this.direction])
			if round(this.aniframe, 1) == nimages-1 or round(this.aniframe, 1) == 0:
				this.nextframe = -this.nextframe
		if this.attacking:
			this.atkframe += 1
			if this.atkframe == 12:
				this.attacking = False
			
			offsetx = this.tile.rect.centerx
			offsety = this.tile.rect.centery
			
			if this.attacking:	
				offsetx = this.tile.rect.centerx + directions[this.direction][0]*16
				offsety = this.tile.rect.centery + directions[this.direction][1]*16
				
			this.rect.center = (offsetx, offsety)
		
		
class Bat(Monster):
	"""
	Fast, weak monsters. Very common and very annoying.
	"""
	def __init__(this, level, world = None):
		super(Bat, this).__init__(level, world)
		this.name = "bat"
		this.maxhp = 11+4*level
		this.hp = this.maxhp
		this.atk = 3+2*level
		this.spd = 1.5
		this.sight = 6

class Skel(Monster):
	"""
	Medium speed, low-medium damage, high hp. Don't underestimate them.
	"""
	images = {}
	
	def __init__(this, level, world = None):
		super(Skel, this).__init__(level, world)
		this.name ="skel"
		this.maxhp = 17+5*level
		this.hp = this.maxhp
		this.atk = 10+4*level
		this.spd = 1
		this.sight = 4

class Dragon(Monster):
	"""
	Slow but very high hp. Attacks are very strong
	"""
	images = {}
	
	def __init__(this, level, world = None):
		super(Dragon, this).__init__(level, world)
		this.name="dragon"
		this.maxhp = 10+15*level
		this.hp = this.maxhp
		this.atk = 4+10*level
		this.spd = 0.5+0.15*level
		this.sight = 6

class Reaper(Monster):
	"""
	Very slow and Very deadly. The Reaper's sight also becomes 
	increasingly dangerous later on.
	"""
	images = {}
	
	def __init__(this, level, world = None):
		super(Reaper, this).__init__(level, world)
		this.name="reaper"
		this.maxhp = 5+10*level
		this.hp = this.maxhp
		this.atk = 7+17*level
		this.spd = 0.3 + 0.1*level
		this.sight = int(round(0+level/2.))
		if this.sight > 10:
			this.sight = 10
	


class Chest(Sprite):
	image = None
	def __init__(this, world = None):
		pygame.sprite.Sprite.__init__(this)
		this.rect = this.image.get_rect()
		
		# Carry a reference to the world
		this.world = world
		
		# The tile the sprite is standing on
		this._tile = None 
	
	@property
	def tile(this):
		return this._tile
	
	@tile.setter
	def tile(this, tile):
		if this._tile != None:
			this._tile.contains.remove(this)
		
		this._tile = tile
		
		if tile != None:
			this._tile.contains.append(this)
	
	
	def update(this):
		pass
	
	def draw(this, camera):
		if this.tile.lighting > 0:
			screen.blit(this.image, camera.getrect(this.rect))
