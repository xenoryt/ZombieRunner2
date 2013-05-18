import pygame
from ai import AI

directions = {"up":[0,-1], "down":[0,1], "left":[-1,0], "right":[1,0], "none":[0,0]}

def move(loc, dir):
	nloc = list(loc) # make nloc a list of loc
	nloc[0] += directions[dir][0]
	nloc[1] += directions[dir][1]
	return tuple(nloc)

class Sprite(pygame.sprite.Sprite, object):
	"""
	The main sprite class.
	It is intended to be used to store data on the player,
	however the Monster class is derived from this class.
	"""
	images = []
	def __init__(this, world = None):
		pygame.sprite.Sprite.__init__(this, this.groups)
		this.image = None
		this.rect = None
		
		# Carry a reference to the world
		this.world = world
		
		# The tile the sprite is standing on
		this._tile = None 
		
		# Stats
		this.hp = 0
		this.def = 0
		this.atk = 0
		
		# This is how many actions per turn the sprite gets to perform
		# 0.5 means 1 action every 2 turns
		this.spd = 1
		
		# This var stores how many actions are left to perform
		this.actions = 0
		
		# how far the sprite can see 
		# 5 is slightly less than half the screen height
		this.sight = 5
		
		# This var sets the radius of the area that is lit up 
		# around this sprite
		this.brightness = 0
		
		# This var is used to store whether or not the sprite
		# is in the middle of an animation
		this.animating = False
		
		this._moving = False
		this._attacking = False
	
	@property
	def tile(this):
		return this._tile
	
	@tile.setter
	def tile(this, tile):
		if this._tile != None:
			this._tile.contains.remove(this)
		this._tile = tile
		this._tile.contains.append(this)
		
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
			tile.distance = -1
			tile.lighting = 0
		
		
		marked = [] # Stores tiles that have already been marked
		queue = [this.tile] # Stores tiles that have not yet been marked
		
		for dist in range(15):
			newqueue = []
			for tile in queue:
				tile.distance = dist
				if dist < this.sight: 
					tile.lighting = this.sight - dist
				for d in directions:
					loc = move(tile.gridloc, d)
					if world.map[loc[1]][loc[0]] not in marked:
						newqueue.append(world.map[loc[1]][loc[0]])
			queue = list(set(newqueue))
	
	def update(this):
		#TODO: updating animation frames
	
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
		
		# If its not moving in any direction, do nothing
		if direction[0] == 0 and direction[1] == 0:
			return False
		
		d = direction
		if this.tile == None:
			this.getCurrentTile()
		
		# Check if the tile the sprite is moving to is passable
		loc = this.tile.gridloc
		if map[loc[1] + d[1]][loc[0] + d[0]].passable:			
			this.rect.x += directions[direction][0]
			this.rect.y += directions[direction][1]
			
			# Check if this sprite has moved off of its current tile
			if this.rect.centerx < this.tile.rect.left or this.rect.centerx > this.tile.rect.right:
				this.tile = map[loc[1] + d[1]][loc[0] + d[0]]
			elif this.rect.centery < this.tile.rect.top or this.rect.centery > this.tile.rect.bottom:
				this.tile = map[loc[1] + d[1]][loc[0] + d[0]]
		
		return True
		
		


class Monster(Sprite):
	"""
	Very similar to the Sprite class with less stats and an AI.
	Monsters are also automagically recorded in a list in the current
	world.
	"""
	images = []
	
	def __init__(this, world = None):
		#~ pygame.sprite.Sprite.__init__(this, this.groups)
		
		# Call the parent constructor
		super(Monster, this).__init__(world)
		
		this.ai = AI(this)
		
		# Add this monster to list of monsters
		world.monsters.append(this)
	
	@property
	def tile(this):
		return this._tile
	
	@tile.setter
	def tile(this, tile):
		if this._tile != None:
			this._tile.contains.remove(this)
		this._tile = tile
		this._tile.contains.append(this)
	
	def update(this):
		pass
