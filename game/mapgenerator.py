import tile, world
from tile import *


class MapGenerator:
	"""
	This is a singleton.
	This class is used to create and load maps
	in the form of a 2D array of characters. The characters
	used will match the character representation used by the Type
	class (in tile.py).
	"""
	
	
	
	
	def load(this, mapname):
		raise NotImplementedError
	
	def create(this, mapname, size = (64,64)):
		"""
		Generates a dungeon and saves it in a file called
		"mapname.map". 
		Returns a World object.
		"""
		
		world = World()
		world.new(64,64, '#')
		
		
	
	
