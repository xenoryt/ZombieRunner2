
import math

avgRoomSize = 	[7,7]
size =			[64,64]
density = 		4

for density in range(10):
	print math.ceil(((size[1]-2)*(size[0]-2) / (avgRoomSize[0]*avgRoomSize[1])) * (density*0.65+1)/12)
