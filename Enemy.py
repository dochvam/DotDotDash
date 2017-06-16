from random import *
import pygame
from math import *

class Drone(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.health = 100
		self.alive = True
		self.max_health = 100
		self.counter = int(random()*20)
		self.radius = 4
		self.frequency = 50

	def step(self, other_x, other_y):
		step_dir = [0,0]

		dx = other_x - self.x
		dy = other_y - self.y

		if dy != 0:
			if dx > 0:
				step_dir[0] = 1
			elif dx < 0:
				step_dir[0] = -1
			if dy < 0:
				step_dir[1] = -1
			elif dy > 0:
				step_dir[1] = 1

			y = 2 / ((dx/dy)**2 + 1)**(1/2)
			x = (4 - y**2)**(1/2)
		else:
			x = 2
			y = 0
			if dx > 0: step_dir = [1,0]
			else: step_dir = [-1, 0]

		self.x += int(step_dir[0]*abs(x))
		self.y += int(step_dir[1]*abs(y))
			

	def hurt(self, damage, room):
		self.health -= damage
		if self.health <= 0:
			self.alive = False

	def shoot(self, ox, oy):
		self.counter += 1
		if self.counter >= self.frequency:
			self.counter = self.counter % self.frequency - int(150*random())
			dx = ox - self.x
			dy = oy - self.y			
			return Shot(self.x, self.y, [dx, dy])

	def draw(self, screen):
		if self.alive:
			pygame.draw.circle(screen, [0,0,0], [self.x,self.y], self.radius)
			if self.max_health != self.health:
				pygame.draw.rect(screen, [0,0,0], pygame.Rect(self.x-5, self.y-7,10,2))
				pygame.draw.rect(screen, [225,20,20], pygame.Rect(self.x-5, self.y-7,0.1*self.health,2))


class Shot(pygame.sprite.DirtySprite):
	def __init__(self, x, y, direc):
		pygame.sprite.DirtySprite.__init__(self)
		self.x = x
		self.y = y
		if direc[0] != 0: self.direction = atan(direc[1]/direc[0])
		else: self.direction = 0
		self.dir_sin = [1,1]
		if direc[0] < 0: self.dir_sin[0] = -1
		if direc[1] < 0: self.dir_sin[1] = -1
		self.lifespan = 60
		self.counter = 0
		self.speed = 3
		self.alive = True
		self.radius = 2

	def step(self):
		self.x += self.speed * abs(cos(self.direction)) * self.dir_sin[0]
		self.y += self.speed * abs(sin(self.direction)) * self.dir_sin[1]
		self.counter += 1
		if self.counter >= self.lifespan:
			self.remove = False
		self.dirty = 1

	def draw(self, screen):
		if self.alive:
			pygame.draw.circle(screen, [20,0,0], [int(self.x),int(self.y)], self.radius)


class Boss(object):
	def __init__(self, bossType):
		self.x = 200
		self.y = 150
		self.counter = 0
		self.alive = True
		self.type = bossType

		if bossType == 1:
			self.health = 200
			self.max_health = 200
			self.radius = 10
			self.shape = "Circle"
			self.frequency = 5

		if bossType == 2:
			self.health = 400
			self.max_health = 400
			self.radius = 7
			self.shape = "Pentagon"
			self.frequency = 18


	def step(self, other_x, other_y):
		step_dir = [0,0]

		dx = other_x - self.x
		dy = other_y - self.y

		if dy != 0:
			if dx > 0:
				step_dir[0] = 1
			elif dx < 0:
				step_dir[0] = -1
			if dy < 0:
				step_dir[1] = -1
			elif dy > 0:
				step_dir[1] = 1

			y = 2 / ((dx/dy)**2 + 1)**(1/2)
			x = (4 - y**2)**(1/2)
		else:
			x = 2
			y = 0
			if dx > 0: step_dir = [1,0]
			else: step_dir = [-1, 0]

		self.x += int(step_dir[0]*abs(x))
		self.y += int(step_dir[1]*abs(y))
			

	def hurt(self, damage, room):
		self.health -= damage
		if self.health <= 0:
			self.alive = False
			if len(room.chests) == 0:
				room.initChest()
			room.defeated = True

	def shoot(self, ox, oy):
		self.counter += 1
		if self.counter >= self.frequency:
			self.counter = self.counter % self.frequency
			dx = ox - self.x
			dy = oy - self.y			
			return Shot(self.x, self.y, [dx, dy])

	def draw(self, screen):
		if self.alive:
			if self.shape == "Circle":
				pygame.draw.circle(screen, [0,0,0], [self.x,self.y], self.radius)
			if self.shape == "Pentagon":
				draw_ngon(screen, [0,0,0], 5, self.radius, [self.x, self.y])


			if self.max_health != self.health:
				pygame.draw.rect(screen, [0,0,0], pygame.Rect(self.x-5, self.y-7,10,2))
				pygame.draw.rect(screen, [225,20,20], pygame.Rect(self.x-5, self.y-7,0.1*self.health,2))



def draw_ngon(Surface, color, n, radius, position):
    pi2 = 2 * 3.14

    for i in range(0, n):
        pygame.draw.line(Surface, color, position, (cos(i / n * pi2) * radius + position[0], sin(i / n * pi2) * radius + position[1]))

    return pygame.draw.lines(Surface,
          color,
          True,
          [(cos(i / n * pi2) * radius + position[0], sin(i / n * pi2) * radius + position[1]) for i in range(0, n)])







