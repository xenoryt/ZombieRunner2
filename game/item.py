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
	
	shp = Item(itemType.edible, "Small HP Potion", "Heals a bit of your HP")
	shp.attributes = {"heal": 10}
	mhp = Item(itemType.edible, "Medium HP Potion", "Heals a decent amount of HP")
	mhp.attributes = {"heal":30}
	lhp = Item(itemType.edible, "Large HP Potion", "Heals a Large amount of HP")
	lhp.attributes = {"heal":100}
	
	rock = Item(itemType.throw, "Pebble", "How rare...")
	rock.canTarget = True
	rock.attributes = {"atk":2,"rng":6}
	
	stick = Item(itemType.wpn, "Cypress Stick")
	stick.attributes = {"atk":2}	
		
	csword = Item(itemType.wpn, "Cracked Sword", 
								"It looks like it may break anytime now")
	csword.attributes = {"atk":5}
	
	sword = Item(itemType.wpn, "Sword", "Ordinary sword")
	sword.attributes = {"atk":12, "str":1}
	
	gsword = Item(itemType.wpn, "Great Sword", "A sword that has been through many battles")
	gsword.attributes = {"atk":20, "hp":25, "agi":-2}
	
	requiem = Item(itemType.wpn, "Requiem", "A light sword with a glowing aura around it")
	requiem.attributes = {"atk":35, "str":3, "agi":6}
	
	thammer = Item(itemType.wpn, "Thor's Hammer", "A hammer used by Thor. How did it end up here?")
	thammer.attributes = {"atk":50, "hp":40, "str":6, "agi":-10}
	
	return items
