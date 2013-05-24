# this class actually only needs pygame.surface and blitting for rendering purposes
# it only needs to render the map each time a new map is loaded
#~ import pygame, os
#~ from pygame.locals import * 

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
	def __init__(this):
		this.size = (0,0)
		this.map = []
		this.charmap = []
		this.image = None
	
	# Override the [] operation
	def __getitem__(this, index):
		print "getting index"
		if type(index) != int:
			x,y = index
			return map[y][x]
		else:
			return this.map[index]
	
	# Override = operator
	def __set__(this, newmap):
		print "Setting"
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
	
		
	
	def new(this, size, char='.'):
		"""
		Creates a new map filled with the character [char]
		"""
		this.size = size
		
		this.map = []
		this.charmap = []
		for y in range(size[1]):
			this.charmap.append([char for x in range(size[0])])
			this.map.append([charToTile(char) for x in range(size[0])])
			
		this = map
	
	def load(this, mapfile):
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
					# this.map # What was i gonna do again...
			
		except:
			print "Error: unknown error while loading map file"
			return False
			
		return True
	
	def save(this, mapfile):
		fw = open(mapfile, "w")
		
		for y in range(len(this.charmap)):
			for x in range(len(this.charmap[y])):
				fw.write(this.charmap[y][x])
			fw.write("\n")
		
	
	def dig(this, points):
		"""
		This function digs out all the locations given in [points]
		"""
		#print points
		for p in points:
			#print p
			try:
				this.map[p[1]][p[0]] = Type.Floor
				this.charmap[p[1]][p[0]] = '.'
			except:
				print "Error: ",len(this.map)
				return
	
	def place(this, points, obj):
		"""
		This function places [obj] at [points]
		"""
		for p in points:
			if type(obj) == str:
				this.map[p[1]][p[0]] = Type.conv(obj)
				this.charmap[p[1]][p[0]] = obj
			else:
				this.map[p[1]][p[0]] = obj
				this.charmap[p[1]][p[0]] = Type.char(obj)
				
	
	#~ def renderMap(this):
		#~ """
		#~ renderMap() : pygame.Surface
		#~ Blits all the tiles onto a surface and returns it
		#~ """
		#~ this.image = pygame.Surface((this.size[0] * Tile.size[0], this.size[1]*Tile.size[1]))
		#~ for y in range(this.size[1]):
			#~ for x in range(this.size[0]):
				#~ map[y][x].image.blit(this.image, map[y][x].maploc)
		#~ 
		#~ return this.image
		
		
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
