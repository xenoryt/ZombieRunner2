import pygame
import os

screensize = [800,600]
pygame.init()
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("TEST")

player = {}

def loadImages(imagefile, d):
	sheet = pygame.image.load(os.path.join("data",imagefile))
	sheetrect = sheet.get_rect()
	images = []
	#~ print imagefile, d, range(sheetrect.width/48)
	for x in range(sheetrect.width/48):
		rect = pygame.Rect(x*48,0, 48,48)
		print rect
		image = pygame.Surface((48,48))
		
		image.blit(sheet, (0,0),rect)
		image.set_colorkey((0,0,0))
		images.append(image)
	player[d] = images
	
loadImages("player_up.png", "up")
loadImages("player_down.png", "down")
loadImages("player_right.png", "right")
loadImages("player_left.png", "left")

sheet = pygame.image.load(os.path.join("data","player_down.png"))

print "loaded"

running = True

while running:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	screen.blit(background, (0, 0))
	for x in range(3):
		screen.blit(player["down"][x], player["down"][x].get_rect(topleft=(x*48, 0)))
	screen.blit(sheet, (0,48))
	pygame.display.flip()
	
