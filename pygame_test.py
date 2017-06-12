import pygame
from Room import *
from Roommap import *
from queue import *
from Enemy import *
from Torch import *
from Chest import *
pygame.font.init() 

global width, height, sqwidth, sqheight

def drawWalls(screen, walls):
	global width, height, sqwidth, sqheight, bgcolor, roomType, distance
	pygame.draw.rect(screen, (100,100,100), pygame.Rect(0,0, width, 10))
	pygame.draw.rect(screen, (100,100,100), pygame.Rect(0,0, 10, height))
	pygame.draw.rect(screen, (100,100,100), pygame.Rect(0,height-10, width, 10))
	pygame.draw.rect(screen, (100,100,100), pygame.Rect(width-10,0, 10, height))

	for i in range(len(walls[0])):
		if walls[0][i] == 1:
			pygame.draw.rect(screen, bgcolor, pygame.Rect(i*sqwidth, 0, sqwidth, sqheight))
	for i in range(len(walls[1])):
		if walls[1][i] == 1:
			pygame.draw.rect(screen,bgcolor, pygame.Rect(i*sqwidth, height-sqheight, sqwidth, sqheight))
	for i in range(len(walls[2])):
		if walls[2][i] == 1:
			pygame.draw.rect(screen, bgcolor, pygame.Rect(0, i*sqheight, sqwidth, sqheight))
	for i in range(len(walls[3])):
		if walls[3][i] == 1:
			pygame.draw.rect(screen, bgcolor, pygame.Rect(width-sqwidth, i*sqheight, sqwidth, sqheight))

	font=pygame.font.Font(None,30)
	scoretext=font.render(str(numTorches), 1, (255,255,255))
	screen.blit(scoretext, (width-50, height-25))

	Torch(width-30, height-20).draw(screen)

def getWalls(room):
	global width, height, sqwidth, sqheight
	topwalls = [0 for i in range(width//sqwidth)]
	bottomwalls = [0 for i in range(width//sqwidth)]
	rightwalls = [0 for i in range(height//sqheight)]
	leftwalls = [0 for i in range(height//sqheight)]

	for door in room.doors:
		if door[0] == 0: topwalls[door[1]] = 1
		if door[0] == 1: bottomwalls[door[1]] = 1
		if door[0] == 2: leftwalls[door[1]] = 1
		if door[0] == 3: rightwalls[door[1]] = 1

	return topwalls, bottomwalls, leftwalls, rightwalls			

def moveUnit(step):
	global width, height, sqwidth, sqheight, x, y, walls, bigX, bigY
	tempx = (x + step[0]) % width
	tempy = (y + step[1]) % height

	if (x + step[0]) < 0:
		bigX = bigX - 1
		return tempx, y
	elif (x + step[0]) >= width:
		bigX = bigX + 1
		return tempx, y
	elif (y + step[1]) < 0:
		bigY = bigY - 1
		return x, tempy
	elif (y + step[1]) >= height:
		bigY = bigY + 1
		return x, tempy

	changeX = False
	if tempx < 10:
		if walls[2][tempy // sqheight] != 0 and walls[2][(tempy + sqheight-5)// sqheight]: return(tempx, y)
	elif tempx > width - (5+sqwidth):
		if walls[3][tempy // sqheight] != 0 and walls[3][(tempy + sqheight-5)// sqheight]: return(tempx, y)
	else:
		changeX = True

	if tempy < 10:
		if walls[0][tempx // sqwidth] != 0 and walls[0][(tempx + sqwidth-5)// sqwidth]: return(x, tempy)
	elif tempy > height - (5+sqheight):
		if walls[1][tempx // sqwidth] != 0 and walls[1][(tempx + sqwidth-5)// sqwidth]: return(x, tempy)
	else:
		y = tempy

	if changeX: x = tempx
	return x,y

def testForHit(enemylist):
	global sqheight, sqwidth, game_over

	for obj in enemylist:
		if obj != None:
			dx = x + 0.5*(sqwidth-5) - obj.x
			dy = y + 0.5*(sqheight-5) - obj.y

			necessary_x = 0.5*(sqwidth-5) + obj.radius
			necessary_y = 0.5*(sqheight-5) + obj.radius

			if abs(dx) < necessary_x and abs(dy) < necessary_y:
				game_over = True

def testForTouch(chestlist):
	global sqheight, sqwidth, numTorches
	for obj in chestlist:
		if obj != None and not obj.open:
			dx = x + 0.5*(sqwidth-5) - obj.x
			dy = y + 0.5*(sqheight-5) - obj.y
			necessary_x = 0.5*(sqwidth-5) + obj.width
			necessary_y = 0.5*(sqheight-5) + obj.width

			if abs(dx) < necessary_x and abs(dy) < necessary_y:
				obj.open = True
				numTorches += obj.numTorches

def killDead(enemylist):
	temp_list = []
	for i in range(len(enemylist)):
		if enemylist[i] != None and enemylist[i].alive:
			temp_list.append(enemylist[i])
	return temp_list

def getDrones(room, width, height):
	return room.getDrones(width, height)

def getTorches(room):
	return room.getTorches()

def getChests(room):
	return room.getChests()

def getTrapdoors(room):
	return room.getTrapdoors()

def drawLoadingScreen():
	global intro_screen, status, screencounter
	screencounter += 1
	intro_screen = pygame.Surface((width, height))
	font = pygame.font.SysFont("Arial",50)
	scoretext = font.render("DOT DOT DASH", 1, (255,255,255))
	text_rect = scoretext.get_rect(center=(width/2, height/3))
	menu = ["Begin", "Instructions", "Credits"]
	intro_screen.blit(scoretext, text_rect)
	screen.blit(intro_screen, [0,0])



pygame.init()
done = False
is_blue = True
x = 50
y = 50
width = 400
height = 300
sqheight = sqwidth = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
lastBigX = -1
lastBigY = -1
bgcolor = (220, 220, 220)
radius = 1
bigX = radius-1
bigY = radius-1
game_over = False
numTorches = 5
roomType = ""
distance = 0 
screencounter = 0
status = 0

rooms = Roommap(radius)

walls = getWalls(rooms.room_grid[bigX][bigY])
draw_all = True

drones = []
shots = []
chests = []
trapdoors = []

testdrive = False

ready = False

while not ready:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			if status == 0: ready = True

	print(screencounter)
	drawLoadingScreen()
	pygame.display.flip()
	clock.tick(60)



while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			rooms.draw(screen, width, height, bigX, bigY)
			draw_all = not draw_all
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			if numTorches > 0:
				numTorches -= 1
				rooms.room_grid[bigX][bigY].addTorch(Torch(x, y))
				torches.append(Torch(x, y))

	if (draw_all):
		if (bigX != lastBigX) or (bigY != lastBigY):
			walls = getWalls(rooms.room_grid[bigX][bigY])
			if not testdrive: drones = getDrones(rooms.room_grid[bigX][bigY], width, height)
			torches = getTorches(rooms.room_grid[bigX][bigY])
			trapdoors = getTrapdoors(rooms.room_grid[bigX][bigY])
			shots = []
			roomType = rooms.room_grid[bigX][bigY].roomType
			distance = rooms.room_grid[bigX][bigY].dist
			chests = getChests(rooms.room_grid[bigX][bigY])

		lastBigX = bigX
		lastBigY = bigY

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_UP]: x,y = moveUnit([0,-2])
		if pressed[pygame.K_DOWN]: x,y = moveUnit([0,2])
		if pressed[pygame.K_LEFT]: x,y = moveUnit([-2,0])
		if pressed[pygame.K_RIGHT]: x,y = moveUnit([2,0])
		
		screen.fill(bgcolor)
		drawWalls(screen, walls)
		if is_blue: color = (0, 128, 255)
		else: color = (255, 100, 0)
		pygame.draw.rect(screen, color, pygame.Rect(x, y, sqheight-5, sqwidth-5))
		for drone in drones:
			drone.draw(screen)
			drone.step(x, y)

			shots.append(drone.shoot(x,y))
		torches = killDead(torches)
		for torch in torches:
			torch.draw(screen, width, height, True)
			torch.glow(drones, rooms.room_grid[bigX][bigY])
		shots = killDead(shots)

		testForTouch(chests)
		for chest in chests:
			chest.draw(screen)

		for shot in shots:
			shot.step()
			shot.draw(screen)

		for door in trapdoors:
			door.draw(screen)
			if door.exit(x, y, sqwidth, sqheight):
				radius += 1
				rooms = Roommap(radius)
				bigX = radius-1
				bigY = radius-1

		chests = getChests(rooms.room_grid[bigX][bigY])

		testForHit(drones)
		testForHit(shots)
		drones = killDead(drones)

	if game_over:
		done = True

	pygame.display.flip()
	clock.tick(60)

pygame.display.flip()
clock.tick(600)