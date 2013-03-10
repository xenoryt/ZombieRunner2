import pygame
from pygame.locals import *



class Tile(pygame.sprite.Sprite, object):
"""
Tile()
This class is used to store data on individual tiles on the map.
It can store and retrieve data on the objects located standing on the 
tile. The World class contains a 2D array of this class to draw and 
manipulate the map.
"""
	
	images = []
	size = (64,64)
	def __init__(this, type = None, loc=(0,0)):
		pygame.sprite.Sprite.__init__(this)
		this._type = type
		this._gridloc = loc
		this.image = None
		
	@property
	def type(this):
		"""
		The tile type. Ex: Ground, Wall
		"""
		return this._type
	
	@type.setter
	def type(this, t):
		if type(t) == str:
			if   t == '.':
				t = Type.Null
			elif t == '#':
				t = Type.Wall
			elif t == '^':
				t = Type.Tower
			else:
				t = Type.Null
			
		elif type(t) == int: 
			this._type = t
			
		this.image = this.images[this._type]
		
	
	@property
	def gridloc(this):
		return this._gridloc
	
	@gridloc.setter
	def gridloc(this, loc):
		"""
		loc should be a tuple like (0,0)
		"""
		this._gridloc = loc
	
	@property
	def maploc(this):
		return (this._gridloc[0] * this.size[0], this._gridloc[1] * this.size[1])
	
	
	class Type:
		Null, Wall, Tower = range(3)
