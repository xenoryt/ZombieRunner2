import tile, world
from tile import *
from world import *
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
	nloc = list(loc) # make nloc a list of loc
	nloc[0] += directions[dir][0]
	nloc[1] += directions[dir][1]
	return tuple(nloc)
	
def rmove(loc, dir):
	""" Similar to move(), but moves in opposite direction) """
	nloc = list(loc)
	nloc[0] += directions[dir][0]*-1
	nloc[1] += directions[dir][1]*-1
	return tuple(nloc)

class Corridor:
	def __init__(this):
		this.endpoints = [] #endpoints are connected to rooms or corridors
		this.endrooms = [] 
		this.points = []
		
	def generate(this, map, areas, cors, loc, dir):
		"""
		A recursive function to connect the rooms together.
		map 	- a World object. 
		areas 	- a list of all the rooms
		cors	- a list of all the corridors
		loc		- current location of corridor
		dir		- direction in which the corridor should generate
		
		Returns a bool representing whether or not the corridor connected
		to another room. 
		""" 
		if map.onBound(loc): 
			# This may happen if it starts directly on boundary
			return False
		
		if loc not in this.points: # NOTE: may be inefficient (try using set())
			this.points.append(loc)
		
		# Check if this corridor is connected to a room
		for area in areas:
			if len(area.corridors) > 0:
				continue
			if loc in area.walls:
				area.corridors.append(this)
				this.endpoints.append(loc)
				this.endrooms.append(area)
				return True
		
		for cor in cors:
			if this is cor:
				continue # if it ran into itself...
			if cor.has(loc):
				this.endpoints.append(loc)
				this.endrooms += cor.endrooms
				for area in cor.endrooms:
					area.corridors.append(this)
				
				# if this corridor collides into another corridor
				# include a chance of stopping the construction of 
				# this corridor
				if random.randint(0,1) == 0:
					return True # stop
				# else it continues
		
		## Make corridor move generally in a straight line
		d = dir 
		
		# Give 1/4 chance of turning
		if (random.randint(0,4) == 0):
			while True: 
				# This loops until the corridor goes in any direction
				# that is not backwards
				# and does not go off the map
				d = random.choice(directions.keys())
				if move(loc, d) == rmove(loc,dir):
					continue
				if map.onBound(move(loc,d)):
					continue
				break
		
		# recursively dig a corridor
		return this.generate(map, areas, cors, move(loc, d), d)
	
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
		
		this.points = []
		this.loc = loc
		this.corridors = []
		this.walls = []
	
	def create(this,loc = [0,0], size=[0,0]):
		"""
		"Creates" an area based on specifications
		Also calculates the location of walls
		"""
		this.points = [(x,y) for x in range(loc[0],size[0]+loc[0]) for y in range(loc[1], size[1]+loc[1])]

	def calcWalls(this, cleared):
		""" 
		Calculates the location of walls given the points
		occupied by rooms.
		It stores the walls and the direction towards the outside
		of the room inside this.walls
		"""
		for point in this.points:
			for d in directions.keys():
				if move(point, d) not in cleared:
					this.walls.append((move(point, d), d))
					break
	
	def has(this, point):
		if point in this.points:
			return True
		return False
	
	def isConnected(this, area):
		"""
		Checks if this area overlaps with the given area
		"""
		if area is this:
			return False
		for point in this.points:
			if area.has(point):
				return True
		return False
	
	def merge(this, area):
		# Merges two areas together
		this.points += area.points
		this.points = list(set(this.points)) # remove duplicates


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
	
	def create(this, mapname, size = (64,64), density=1):
		"""
		Generates a dungeon given a map size and room concentration. 
		The concentration ranges from 0 to 9, inclusively,
		with 0 being sparse and 9 being dense.
		Note that high density will result in more rooms/corridors 
		that will most likely overlap causing large open areas.
		Returns a World object.
		"""
		
		### A slightly more detailed description of the algorithm ###
		# 1) A blank world is generated and filled with walls
		# 2) Random rooms are generated 
		# 	- Note that the rooms are not written yet
		# 	- All the points the rooms cover are stored in memory
		# 	- Same with the corridors
		# 3) Merge any rooms that are generated on top of eachother
		# 4) Connect all the rooms with corridors
		# 	- Corridors are recursively generated (and can be buggy)
		# 	- The corridor generation is completely random
		# 	- It only stops when it reaches a room
		# 	- It is theoretically possible for the entire map
		# 	  to be one corridor
		# 5) Write all these points into the world as floors
		# 6) Place random objects throughout the map
		# 7) Write again and save
		#############################################################
		
		world = World()
		world.new((64,64), '#')
		
		# Calculate number of rooms based on map size and difficulty
		#avgHeight = 
		roomCount = int(math.ceil(((world.size[1]-2)*(world.size[0]-2) / (this.avgRoomSize[0]*this.avgRoomSize[1])) * (density*0.65+1)/12))
		
		# Make sure the number of rooms is even
		# (Algorithm fails if it isnt...)
		if roomCount % 2 != 0:
			roomCount + 1
		
		# Create rooms (areas) 
		rooms = []
		halls = []
		cleared = [] # locations that have been dug out
		
		for i in range(roomCount):
			#generate an area
			area = Area()
			loc = (random.randint(1,world.size[0]-this.avgRoomSize[0]-3), random.randint(1,world.size[1]-this.avgRoomSize[1]-3))
			size = (random.randint(this.avgRoomSize[0]-3, this.avgRoomSize[0]+3), random.randint(this.avgRoomSize[1]-3, this.avgRoomSize[1]+3))
			area.create(loc, size)
			
			rooms.append(area)
		
			# add the points in the area to cleared
			cleared += area.points
		
		# Remove duplicates from the tuple of cleared areas
		# This is also performed again later, but cleared will
		# be accessed a lot. Clearing duplicates now will save cpu
		cleared = list(set(cleared))
		
		# Calculate locations of walls for each room
		for r in rooms:
			r.calcWalls(cleared)
		
		# After generating rooms, merge rooms that are connected to each other
		i = 0
		while i < len(rooms):
			n = 0
			while n < len(rooms):
				if rooms[i].isConnected(rooms[n]):
					rooms[i].merge(rooms[n])
					rooms.pop(n)
				n+=1
			i+=1
		
		
		# Now connect rooms via corridors
		for i in range(len(rooms)):
			if len(rooms[i].corridors) == 0:
				hall = Corridor()
				loc, d = random.choice(rooms[i].walls)
				
				# Start generating
				hall.generate(world, rooms, halls, loc, d) # Prepare for crashes
				
				# Appened corridors to cleared areas
				cleared += hall.points
		
		# Remove duplicates from the tuple of cleared areas
		cleared = list(set(cleared))
		
		# dig out rooms and corridors
		world.dig(cleared)
		
		## Randomly place objects and monsters ##
		
		
		# Place objects and monsters
		
		world.save(mapname)
		return world
