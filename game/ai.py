#~ import math


directions = {"up":[0,-1], "down":[0,1], "left":[-1,0], "right":[1,0], "none":[0,0]}


def distance(a, b):
	"""
	Calculates the distance between point a and point b
	"""
	return ((b[0] - a[0]), (b[1] - a[1]))


def unitVect(v):
	"""
	Converts a position/vector into -1,0, or 1
	e.g. (-3,5) turns into (-1,1)
	"""
	ret = [0,0]
	if v[0] != 0: v[0] = -1 if v[0] < 0 else 1
	if v[1] != 0: v[1] = -1 if v[1] < 0 else 1
		
	return ret


	
def move(loc, dir):
	nloc = list(loc)
	#print nloc
	nloc[0] += directions[dir][0]
	nloc[1] += directions[dir][1]
	return tuple(nloc)

class AI(object):
	"""
	This AI class is designed to guide a monster
	to its target (the player) while performing certain
	characteristic behaviours (e.g. wandaring when player not in view)
	"""
	
	def __init__(this, body):
		# body is the owner of this AI
		this.body = body
		
		# Store a reference to the world state (required for pathfinding)
		this.world = body.world
		
		# When this is true, the monster goes into an aggresive state
		this.lockedOn = False

	
	def nextStep(this):
		"""
		This function returns the direction of the next step to take.
		Intended to be used with the move() function in Sprite.
		"""
		
		# Check if target is in range
		# If it isn't don't need to move monster
		dx,dy = distance(this.body.tile.gridloc, this.body.world.player.tile.gridloc)
		if abs(dx) + abs(dy) > this.body.sight:
			return "none"
		
		# Check which tile to move to 
		lowest = [this.body.sight + 1, "none"]
		for d in directions:
			if d == "none":
				continue
			loc = move(this.body.tile.gridloc, d)
			tile = this.world.map[loc[1]][loc[0]]
			if tile.type == 1 or tile.getMonster() != None:
				continue
			if tile.distance < lowest[0]:
				lowest = [tile.distance, d]
		
		# Player out of range
		return lowest[1]
		
