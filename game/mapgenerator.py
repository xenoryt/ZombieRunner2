import tile, world
from tile import *
from world import *
import math

import random


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
		
	def generate(this, world, areas, cors, loc, dir):
		"""
		A recursive function to connect the rooms together.
		world 	- a World object. 
		areas 	- a list of all the rooms
		cors	- a list of all the corridors
		loc		- current location of corridor
		dir		- direction in which the corridor should generate
		
		Returns a bool representing whether or not the corridor connected
		to another room. 
		
		The corridor's endroom may contain the same room more than once.
		You will need to remove duplicates after generating corridor.
		This generation does not automatically put this corridor
		inside the room's array of corridors (in case this generation
		fails).
		""" 
		
		if world.onBound(loc): 
			# This may happen if it starts directly on boundary
			return False
		
		if loc not in this.points:
			this.points.append(loc)
		
		# Check if this corridor is connected to an isolated room
		for area in areas:
			# if the current position of the corridor is on the
			# wall of a room
			if area in this.endrooms:
				continue
			if loc in map(lambda x: x[0], area.walls):
				# Mark the room as connected
				#area.corridors.append(this)
				this.endpoints.append(loc)
				this.endrooms.append(area)
				
				# If this room does not have any other corridors connected
				if len(area.corridors) <= 2:
					return True # end corridor generation
		
		for cor in cors:
			if this is cor:
				continue # why check if you are connected to yourself?
			if cor.has(loc):
				this.endpoints.append(loc)
				this.endrooms += cor.endrooms
				#for area in cor.endrooms:
				#	area.corridors.append(this)
				
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
				# and does not go off the world
				d = random.choice(directions.keys())
				if move(loc, d) == rmove(loc,dir):
					continue
				if world.onBound(move(loc,d)):
					continue
				break
		
		# recursively dig a corridor
		return this.generate(world, areas, cors, move(loc, d), d)
	
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
	
	def isOverlap(this, area):
		"""
		Checks if this area overlaps with the given area
		"""
		if area is this:
			return False
		for point in this.points:
			if area.has(point):
				return True
		return False
	
	def getConnectedRooms(this, connected = []):
		"""
		Returns a list of rooms that this room is directly and
		indirectly connected to
		"""
		
		if connected == []:
			connected.append(this)
		
		for hall in this.corridors:
			for endroom in hall.endrooms:
				if endroom not in connected:
					connected += endroom.getConnectedRooms(connected + [endroom])
		
		return connected
		
	
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
	
	def create(this, mapname, size = (64,64), density=5):
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
		# 	- It only stops when it reaches a room or another corridor
		# 	- It is theoretically possible for the entire map
		# 	  to be one corridor
		# 5) Check if all rooms are connected
		#	- If not, redo map entire generation process from start
		# 6) Write all these points into the world as floors
		# 7) Place random objects throughout the map
		# 8) Write again and save
		#############################################################
		
		
		# Generate a new world filled with only walls
		world = World()
		world.new((64,64), '#')
		
		# Create lists of rooms, corridors and points of the map
		# that are no longer occupied by a wall (aka "dug out")
		rooms = []
		halls = []
		cleared = [] # locations that have been dug out
		
		# Calculate number of rooms based on map size and difficulty
		#avgHeight = 
		roomCount = int(math.ceil(((world.size[1]-2)*(world.size[0]-2) / (this.avgRoomSize[0]*this.avgRoomSize[1])) * (density*0.65+1)/12))
		
		# Make sure the number of rooms is even
		# (Algorithm fails if it isnt...)
		if roomCount % 2 != 0:
			roomCount + 1
		
		# This infinite while loop is here to repeat the map generation
		# process in case an "invalid" map has been generated
		while True:
			# clear any old data
			del rooms[:]
			del halls[:]
			del cleared[:]
			
			#~ print len(rooms)
			#~ print len(halls)
			#~ print len(cleared)
			
			# Create rooms (areas) 
			for i in range(roomCount):
				# Generate a new room
				area = Area()
				loc = (random.randint(1,world.size[0]-this.avgRoomSize[0]-4), random.randint(1,world.size[1]-this.avgRoomSize[1]-4))
				size = (random.randint(this.avgRoomSize[0]-3, this.avgRoomSize[0]+3), random.randint(this.avgRoomSize[1]-3, this.avgRoomSize[1]+3))
				area.create(loc, size)
				
				# Add the new room to the list of rooms
				rooms.append(area)
			
				# add the all the locations the room occupies to [cleared]
				cleared += area.points
			
			# Remove duplicates from the tuple of cleared areas
			# This is also performed again later, but cleared will
			# be accessed a lot. Clearing duplicates now will save cpu
			cleared[:] = list(set(cleared))
			
			
			
			# After generating rooms, merge rooms that are connected to each other
			i = 0
			while i < len(rooms):
				# n = i + 1 because all the rooms before i have already been checked
				n = i+1
				while n < len(rooms):
					if rooms[i].isOverlap(rooms[n]):
						# Merge the two rooms
						rooms[i].merge(rooms[n])
						
						# Remove the second room (room[n]) since that one
						# is now a part of the current room (room[i])
						rooms.pop(n)
						
						# Recheck the current room with the rest again
						n = i
						continue
					n+=1
				i+=1
			
			# Calculate locations of walls for each room
			for r in rooms:
				r.calcWalls(cleared)
			
			# Now connect rooms via corridors
			for i in range(len(rooms)):
				if len(rooms[i].corridors) == 0:
					while True:
						hall = Corridor()
						loc, d = random.choice(rooms[i].walls)
						
						hall.endrooms.append(rooms[i])
						
						# if this hall generated properly
						if hall.generate(world, rooms, halls, loc, d):
							# Add this corridor to all the rooms
							# it connected to
							for room in hall.endrooms:
								room.corridors.append(hall)
							break # exit
											
					hall.endrooms[:] = list(set(hall.endrooms))
					
					# Appened corridors to cleared areas
					cleared += hall.points
			print "out"
			# Remove duplicates from the tuple of cleared areas
			cleared[:] = list(set(cleared))
			
			# Check if all the rooms are connected
			connected = rooms[0].getConnectedRooms()
			connected[:] = list(set(connected))
			print len(connected),"is connected"
			print len(rooms),"were generated"
			if len(connected) < len(rooms):
				print "Invalid map detected\nRegenerating..."
				del connected[:]
				continue
			elif len(connected) > len(rooms):
				print "Something is wrong here..."
				raise ValueError
			
			
			# dig out rooms and corridors
			world.dig(cleared)
			
			## Randomly place objects and monsters ##
			# TODO: create a way to calculate how many of each object to place
			
			nchests = 3
			nlowlvl = 9
			nhighlvl = 2
			nportal = 1
			nplayer = 1
			
			
			
			# Place objects and monsters
			break
			
		world.save(mapname)
		return world
