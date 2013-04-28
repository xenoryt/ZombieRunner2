items = []

class Item(object):
	# This variable is static (same across all class instances
	_curID = 0 
	
	def __init__(this, type = 0, weight = 0, name = "", desc = ""): #initializer
		# Item descriptions
		this.Type = type
		this.Name = name
		this.Description = desc
		this.weight = weight
		
		# Item settings
		this.canTarget = False
		this.canExplode = False
		
		
		# automatically set the ID
		this.ID = this.__class__._curID
		this.__class__._curID += 1
		
		# A dictionary for status buffs/debuffs
		# e.g. "hp":20 to increase hp by 20 or 
		# "atk":-10 to decrease attack by 10
		this.attributes = {"hp":0}
		
		items.append(this)
	
	def onThrow(this, target):
		pass # do nothing
	
	
	

# "Enumerator" of item types
class itemType():
	item, edible, throw, wpn, armor = range(5)

def CreateItemList():
	""" 
	This function creates all the items in the game and
	returns a list of all the items.
	This function only needs to be called once.
	"""
	
	# Items will automatically be placed into the global
	# items list upon initializing
	
	shp = Item(itemType.edible, 2, "Small HP Potion", "Heals a bit of your hp")
	shp.attributes = {"heal": 25}
	
	rock = Item(itemType.throw, 1, "Pebble", "How rare...")
	rock.canTarget = True
	rock.attributes = {"atk":2,"rng":6}
	
	stick = Item(itemType.wpn, 20, "Cypress Stick")
	stick.atk = 2
	
		
	csword = Item(itemType.wpn, 50, "Cracked Sword", 
								"It looks like it may break anytime now")
	csword.atk = 5
	
	sword = Item(itemType.wpn, 72,  "Sword", "Ordinary sword")
	sword.atk = 12
	sword.str = 1
	
	
	return items
