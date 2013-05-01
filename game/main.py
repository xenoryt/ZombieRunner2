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

from game import *
import mapgenerator
from mapgenerator import MapGenerator
#~ import tile
#~ from tile import *5

class testState(Game.State):
	def __init__(this):
		this.isCurrent = False
		
	def update(this):
		# you can never be too safe
		if not this.isCurrent:
			game.Error("Updating an inactive state")
			raise ValueError
		
		# Get input
		for event in pygame.event.get():
			if event.type == QUIT:
				game.running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					game.running = False
				elif event.key == K_1:
					game.msgbox()
					
	def draw(this,screen):
		# Fill background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))
		
		# Display some text
		font = pygame.font.Font(None, 36)
		text = font.render("Hello There", 1, (10, 10, 10))
		textpos = text.get_rect()
		textpos.centerx = background.get_rect().centerx
		background.blit(text, textpos)

		# Blit everything to the screen
		screen.blit(background, (0, 0))
		pygame.display.flip()
			
		

def main():
	#~ worldgenerator = MapGenerator()
	#~ world = worldgenerator.create("map.txt", (120,120), 7)
	
	game.run(testState)
	
	return 0

if __name__ == '__main__':
	main()

