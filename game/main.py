#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2013 Tyrone Xiong <ty.cx@hotmail.com>
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

import pygame, sys
from pygame.locals import *

from game import *
import mapgenerator
from mapgenerator import MapGenerator
from world import World
import tile
import os
import sprite
import item

import gui
		
def loadImages():
	files = ["floor.png", "wall.png"]
	for file in files:
		tile.Tile.images.append(pygame.image.load(os.path.join("data",file)))
	
	gui.Button.images.append(pygame.image.load(os.path.join("data","button_normal.png")))
	gui.Button.images.append(pygame.image.load(os.path.join("data","button_hover.png")))
	
	gui.Bar.images = pygame.image.load(os.path.join("data","bar.png"))
	
	sprite.loadImages(sprite.Sprite, "player_up.png", "up")
	sprite.loadImages(sprite.Sprite, "player_down.png", "down")
	sprite.loadImages(sprite.Sprite, "player_right.png", "right")
	sprite.loadImages(sprite.Sprite, "player_left.png", "left")
	
	sprite.loadImages(sprite.Bat, "bat_up.png", "up")
	sprite.loadImages(sprite.Bat, "bat_down.png", "down")
	sprite.loadImages(sprite.Bat, "bat_right.png", "right")
	sprite.loadImages(sprite.Bat, "bat_left.png", "left")
	
	sprite.loadImages(sprite.Skel, "skel_up.png", "up")
	sprite.loadImages(sprite.Skel, "skel_down.png", "down")
	sprite.loadImages(sprite.Skel, "skel_right.png", "right")
	sprite.loadImages(sprite.Skel, "skel_left.png", "left")
	
	sprite.loadImages(sprite.Reaper, "reaper_up.png", "up")
	sprite.loadImages(sprite.Reaper, "reaper_down.png", "down")
	sprite.loadImages(sprite.Reaper, "reaper_right.png", "right")
	sprite.loadImages(sprite.Reaper, "reaper_left.png", "left")
	
	sprite.loadImages(sprite.Dragon, "dragon_up.png", "up")
	sprite.loadImages(sprite.Dragon, "dragon_down.png", "down")
	sprite.loadImages(sprite.Dragon, "dragon_right.png", "right")
	sprite.loadImages(sprite.Dragon, "dragon_left.png", "left")
	
	sprite.Chest.image = pygame.image.load(os.path.join("data","chest.png"))
	sprite.Stair.image = pygame.image.load(os.path.join("data","stairs2.png"))
	
	state.InventoryState.btnImages = [pygame.image.load(os.path.join("data","inventory_grid.png"))]
	
	state.InventoryState.invImages = {0:pygame.image.load(os.path.join("data","inventory_grid.png")),
									  1:pygame.image.load(os.path.join("data/items","red_potion.png")),
									  2:pygame.image.load(os.path.join("data/items","orange_potion.png")),
									  3:pygame.image.load(os.path.join("data/items","yellow_potion.png")),
									  4:pygame.image.load(os.path.join("data/items","white_potion.png")),
									  5:pygame.image.load(os.path.join("data/items","rock.png")),
									  6:pygame.image.load(os.path.join("data/items","cypress_stick.png")),
									  7:pygame.image.load(os.path.join("data/items","item.png")),
									  8:pygame.image.load(os.path.join("data/items","item.png")),
									  9:pygame.image.load(os.path.join("data/items","item.png")),
									  10:pygame.image.load(os.path.join("data/items","item.png")),
									  11:pygame.image.load(os.path.join("data/items","Torch.png")),
									  12:pygame.image.load(os.path.join("data/items","lantern.png")),
									  13:pygame.image.load(os.path.join("data/items","Blade_of_Grass.png")),
									  14:pygame.image.load(os.path.join("data/items","muramasa.png")),
									  15:pygame.image.load(os.path.join("data/items","Master_Sword_edited.png")),
									  16:pygame.image.load(os.path.join("data/items","item.png")),
									  17:pygame.image.load(os.path.join("data/items","item.png")),
									  18:pygame.image.load(os.path.join("data/items","item.png")),
									  19:pygame.image.load(os.path.join("data/items","item.png")),
									  20:pygame.image.load(os.path.join("data/items","item.png"))
									  }

def main():
	
	loadImages()
	item.CreateItemList()
	
	game.run(state.MainMenuState(game))
	
	return 0

if __name__ == '__main__':
	main()

