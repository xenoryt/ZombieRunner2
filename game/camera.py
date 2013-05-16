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
