#~ import math


directions = {"up":[0,-1], "down":[0,1], "left":[-1,0], "right":[1,0]}


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

def route(world, loc, dest, maxsteps, steps = 0):
	"""
	This function recursively tries to route its way
	to the target destination. If the routing was successful,
	it returns the direction the sprite should head in.
	If it can't reach destination within a certain # of steps, 
	it returns None.
	"""
	
	# Check if max steps has been reached
	if steps >= maxsteps:
		return False, "none"
	
	# Check if target is in range
	dx,dy = distance(loc, dest)
	if abs(dx) + abs(dy) == 1 and steps + 1 < maxsteps:
		return True
	
	# If code reaches here, it means the target MAY be in range
	# Attempt to route to target 
	if abs(dx) > abs(dy):
		
	


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
		
	def checkTarget(this, target):
		dx,dy = distance(this.body.tile.gridloc, this.target.tile.gridloc)
		
		# If the target is out of sight
		if abs(dx) + abs(dy) > this.body.sight:
			return False
		
		# Target MAY be in sight
		# Check for obstacles
		
