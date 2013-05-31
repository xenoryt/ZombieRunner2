# this class actually only needs pygame.surface and blitting for rendering purposes
# it only needs to render the map each time a new map is loaded
import pygame, os
from pygame.locals import * 

import tile
from tile import *
import item

import sprite

class World:
	"""
	A class that stores all the information about a single map.
	It is capable of loading a new map from a file and can also
	create a new blank map given a size.
	Individual tiles of the map can be accessed through [x, y]
	or through [y][x].
	"""
	
	# Constructor
	def __init__(this, name = "map", level = 1):
		# the size of the grid
		# the size of the map is a property defined later on
		this.size = (0,0)
		
		this.map = []
		this.image = None
		this.name = name
		
		# if the map has been successfully loaded this is set to True
		this.loaded = False
		
		this.level = level
		
		# List of all the objects in the game
		this.objects = []
		
		# List of all the monsters in the world
		this.monsters = []
		
		# The main player
		this.player = None
		
		# The exit
		this.staircase = None
		
		# A dictionary of item id's and the amount the player is carrying
		this.inventory = [item.nullitem for i in range(32)]
		
		# this array stores a list of tiles that have been "marked"
		# marked tiles are used by monsters to pathfind the shortest 
		# path to the player. These tiles have their .distance value
		# set a value other than -1 and need to be reset when the 
		# player moves.
		this.markedtiles = []
	
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
	
	def load(this, mapname):
		try:
		  fr = open(mapname + ".txt", "r")
		except IOError as e:
		   print 'Error: file %s not found' % (mapname + ".txt")
		   return False
		
		this.name = mapname
		
		# read in map file
		lines = fr.readlines()
		map = []
		for line in lines:
			map.append(line.strip('\n').strip('\r'))
		
		# make sure the map dimensions are correct
		for i in range(1,len(map)-1):
			if len(map[i]) != len(map[i-1]):
				print "Error: invalid map format detected"
				fr.close()
				return False
		
		# store dimensions
		this.size = (len(map[0]), len(map)-1)
		
		# Create 2D array of Tile class
		for y in range(this.size[1]):
			this.map.append([])
			for x in range(this.size[0]):
				this.map[y].append(Tile(map[y][x], (x,y)))
				# this.map # What was i gonna do again...
				
		# Set the dungeon level
		this.level = int(map[this.size[1]][0:])
		if this.level > 10:
			this.level = 10
		
		# Set list of items available for this dungeon level
		this.itemlist = item.items[this.level-1]
		
		fr.close()
		
		try:
			fr = open(this.name + "_objects.txt", "r")
		except IOError as e:
			print 'Error: file %s not found' % (mapname + "_objects.txt")
			return False
		
		# Delete previous references to objects if there were any
		del this.monsters
		del this.player
		this.monsters = []
		lines = fr.readlines()
		for i in range(len(lines)):
			line = lines[i].split(' ')
			
			# The objects file should follow the following format
			# <ObjectType> <LocX> <LocY>
			locx = int(line[1])
			locy = int(line[2])
			
			this.placeObject(line[0], locx, locy, int(line[3]))
		
		fr.close()
		
		if not this.loadInventory():
			return False
		if not this.loadExplored():
			return False
		
		this.loaded = True
		return True
	
	def placeObject(this, name, locx, locy, hp = -1):
		"""
		Places objects such as players, monsters and chests at the 
		specified grid location.
		"""
		if name == "chest":
			chest = sprite.Chest(this.level, this)
			chest.rect.topleft = (locx*48, locy*48)
			chest.tile = this.map[locy][locx]
			this.objects.append(chest)
		if name == "stair":
			stair = sprite.Stair(this.level, this)
			stair.rect.topleft = (locx*48, locy*48)
			stair.tile = this.map[locy][locx]
			this.objects.append(stair)
			print stair.tile, this.map[locy][locx].contains
		if name == "player":
			this.player = sprite.Sprite(this)
			this.player.rect.topleft = (locx*48, locy*48)
			this.player.tile = this.map[locy][locx]
			if hp != -1:
				this.player.hp = hp
		if name == "monster":
			m = sprite.Monster(this.level, this)
			m.rect.topleft = (locx*48, locy*48)
			m.tile = this.map[locy][locx]
			if hp != -1:
				m.hp = hp
			this.monsters.append(m)
		if name == "bat":
			m = sprite.Bat(this.level, this)
			m.rect.topleft = (locx*48, locy*48)
			m.tile = this.map[locy][locx]
			if hp != -1:
				m.hp = hp
			this.monsters.append(m)
		if name == "skel":
			m = sprite.Skel(this.level, this)
			m.rect.topleft = (locx*48, locy*48)
			m.tile = this.map[locy][locx]
			if hp != -1:
				m.hp = hp
			this.monsters.append(m)
		if name == "reaper":
			m = sprite.Reaper(this.level, this)
			m.rect.topleft = (locx*48, locy*48)
			m.tile = this.map[locy][locx]
			if hp != -1:
				m.hp = hp
			this.monsters.append(m)
		if name == "dragon":
			m = sprite.Dragon(this.level, this)
			m.rect.topleft = (locx*48, locy*48)
			m.tile = this.map[locy][locx]
			if hp != -1:
				m.hp = hp
			this.monsters.append(m)
	
	def loadInventory(this):
		try:
			fr = open(this.name + "_inventory.txt", "r")
		except IOError as e:
			print 'Error: file %s not found' % (this.name + "_inventory.txt")
			return False
		
		# Load all the items in the inventory
		lines = fr.readlines()
		for i in range(len(lines)):
			# The inventory file should follow the following format
			# <ItemID>
			this.inventory.append(item.getItem(int(lines[i])))
		
		# Set rest of inventory to null; 32 is max inventory size
		for i in range(len(this.inventory), 32):
			this.inventory.append(item.nullitem)
		
		return True
	
	def loadExplored(this):
		try:
			fr = open(this.name + "_explored.txt", "r")
		except IOError as e:
			print 'Error: file %s not found' % (this.name + "_inventory.txt")
			return False
		
		lines = fr.readlines()
		for line in lines:
			data = line.split()
			loc = [int(data[0]), int(data[1])]
			this.map[loc[1]][loc[0]].explored = True
		
		return True
	
	def savemap(this):
		print this.name + ".txt"
		fw = open(this.name + ".txt", "w")
		
		for y in range(len(this.map)):
			for x in range(len(this.map[y])):
				fw.write(str(this.map[y][x]))
			fw.write("\n")
		fw.write(str(this.level)+"\n")
		fw.close()
	
	def save(this):
		fw = open(this.name + "_inventory.txt", "w")
		
		# Save inventory
		for item in this.inventory:
			fw.write(str(item.ID) +"\n")
		fw.close()
		fw = open(this.name + "_objects.txt", "w")
		
		# Write player data
		loc = str(this.player.tile.gridloc[0]) + " " + str(this.player.tile.gridloc[1])
		fw.write("player " +loc+" " +str(int(this.player.hp)) +"\n")
		
		# Write monster data
		for m in this.monsters:
			loc = str(m.tile.gridloc[0]) + " " + str(m.tile.gridloc[1])
			fw.write(m.name+" " + loc + " "+ str(m.hp) + '\n')
		
		for o in this.objects:
			loc = str(o.tile.gridloc[0]) + " " + str(o.tile.gridloc[1])
			fw.write(o.name+" " + loc + " 0" + '\n')
		
		#TODO: Write chest data
		
		
		fw.close()
		
		# Write areas that have been explored
		fw = open(this.name + "_explored.txt", "w")
		#ATTN: This is a TAD bit inefficient...
		for y in range(this.size[0]):
			for x in range(this.size[1]):
				if this.map[y][x].explored:
					fw.write(str(x) + " " + str(y) + '\n')
		fw.close()
	
	def terminate(this):
		"""
		Delete ALL save files related to this world
		"""
		
		print "terminating",this.name+".txt"
		if os.path.exists(this.name+".txt"):
			os.remove(this.name+".txt")
		if os.path.exists(this.name+"_inventory.txt"):
			os.remove(this.name+"_inventory.txt")
		if os.path.exists(this.name+"_objects.txt"):
			os.remove(this.name+"_objects.txt")
		if os.path.exists(this.name+"_explored.txt"):
			os.remove(this.name+"_explored.txt")
		this.loaded = False
		#~ os.remove(this.name+".txt")
	
	def tile(this, points, type):
		for p in points:
			this.map[p[1]][p[0]].type = type
			this.map[p[1]][p[0]].passable = True
	
	def place(this, points, objs):
		"""
		points - an array of coordinates
		objs - an array of the objects 
		"""
		for i in range(len(objs)):
			if this.map[points[i][1]][points[i][0]] == None:
				raise TypeError("Tile on map has not been set")
			
			this.map[points[i][1]][points[i][0]].contains.append(objs[i]) #ATTN: NEED TO ADD ITEM
				
	
	
	
	def draw(this, surface, camera, fog = True):
		"""
		Draws this map onto the surface
		"""
		
		# Calculate the approximate visible area - this saved 30% cpu
		startx = camera.rect.left / Tile.size[0]
		starty = camera.rect.top / Tile.size[1]
		endx = camera.rect.right / Tile.size[0]
		endy = camera.rect.bottom/ Tile.size[1]
		
		startx = 0 if startx < 0 else startx
		starty = 0 if starty < 0 else starty
		endx = this.size[0]-1 if endx > this.size[0]-1 else endx
		endy = this.size[1]-1 if endy > this.size[1]-1 else endy
				
		for y in range(starty, endy+1):
			for x in range(startx, endx+1):
				this.map[y][x].draw(surface, camera, fog)
		
		
		
		
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
