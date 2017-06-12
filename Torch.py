from random import *
import pygame

class Torch(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.health = 100
		self.maxhealth = 100
		self.hurt_dist = 100
		self.alive = True

	def draw(self, screen, width = 0, height = 0, do_glow = False):
		pygame.draw.line(screen, [117,74,50], [self.x,self.y], [self.x,self.y+13], 3)
		pygame.draw.circle(screen, [234,233,182], [self.x, self.y], 8)
		pygame.draw.circle(screen, [255,255,255], [self.x, self.y], 5)
			
		if do_glow:
			glow = pygame.Surface((width, height), pygame.SRCALPHA, 32)
			pygame.draw.circle(glow, [255,255,255,50], [self.x, self.y], self.hurt_dist)
			pygame.draw.circle(glow, [255,238,237,50], [self.x, self.y], int(0.5*self.hurt_dist))
			screen.blit(glow, pygame.rect.Rect(0,0, width, height))

	def get_dist(self, other):
		dx = self.x - other.x
		dy = self.y - other.y
		distance = (dx**2 + dy**2) ** (1/2)
		return distance

	def glow(self, enemies, room):
		for enemy in enemies:
			distance = self.get_dist(enemy)
			if distance < self.hurt_dist:
				enemy.hurt(1, room)
				if distance < 0.5*self.hurt_dist:
					self.hurt(2)

	def hurt(self, damage):
		self.health -= damage
		if self.health <= 0:
			self.alive = False