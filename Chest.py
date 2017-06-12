from random import *
import pygame

class Chest(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 7
		self.open = False
		self.numTorches = int(random()*2+2)

	def draw(self, screen):
		if not self.open: color = [81,59,31]
		else: color = [0,0,0]
		pygame.draw.rect(screen, color, pygame.Rect(self.x-self.width, self.y-self.width, 2*self.width, 2*self.width))

class Trapdoor(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 7

	def draw(self, screen):
		color = [89,244,66]
		pygame.draw.rect(screen, color, pygame.Rect(self.x-self.width, self.y-self.width, 2*self.width, 2*self.width))

	def get_dist(self, other):
		dx = self.x - other.x
		dy = self.y - other.y
		distance = (dx**2 + dy**2) ** (1/2)
		return distance

	def exit(self, x, y, sqheight, sqwidth):
			
		dx = x + 0.5*(sqwidth-5) - self.x
		dy = y + 0.5*(sqheight-5) - self.y
		necessary_x = 0.5*(sqwidth-5) + self.width
		necessary_y = 0.5*(sqheight-5) + self.width

		if abs(dx) < necessary_x and abs(dy) < necessary_y:
			return True

