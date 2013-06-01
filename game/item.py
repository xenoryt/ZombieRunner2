items = [[] for i in range(10)]
nullitem = None

class Item(object):
	# This variable is static (same across all class instances
	_curID = 0 
	
	def __init__(this, lvlrange, type = 0, name = "", desc = ""): #initializer
		# Item descriptions
		this.Type = type
		this.Name = name
		this.Description = desc
		
		# Item settings
		this.lvl = {}
		
		# automatically set the ID
		this.ID = this.__class__._curID
		this.__class__._curID += 1
		
		# A dictionary for status buffs/debuffs
		# e.g. "hp":20 to increase hp by 20 or 
		# "atk":-10 to decrease attack by 10
		this.attributes = {}
		
		for lvl in lvlrange:
			items[lvl-1].append(this)
	
	def __str__(this):
		atts = ""
		for k in this.attributes.keys():
			plus = "+" if this.attributes[k] >= 0 else ""
			atts += k + ": " + plus+str(this.attributes[k]) + "\n"
		
		# atts[:len(atts)-1] is to remove the last \n
		return this.Name + "\n" + this.Description+"\n"+atts[:len(atts)-1]

def getItem(itemid):
	for n in range(10):
		for item in items[n]:
			if itemid == item.ID:
				return item
	return nullitem
	
	
# "Enumerator" of item types
class itemType():
	item, consumable, weapon = range(3)

def CreateItemList():
	""" 
	This function creates all the items in the game and
	returns a list of all the items.
	This function only needs to be called once.
	"""
	
	# Items will automatically be placed into the global
	# items list upon initializing
	global nullitem
	nullitem = Item([], itemType.item)
	
	shp = Item([1,2,3], itemType.consumable, "Small HP Potion", "Heals a bit of your HP")
	shp.attributes = {"heal": 10}
	mhp = Item([3,4,5], itemType.consumable, "Medium HP Potion", "Heals a decent amount of HP")
	mhp.attributes = {"heal":20}
	lhp = Item([5,6,7,8,9,10],itemType.consumable, "Large HP Potion", "Heals a Large amount of HP")
	lhp.attributes = {"heal":40}
	lhp = Item([10], itemType.consumable, "Extra Large HP Potion", "Heals very large amount of HP")
	lhp.attributes = {"heal":65}
	
	rock = Item([1,2,3,4,5,6], itemType.item, "Pebble", "How rare...")
	rock.canTarget = True
	
	stick = Item([1], itemType.weapon, "Cypress Stick", "Used to get out of sticky situations")
	stick.attributes = {"atk":1}
		
	csword = Item([2,3], itemType.weapon, "Cracked Sword", 
								"It looks like it may break anytime now")
	csword.attributes = {"atk":3}
	
	sword = Item([3,4], itemType.weapon, "Sword", "An ordinary sword")
	sword.attributes = {"atk":5}
	
	rsword = Item([4,5], itemType.weapon, "Refined Sword", "Ooooh! Shiny!")
	rsword.attributes = {"atk":7}
	
	gsword = Item([5,6], itemType.weapon, "Great Sword", "A sword that has been through many battles")
	gsword.attributes = {"atk":10, "hp":15}
	
	knife = Item([5,6], itemType.weapon, "Kitchen Knife", "Great for cooking and assassination!")
	knife.attributes = {"atk":5, "spd":0.15}
	
	sspd = Item([6,7], itemType.weapon, "Sword of Speeed", "A magical sword that enhances your speed")
	sspd.attributes = {"atk":10, "hp":10, "spd":0.1}
	
	grass = Item([8,9,10], itemType.weapon, "Blade of Grass", "They say you can ever use it to whistle!")
	grass.attributes = {"atk":11, "hp":-25, "spd":0.4}
	
	muramasa=Item([1], itemType.weapon, "Muramasa", "The cursed Japenese katana")
	muramasa.attributes = {"atk":27, "hp":-20, "spd":0.15}
	
	hammer = Item([7,8,9], itemType.weapon, "Hammer", "Seems like a carpenter got lost...")
	hammer.attributes = {"atk":10, "hp":20, "spd":-0.1}
	
	thammer = Item([7,8,9], itemType.weapon, "Thor's Hammer", "A hammer used by Thor...\nHow did it end up here?")
	thammer.attributes = {"atk":28, "hp":80, "spd":-0.2}
	
	return items
