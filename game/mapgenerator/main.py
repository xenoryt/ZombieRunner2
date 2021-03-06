#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2013 Tyrone Xiong <xenoryt@xenobang>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# Only tested to run on python 2.7

#~ import pygame, sys
#~ from pygame.locals import *

#~ from game import Game
import mapgenerator
from mapgenerator import MapGenerator
#~ import tile
#~ from tile import *5

#~ class testState(Game.State):
	#~ def update(this):
		#~ # you can never be too safe
		#~ if not isCurrent:
			#~ Game.Error("Updating an inactive state")
			#~ 
		#~ 

def main():
	worldgenerator = MapGenerator()
	i = 0
	for i in range(4):
		worldgenerator.create("map"+str(i)+".txt", (80,80), 7)
	
	return 0

if __name__ == '__main__':
	main()

