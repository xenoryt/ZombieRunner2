#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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


import pygame, sys
from pygame.locals import *

import gui, world, units

SCRSIZE = pygame.Rect(0,0, 800,600)
DEFAULTFULLSCR = 0

def init(winsize, fullscreen):
	"""Initializes pygame and the game window"""
	
	#init pygame
	pygame.init()
	
	#set window caption
	pygame.display.set_caption("RTS Game")
	
	#set the screen modes
	winstyle = FULLSCREEN if fullscreen == 1 else 0
	bestdepth = pygame.display.mode_ok(winsize.size, winstyle, 32)
	screen = pygame.display.set_mode(winsize.size,winstyle, bestdepth)
	
	return screen
	
	



def main(screen):
	
	
	#setup groups
	all = pygame.sprite.LayeredUpdates()
	ctrls = pygame.sprite.RenderUpdates()
	
	gui.Control.containers = all, ctrls
	
	
	btn = gui.Button(30,40,50,50)
	btn.moveip(100,-1)
	btn.resize(150,60)
	btn.text = "hi"
	btn.update()
	
	screen.fill(Color('red'))
	pygame.display.flip()
	
	surface = pygame.Surface((50,50))
	surface.fill(Color('white'))
	surface.blit(screen, (40,50))
	pygame.display.flip()
	
	print all
	running = True	
	while running:
		
		## Event handling ##
		events = pygame.event.get()
		for e in events:
			if e.type == QUIT:
				running = False
				break
			if e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					running = False
					break
				elif e.key == K_F11:
					pygame.display.toggle_fullscreen()
				elif e.key == K_a:
					gui.Button()
		
		
		#all.clear(screen, Color('red'))
		
		#btn.draw(screen)
		btn.update()
		#draw sprites
		dirty = all.draw(screen)
		pygame.display.update(dirty)
		#pygame.display.flip()
		#limit frames per second
		clock.tick(60)
	
	print all
	
	#exit
	pygame.quit()
	return 0

if __name__ == '__main__':
	print "argv:",sys.argv
	size = SCRSIZE
	fullscr = DEFAULTFULLSCR
	for i in range(1,len(sys.argv)):
		if sys.argv[i] == '-s':
			size.w = sys.argv[i+1]
			size.h = sys.argv[i+2]
		elif sys.argv[i] == '-f':
			fullscr = int(sys.argv[i+1])
	
	#initialize everything
	screen = init(size, fullscr)
	
	#enter main function
	main(screen)

