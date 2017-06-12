from Room import *
from queue import *
from random import *
import pygame

class Roommap(object):
	def __init__(self, radius):
		self.radius = radius

		self.room_grid = [[0 for i in range(radius*2-1)] for j in range(radius*2-1)]
		
		self.doorgrid = [[[0,0,0,0] for i in range(radius*2-1)] for j in range(radius*2-1)]
		diam = radius*2-1

		for i in range(-radius+1, radius):
			for j in range(-radius+1, radius):
				value = ((i)**2 + (j)**2)**(1/2)
				if value <= radius-1:
					self.room_grid[i+radius-1][j+radius-1] = Room(i+radius-1, j+radius-1, [])

		room_starter = self.room_grid[radius-1][radius-1]

		for i in range(diam):
			for j in range(diam):
				temp = self.room_grid[i][j]
				if type(temp) == type(Room(None,None,[])):
					temp_right = None
					temp_down = None
					try:
						if i+1 < diam or i+1 >= 0:
							temp2 = self.room_grid[i+1][j]
					except Exception:
						continue
					try:
						if j+1 < diam or j+1 >= 0:
							temp3 = self.room_grid[i][j+1]
					except Exception:
						continue

					if type(temp2) == type(Room(None,None,[])) and random() > 0.2:
						location = 1 + int(random() * 13)
						temp.addDoor([3,location])
						temp2.addDoor([2,location])
					if type(temp3) == type(Room(None,None,[])) and random() > 0.2:
						location = 1 + int(random() * 18)
						temp.addDoor([1,location])
						temp3.addDoor([0,location])

		self.connect_rooms()
		self.clear_unconnected()
		self.setRoomTypes()
		self.buildChests()
	
	def draw(self, screen, width, height, bigX, bigY):
		screen.fill([0,0,0])
		sq_size = min(width, height) / (self.radius * 2 + 1)
		space_size = sq_size / (self.radius)
		offset = (width - height) / 2

		for i in range(len(self.room_grid)):
			for j in range(len(self.room_grid)):
				color = [255,80,80]
				if i == bigX and j == bigY: color = [80, 80, 255]
				
				
				if type(self.room_grid[i][j]) == type(Room(None,None,[])):
					if self.room_grid[i][j].roomType == "Boss": color = [100,100,100]
					if self.room_grid[i][j].roomType == "Exit": color = [40,230,40]
					# color[0] = self.room_grid[i][j].dist * 50
					# if color[0] > 255: color[0] = 255
					if any(x[0] == 1 for x in self.room_grid[i][j].doors):
						#draw a line down
						pygame.draw.line(screen, [255,80,80], 
							[offset + space_size + i * (sq_size+space_size) + 0.5*sq_size, (j+1) * (sq_size+space_size) - 5],
							[offset + space_size + i * (sq_size+space_size) + 0.5*sq_size, (j+1) * (sq_size+space_size) + space_size + 5], 5)
					if any(x[0] == 3 for x in self.room_grid[i][j].doors):
						#draw a line to the right
						pygame.draw.line(screen, [255,80,80], 
							[offset + space_size + i * (sq_size+space_size) + sq_size - 5, space_size + j * (sq_size+space_size) + 0.5*sq_size],
							[offset + space_size + i * (sq_size+space_size) + sq_size + space_size + 5, space_size + j * (sq_size+space_size) + 0.5*sq_size], 5)
							
					pygame.draw.rect(screen, color, pygame.Rect(offset + space_size + i * (sq_size+space_size), 
								 space_size + j * (sq_size+space_size), sq_size, sq_size))

	def connect_rooms(self):
		q = Queue()

		q.put(self.room_grid[self.radius-1][self.radius-1].distance(0))

		while not q.empty():
			temp = q.get()
			if not temp.connected:
				temp.connect()

				bigX = temp.bigX
				bigY = temp.bigY

				for door in temp.doors:
					if door[0] == 0:
						q.put(self.room_grid[bigX][bigY-1].distance(temp.dist + 1))
					elif door[0] == 1:
						q.put(self.room_grid[bigX][bigY+1].distance(temp.dist + 1))
					elif door[0] == 2:
						q.put(self.room_grid[bigX-1][bigY].distance(temp.dist + 1))
					elif door[0] == 3:
						q.put(self.room_grid[bigX+1][bigY].distance(temp.dist + 1))

	def setRoomTypes(self):
		maxDist = 0
		mdi = -1
		mdj = -1

		for i in range(len(self.room_grid)):
			for j in range(len(self.room_grid)):
				if type(self.room_grid[i][j]) == type(Room(None,0,0)):
					if (i == self.radius-1 and j == self.radius-1):
						self.room_grid[i][j].setRoomType("Base")
					elif (i == 0 or j == 0 or i == self.radius*2 - 2 or j == self.radius*2 - 2):
						self.room_grid[i][j].setRoomType("Boss")
					elif random() > 0.3:
						self.room_grid[i][j].setRoomType("Enemy")

					temp_dist = self.room_grid[i][j].getDist()

					if temp_dist > maxDist:
						
						maxDist = temp_dist
						mdj = i
						mdi = j

		self.room_grid[mdj][mdi].setRoomType("Exit")

	def buildChests(self):
		for i in range(len(self.room_grid)):
			for j in range(len(self.room_grid)):
				if type(self.room_grid[i][j]) == type(Room(None,0,0)):
					if self.room_grid[i][j].roomType == "Safe":
						self.room_grid[i][j].initChest()


	def clear_unconnected(self):
		for i in range(len(self.room_grid)):
			for j in range(len(self.room_grid)):
				if type(self.room_grid[i][j]) == type(Room(None,None,[])) and not self.room_grid[i][j].connected:
					self.room_grid[i][j] = 0








