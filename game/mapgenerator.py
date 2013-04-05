import tile, world
from tile import *
import math

import random

#~ class Point:
	#~ def __init__(this, x = 0, y = 0):
		#~ this.x = 0
		#~ this.y = 0
	#~ 
	#~ def __getitem__(this, i):
		#~ if i == 0:
			#~ return this.x
		#~ elif i == 1:
			#~ return this.y
		#~ else:
			#~ raise IndexError
			
directions = {"up":[0,-1], "down":[0,1], "left":[-1,0], "right":[1,0]}

def move(loc, dir):
	pnt = loc[:]
	pnt[0] += directions[dir][0]
	pnt[1] += directions[dir][1]
	return pnt

class Corridor:
	def __init__(this):
		this.endpoints = [] #endpoints are connected to rooms or corridors
		this.endrooms = [] 
		this.points = []
		
	def generate(this, map, areas, cors, loc, prevloc):
		if map.onBound(loc):
			return False
		
		if loc not in this.points: # NOTE: may be inefficient 
			this.points.append(loc)
		
		# Check if this corridor is next to a room
		for k in directions.keys():
			tloc = move(loc, direction[k])
			for area in areas:
				if area.has(tloc):
					this.endpoints.append(tloc)
					this.endrooms.append(area)
					break
		
		for cor in cors:
			if this is cor:
				####
			if cor.has(loc):
				this.endpoints.append(loc)
				this.endrooms += cor.endrooms
				
				# if this corridor collides into another corridor
				# include a chance of stopping the construction of 
				# this corridor
				if random.randint(0,1) == 0:
					return True # stop
		
		## Move corridor in random direction
		dir = random.choice(directions.keys())
		while move(loc, dir) == prevloc: 
			# This loops until the corridor goes in any direction
			# that is not backwards
			dir = random.choice(directions.keys())
		
		# recursively dig a corridor
		this.generate(map, areas, cors, move(loc, dir), loc)
	
	def has(this, point):
		if point in this.points:
			return True
		return False

class Area:
	def __init__(this, loc = [0,0], size=[0,0]):
		""" 
		Stores a list of all the points within an area.
		It does not store a size (e.g. 45x30) to allow merging of
		rooms that are connected to eachother
		"""
		
		this.points = [[x,y] for x in range(loc[0],size[0]+loc[0]) for y in range(loc[1], size[1]+loc[1])]
		this.loc = loc
		this.corridors = []
	
	def has(this, point):
		if point in this.points:
			return True
		return False
	
	## TODO: Create merge() method ##
	def merge(this, area):
		this.points += area.points


class MapGenerator:
	"""
	This is a singleton.
	This class is used to create and load maps
	in the form of a 2D array of characters. The characters
	used will match the character representation used by the Type
	class (in tile.py).
	"""
	
	avgRoomSize = [7,7]
	
	def load(this, mapname):
		raise NotImplementedError
	
	def create(this, mapname, size = (64,64), density=0):
		"""
		Generates a dungeon given a map size and room concentration. 
		The concentration ranges from 0 to 9, inclusively,
		with 0 being sparse and 9 being dense.
		Note that high density will result in more rooms/corridors 
		that will most likely overlap causing large open areas.
		Returns a World object.
		"""
		
		world = World()
		world.new(64,64, '#')
		
		# Calculate number of rooms based on map size and difficulty
		avgHeight = 
		roomCount = math.ceil(((map.size[1]-2)*(map.size[0]-2) / (this.avgRoomSize[0]*this.avgRoomSize[1])) * (density*0.65+1)/12)
		
		
		# Create rooms (areas) 
		rooms = []
		
		
		#NOTE: after generating rooms, merge rooms that are connected to each other
		
	
