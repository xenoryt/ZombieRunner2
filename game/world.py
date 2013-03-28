import pygame, os
from pygame.locals import *

import tile
from tile import *

class World:
	"""
	A class that stores all the information about a single map.
	It is capable of loading a new map from a file and can also
	create a new blank map given a size.
	Individual tiles of the map can be accessed through [x, y]
	or through [y][x].
	"""
	
	
	def __init__(this):
		this.size = (0,0)
		this.map = []
		this.charmap = []
		this.image = None
	
	def __getitem__(this, index):
		if type(index) != int:
			x,y = index
			return map[y][x]
		else:
			return this.map[index]
	
	def __set__(this, newmap):
		this.size = len(newmap), len(newmap[0])
		if type(newmap[0][0]) == str:
			this.charmap = newmap
			this.map = this.charmap
			for y in range(len(this.charmap)):
				for x in range(len(this.charmap[y])):
					this.map[y][x] = Type.conv(this.charmap[y][x])
		else:
			this.map = newmap
			this.charmap = newmap
			for y in range(len(this.charmap)):
				for x in range(len(this.charmap[y])):
					this.charmap[y][x] = Type.char(this.map[y][x])
	
	def __get__(this):
		return this.charmap
	
	def new(this, size, char='.'):
		"""
		Creates a new map filled with the character [char]
		"""
		this.size = size
		
		map = []
		for y in range(size[1]):
			map.append([char for x in range(size[0])])
			
		this = map
	
	def loadMap(this, mapfile):
		try:
		   with open(mapfile) as fr: pass
		except IOError as e:
		   print 'Error: file %s not found' % mapfile
		   return False
		
		try:
			# read in map file
			map = fr.readlines()
			lines = map.split('\n')
			map = []
			for line in lines:
				map.append(line.split())
			
			# make sure the map dimensions are correct
			for i in range(1,len(map)):
				if len(map[i]) != len(map[i-1]):
					print "Error: invalid map format detected"
					return False
			
			# store dimensions
			this.size = (len(map[0]), len(map))
			
			# Create 2D array of Tile class
			for y in range(this.size[1]):
				this.map.append([])
				for x in range(this.size[0]):
					this.map[y].append(Tile(map[y][x], (x,y)))
					this.map
			
			
		except:
			print "Error: unknown error while loading map file"
			return False
			
		return True
		
	def renderMap(this):
		"""
		renderMap() : pygame.Surface
		Blits all the tiles onto a surface and returns it
		"""
		this.image = pygame.Surface((this.size[0] * Tile.size[0], this.size[1]*Tile.size[1]))
		for y in range(this.size[1]):
			for x in range(this.size[0]):
				map[y][x].image.blit(this.image, map[y][x].maploc)
		
		return this.image
