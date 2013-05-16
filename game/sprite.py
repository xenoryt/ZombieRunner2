import pygame


class Sprite(pygame.sprite.Sprite):
	def __init__(this):
		pygame.sprite.Sprite.__init__(this, this.groups)
		this.image = None
		this.rect = None
		
		# This var sets the radius of the area that is lit up 
		# around this sprite
		this.brightness = 0
		
		# Stats
		this.hp = 0
		this.def = 0
		this.atk = 0
		this.str = 0
