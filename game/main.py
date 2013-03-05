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

DEFAULTSCRSIZE = [800,600]
DEFAULTFULLSCR = 0



def main(winsize = [DEFAULTSCRSIZE[0], DEFAULTSCRSIZE[1]], fullscreen = DEFAULTFULLSCR):
	
	pygame.init()
	
	winstyle = FULLSCREEN if fullscreen == 1 else 0
	bestdepth = pygame.display.mode_ok(winsize, winstyle, 32)
	
	screen = pygame.display.set_mode(winsize,winstyle, bestdepth)
	
	clock = pygame.time.Clock()
	
	running = True	
	while running:
		events = pygame.event.get()
		for e in events:
			if e.type == QUIT:
				running = False
				break
			if e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					running = False
					break
		
		pygame.display.flip()
		clock.tick(60)
	
	
	#app.close()
	pygame.quit()
	return 0

if __name__ == '__main__':
	print "argv:",sys.argv
	size = [DEFAULTSCRSIZE[0], DEFAULTSCRSIZE[1]]
	fullscr = DEFAULTFULLSCR
	for i in range(1,len(sys.argv)):
		if sys.argv[i] == '-s':
			size = [sys.argv[i+1], sys.argv[i+2]]
		elif sys.argv[i] == '-f':
			fullscr = int(sys.argv[i+1])
	
	main(size, fullscr)

