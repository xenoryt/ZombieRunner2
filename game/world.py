# this class actually only needs pygame.surface and blitting for rendering purposes
# it only needs to render the map each time a new map is loaded
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
	
	# Constructor
	def __init__(this, name = "map.map"):
		# the size of the grid
		# the size of the map is a property defined later on
		this.size = (0,0)
		
		this.map = []
		this.image = None
		this.name = name
		
		# List of all the monsters in the world
		this.monsters = []
		
		# The main player
		this.player = None
	
	# Override the [] operation
	def __getitem__(this, index):
		print "getting index"
		if type(index) != int:
			x,y = index
			return map[y][x]
		else:
			return this.map[index]
	
	# Override = operator (to be fixed)
	#~ def __set__(this, newmap):
		#~ print "Setting"
		#~ this.size = len(newmap), len(newmap[0])
		#~ if type(newmap[0][0]) == str:
			#~ this.map = this.charmap
			#~ for y in range(len(this.charmap)):
				#~ for x in range(len(this.charmap[y])):
					#~ this.map[y][x] = Type.conv(this.charmap[y][x])
		#~ else:
			#~ this.map = newmap
			#~ this.charmap = newmap
			#~ for y in range(len(this.charmap)):
				#~ for x in range(len(this.charmap[y])):
					#~ this.charmap[y][x] = Type.char(this.map[y][x])
	
	@property
	def mapsize(this):
		""" Returns the size of the world in pixels (not the grid) """
		return (this.size[0]*Tile.size[0],this.size[1]*Tile.size[1])
	
	def new(this, size, char='.'):
		"""
		Creates a new map filled with the character [char]
		"""
		this.size = size
		
		this.map = []
		for y in range(size[1]):
			this.map.append([Tile(char, (x,y)) for x in range(size[0])])
			
		this = map
	
	def load(this, mapfile):
		try:
		  fr = open(mapfile, "r")
		except IOError as e:
		   print 'Error: file %s not found' % mapfile
		   return False
		
		this.name = mapfile
		
		# read in map file
		lines = fr.readlines()
		map = []
		for line in lines:
			map.append(line.strip('\n').strip('\r'))
		
		# make sure the map dimensions are correct
		for i in range(1,len(map)):
			if len(map[i]) != len(map[i-1]):
				print "Error: invalid map format detected"
				fr.close()
				return False
		
		# store dimensions
		this.size = (len(map[0]), len(map))
		
		# Create 2D array of Tile class
		for y in range(this.size[1]):
			this.map.append([])
			for x in range(this.size[0]):
				this.map[y].append(Tile(map[y][x], (x,y)))
				# this.map # What was i gonna do again...
			
		
		
		fr.close()
		return True
	
	def save(this):
		fw = open(this.name, "w")
		
		for y in range(len(this.map)):
			for x in range(len(this.map[y])):
				fw.write(str(this.map[y][x]))
			fw.write("\n")
	
	def tile(this, points, type):
		for p in points:
			this.map[p[1]][p[0]].type = type
	
	def place(this, points, objs):
		"""
		points - an array of coordinates
		objs - an array of the objects 
		"""
		for i in range(len(objs)):
			if this.map[points[i][1]][points[i][0]] == None:
				raise TypeError("Tile on map has not been set")
			
			this.map[points[i][1]][points[i][0]].contains.append(objs[i]) #ATTN: NEED TO ADD ITEM
				
	
	def renderMap(this):
		"""
		renderMap() : pygame.Surface
		Blits all the tiles onto a surface and returns it
		- This function is obsolete -
		"""
		this.image = pygame.Surface((this.size[0] * Tile.size[0], this.size[1]*Tile.size[1]))
		for y in range(this.size[1]):
			for x in range(this.size[0]):
				this.image.blit(this.map[y][x].image, this.map[y][x].maploc)
		
		return this.image
	
	def draw(this, surface, camera):
		"""
		Draws this map onto the surface
		"""
		
		# Calculate the approximate visible area - this saved 30% cpu
		startx = camera.rect.left / Tile.size[0]
		starty = camera.rect.top / Tile.size[1]
		endx = camera.rect.right / Tile.size[0]
		endy = camera.rect.bottom/ Tile.size[1]
		
		
		for y in range(starty, endy+1):
			for x in range(startx, endx+1):
				this.map[y][x].draw(surface, camera)
		
		
		
	## Some functions for world generation ##
	def onBound(this, loc):
		if loc[0] == 0 or loc[1] == 0:
			return True
		if loc[0] == this.size[0]-1 or loc[1] == this.size[1]-1:
			return True
		return False
	def outBound(this, loc):
		if loc[0] < 0 or loc[1] < 0:
			return True
		if loc[0] >= this.size[0] or loc[1] >= this.size[1]:
			return True
		return False
