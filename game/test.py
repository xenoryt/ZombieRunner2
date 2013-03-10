
class t(object):
	def __init__(self):
		self._s = ""
	
	@property
	def s(this):
		this._s
	
	@s.setter
	def s(this, a):
		print "test: ",a
		this._s = a
	
	def write(this):
		print "printing",this._s
		

a = t()
a.s = 2

print a.write()
