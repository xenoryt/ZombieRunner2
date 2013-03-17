import pygame, os
from pygame.locals import *

import tile
from tile import *

class World:
	def __init__(this):
		this.size = (0,0)
		this.map = []
		this.image = None
		
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
					print "Error: invalid map format!"
					return -1
			
			# store dimensions
			this.size = (len(map[0]), len(map))
			
			# Create 2D array of Tile class
			for y in range(this.size[1]):
				this.map.append([])
				for x in range(this.size[0]):
					this.map[y].append(Tile(map[y][x], (x,y)))
			
			
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
