from random import *
from Enemy import *
from Torch import *
from Chest import *

class Room(object):
	def __init__(self, BigX, BigY, doors):
		self.bigX = BigX
		self.bigY = BigY
		self.doors = doors

		self.roomType = ""
		self.numEnemies = int(random() * 5) + 1
		roomNum = random()
		self.roomType = "Safe"
		self.connected = False
		self.dist = -1
		self.torches = []
		self.chests = []

		self.defeated = False

	def getDoors(self):
		return self.doors

	def addDoor(self, door):
		self.doors.append(door)

	def connect(self):
		self.connected = True

	def distance(self, dist):
		if self.dist == -1:
			self.dist = dist
		return self

	def getDrones(self, width, height):
		if self.roomType == "Enemy" and not self.defeated:
			drone_list = []
			for i in range(self.numEnemies):
				drone_list.append(Drone(int(40+random()*(width-80)), int(40+random()*(height-80))))
			return drone_list
		elif self.roomType == "Boss" and not self.defeated:
			drone_list = [Boss(1+int(random()*2))]
			return drone_list
		return []

	def addTorch(self, torch):
		self.torches.append(torch)

	def getTorches(self):
		return self.torches

	def setRoomType(self, rt):
		self.roomType = rt

	def getDist(self):
		return self.dist

	def initChest(self):
		self.chests = [Chest(200,150)]

	def getChests(self):
		return self.chests

	def getTrapdoors(self):
		if self.roomType == "Exit":
			return [Trapdoor(200,150)]
		return []

