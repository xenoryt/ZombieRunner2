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
		
		# buffs for the player when equipped
		this.atk = 0
		this.blk = 0
		this.str = 0
		this.dex = 0
		this.int = 0
		
		this.heal = 0
		
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
	shp.heal = 25
	
	rock = Item(itemType.throw, 1, "Pebble", "How rare...")
	rock.atk = 1
	rock.canTarget = True
		
	csword = Item(itemType.wpn, 50, "Cracked Sword", 
								"It looks like it may break anytime now")
	csword.atk = 5
	
	sword = Item(itemType.wpn, 72,  "Sword", "Ordinary sword")
	sword.atk = 12
	sword.str = 1
	
	
	return items
