import pygame
from pygame.locals import *



#~ class Type:
	#~ Floor, Wall, Trap, Chest, Portal, \
	#~ Ghost, Hound, Zombie, \
	#~ Ghoul, Demon, Guardian, Dragon, \
	#~ Player = range(13)
	#~ 
	#~ _tiles = {'.':Floor, '#':Wall, '^':Trap, '$':Chest, '*':Portal, 
				#~ 'g':Ghost, 'h':Hound, 'z':Zombie,
				#~ 'G':Ghoul, 'D':Demon, 'A':Guardian, 'R':Dragon,
				#~ '@':Player}
	#~ 
	#~ def conv(this,c):
		#~ if type(c) != str:
			#~ raise TypeError
		#~ return this._tiles[c]
	#~ 
	#~ def char(this, t):
		#~ if type(t) != int:
			#~ raise TypeError
		#~ 
		#~ vals = this._tiles.values()
		#~ for i in range(len(vals)):
			#~ if t == vals[i]:
				#~ return this._tiles.keys()[i]

def charToTile(c):
	return 0 if c == '.' else 1

def tileToChar(t):
	return '.' if t == 0 else '#'


class Tile(pygame.sprite.Sprite, object):
	"""
	This class is used to store data on individual tiles on the map.
	It can store and retrieve data on the objects located standing on the 
	tile. The World class contains a 2D array of this class to draw and 
	manipulate the map.
	"""
	
	images = []
	size = (48,48)
	def __init__(this, type = None, gridloc=(0,0)):
		pygame.sprite.Sprite.__init__(this)
		this._gridloc = gridloc
		this.type = type
		
		# Stores the sprites/entities that are above this tile
		this.contains = []
		
		# this var is to store how bright the tile is lit
		this.lighting = 0
		
		# this var stores how far this tile is from the player
		this.distance = 99
		
		#~ this.image = this.images[this.type]
		#~ this.rect = this.image.get_rect(topleft=this.maploc)
		
		# Set whether or not a sprite can walk onto this tile
		this.passable = True if this.type == 0 else False
		
		# Set whether or not the tile has been seen by the player before
		this.explored = False
	
	def __str__(this):
		return tileToChar(this._type)
	
	def update(this):
		# Set whether or not a sprite can walk onto this tile
		if this.type == 0:
			this.passable = True if len(this.contains) == 0 else False
		
	
	def draw(this, surface, camera):
		""" Draws the tile onto a surface """
		# Check if the tile is NOT visible
		#  - world.draw now handles this. This check is now obsolete
		#~ if this.rect.right < camera.rect.left or this.rect.left > camera.rect.right:
			#~ return None
		#~ if this.rect.top > camera.rect.bottom or this.rect.bottom < camera.rect.top:
			#~ return None
		
		# If lighting is 0, draw just black image
		if this.lighting <= 0:
			fog = pygame.Surface(this.size)
			fog = fog.convert()			
			if this.explored:
				fog.fill((50,50,50))
				fog.set_alpha(128)
				surface.blit(this.image, camera.getrect(this.rect))
				surface.blit(fog, camera.getrect(this.rect))
			else:
				fog.fill((0,0,0))
				surface.blit(fog, camera.getrect(this.rect))
		else:
			# Else draw the tile
			surface.blit(this.image, camera.getrect(this.rect))
		
		
	#~ @property
	#~ def rect(this):
		#~ return pygame.Rect(this.maploc[0], this.maploc[1], this.size[0], this.size[1])
	
	@property
	def type(this):
		"""
		The tile type. Ex: Ground, Wall
		"""
		return this._type
	
	@type.setter
	def type(this, t):
		if type(t) == str:
			this._type = charToTile(t)
		elif type(t) == int: 
			this._type = t
		
		
		this.image = this.images[this._type]
		this.rect = this.image.get_rect(topleft = this.maploc)
		
		
	
	@property
	def gridloc(this):
		return this._gridloc
	
	@gridloc.setter
	def gridloc(this, loc):
		"""
		loc should be a tuple like (0,0)
		"""
		this._gridloc[0] = loc[0]*this.size[0]
		this._gridloc[1] = loc[1]*this.size[1]
	
	@property
	def maploc(this):
		return (this._gridloc[0] * this.size[0], this._gridloc[1] * this.size[1])
	


