from pygame import Rect
import copy

class Camera(object):
	def __init__(this, screensize, x=0,y=0):
		this.rect = Rect(x,y, screensize[0], screensize[1])
	
	def getrect(this,spriterect):
		"""
		Returns a rect that has been modified to be relative to
		the camera
		"""
		
		rect = copy.copy(spriterect)
		rect.left -= this.rect.left
		rect.top -= this.rect.top
		return rect
	
	def clip(this, world):
		if this.rect.bottom > world.mapsize[1]:
			this.rect.bottom = world.mapsize[1]
		elif this.rect.top < 0:
			this.rect.top = 0
		
		if this.rect.right > world.mapsize[0]:
			this.rect.right = world.mapsize[0]
		elif this.rect.left < 0:
			this.rect.left = 0
	
