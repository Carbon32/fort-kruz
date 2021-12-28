# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
from pygame import mixer
import math
import random

# Pygame & Mixer Initializations: #

pygame.init()
mixer.init()

# Global Variables: #

windowWidth = 0
windowHeight = 0
gameLevel = 1
nextLevel = False
levelDifficulty = 0
gameDifficulty = 1000
difficultyMultiplier = 2
enemyTimer = 2000
lastEnemy = pygame.time.get_ticks()
enemiesAlive = 0
gameOver = False
randomEnemy = 0
levelResetTime = 0

# Tower Spawn Positions: #

towerPositions = [
[600, 440],
[400, 445],
]

# Sprite Groups: #

cannonBalls = pygame.sprite.Group()
gameEnemies = pygame.sprite.Group()
gameTowers = pygame.sprite.Group()

# Engine Functions: #

def changeSpawnTimer(newSpawnTimer : int):
	global enemyTimer
	enemyTimer = newSpawnTimer

def changeGameDifficulty(newLevelDifficulty : int, newGameDifficulty : int, newDifficultyMultiplier : int):
	global levelDifficulty
	global gameDifficulty
	global difficultyMultiplier
	levelDifficulty = newLevelDifficulty
	gameDifficulty = newGameDifficulty
	newDifficultyMultiplier = newDifficultyMultiplier

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path)
		image = pygame.transform.scale(image, (width, height))
		return image

def updateGameTowers(engineWindow : pygame.Surface, fort : pygame.Surface, ballSprite : pygame.Surface):
	global gameEnemies
	gameTowers.update(engineWindow, fort, gameEnemies, ballSprite)
	gameTowers.draw(engineWindow)

def updateGameMechanics(engineWindow : pygame.Surface, fort : pygame.Surface, enemyAnimations : list, enemyTypes : list, enemyHealth : list, sound : mixer.Sound):
		global levelDifficulty
		global gameDifficulty
		global lastEnemy
		global randomEnemy
		global nextLevel
		global gameLevel
		global levelResetTime
		cannonBalls.update(windowWidth, windowHeight)
		cannonBalls.draw(engineWindow)
		gameEnemies.update(engineWindow, fort, sound)
		gameEnemies.draw(engineWindow)
		showStats(engineWindow, fort, gameLevel)
		if(levelDifficulty < gameDifficulty):
			if(pygame.time.get_ticks() - lastEnemy > enemyTimer):
				if(gameLevel == 1):
					randomEnemy = random.randint(0, len(enemyTypes) - 3)
				elif(gameLevel == 2):
					randomEnemy = random.randint(0, len(enemyTypes) - 2)
				else:
					randomEnemy = random.randint(0, len(enemyTypes) - 1)
				lastEnemy = pygame.time.get_ticks()
				gameEnemy = Enemy(enemyHealth[randomEnemy], enemyAnimations[randomEnemy], -100, 525, 1)
				gameEnemies.add(gameEnemy)
				levelDifficulty += enemyHealth[randomEnemy]
		if(levelDifficulty >= gameDifficulty):
			enemiesAlive = 0
			for enemy in gameEnemies:
				if enemy.alive == True:
					enemiesAlive += 1
			if(enemiesAlive == 0 and nextLevel == False):
				nextLevel = True
				levelResetTime = pygame.time.get_ticks()

		if(nextLevel == True):
			drawText(engineWindow, 'LEVEL COMPLETE', 20, (204, 0, 0), 260, 200)
			if(pygame.time.get_ticks() - levelResetTime > 1500):
				nextLevel = False
				gameLevel += 1
				lastEnemy = pygame.time.get_ticks()
				gameDifficulty *= difficultyMultiplier
				levelDifficulty = 0
				gameEnemies.empty()
		if(fort.health <= 0):
			gameOver = True

def loadGameEnemies(enemyTypes : list, anims : list):
	enemyAnimations = []
	enemyTypes = enemyTypes
	animationTypes = anims

	for enemy in enemyTypes:
	    animationList = []
	    for animation in animationTypes:
	        tempList = []
	        spriteFrames = 5
	        for i in range(spriteFrames):
	            image = pygame.image.load(f'assets/{enemy}/{animation}/{i}.png').convert_alpha()
	            enemyWidth = image.get_width()
	            enemyHeight = image.get_height()
	            image = pygame.transform.scale(image, (int(enemyWidth * 0.15), int(enemyHeight * 0.15)))
	            tempList.append(image)
	        animationList.append(tempList)
	    enemyAnimations.append(animationList)
	return enemyAnimations, enemyTypes

def assignEnemyHealth(enemyHealth : list):
	return enemyHealth

def drawText(engineWindow : pygame.Surface, text : str, size : int, color : tuple, x : int, y : int):
    textImage = pygame.font.SysFont('Impact', size).render(text, True, color)
    engineWindow.blit(textImage, (x, y))

def showStats(engineWindow : pygame.Surface, fort : pygame.Surface, level : int):
	drawText(engineWindow, 'Coins: ' + str(fort.coins), 20, (50, 49, 63), 10, 10)
	drawText(engineWindow, 'Score: ' + str(fort.kills), 20, (50, 49, 63), 180, 10)
	drawText(engineWindow, 'Level: ' + str(level), 20, (50, 49, 63), 400, 10)
	drawText(engineWindow, 'Health: ' + str(fort.health) + "/" + str(fort.maxHealth), 18, (50, 49, 63), 585, 225)
	drawText(engineWindow, '500c', 16, (34, 34, 31), 660, 42)
	drawText(engineWindow, '1,000c', 16, (34, 34, 31), 650, 112)
	drawText(engineWindow, '2,000c (Max: 2)', 16, (34, 34, 31), 600, 183)

def resetGame():
	drawText('GAME OVER', secondGameFont, (204, 0, 0), 260, 200)
	drawText('PRESS "SPACE" TO RESTART', secondGameFont, (204, 0, 0), 150, 280)
	pygame.mouse.set_visible(True)
	key = pygame.key.get_pressed()
	if(key[pygame.K_SPACE]):
		gameOver = False
		level = 1
		gameDifficulty = 1000
		levelDifficulty = 0
		lastEnemy = pygame.time.get_ticks()
		gameEnemies.empty()
		gameTowers.empty()
		fort.score = 0
		fort.health = 1000
		fort.coins = 0
		pygame.mouse.set_visible(False)

# Engine Window: #

class Window():
	def __init__(self, screenWidth : int, screenHeight : int, windowTitle : str):
		global windowWidth, windowHeight
		windowWidth = screenWidth
		windowHeight = screenHeight
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.engineRunning = False
		self.windowTitle = windowTitle
		self.fpsLimit = pygame.time.Clock()
	
	def init(self):
		self.engineWindow = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption(self.windowTitle)
		self.engineRunning = True

	def updateDisplay(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.engineRunning = False
		pygame.display.update()

	def limitFPS(self, fps : int):
		self.fpsLimit.tick(fps)
	
	def setBackground(self, background : pygame.Surface, x : int, y : int):
		self.engineWindow.blit(background, (x, y))

# Game Fort: #

class Fort():
    def __init__(self, firstImage : pygame.Surface, secondImage : pygame.Surface, thirdImage : pygame.Surface, x : int, y : int, health : int, coins : int):
        self.health = health
        self.maxHealth = self.health
        self.alreadyFired = False
        self.coins = coins
        self.kills = 0
        self.firstImage = firstImage
        self.secondImage = secondImage
        self.thirdImage = thirdImage
        self.image = firstImage
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def fireBall(self, ballSprite : pygame.Surface, sound : mixer.Sound):
        position = pygame.mouse.get_pos()
        xDistance = (position[0] - self.rect.midleft[0])
        yDistance = -(position[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(yDistance, xDistance))
        if (pygame.mouse.get_pressed()[0] and self.alreadyFired == False and position[0] <= 500 and position[1] > 100):
            ball = Ball(ballSprite, self.rect.midleft[0] + 30, self.rect.midleft[1] - 25, self.angle)
            cannonBalls.add(ball)
            self.alreadyFired = True
            sound.play()
        if (pygame.mouse.get_pressed()[0] == False):
            self.alreadyFired = False


    def drawFort(self, engineWindow : pygame.Surface):
        if(self.health <= 250):
            self.image = self.thirdImage
        elif(self.health <= 500):
            self.image = self.secondImage
        else:
            self.image = self.firstImage
        engineWindow.blit(self.image, self.rect)

    def repairFort(self):
        if(self.coins >= 500 and self.health < self.maxHealth):
            self.health += 250
            self.coins -= 500
            if (self.health > self.maxHealth):
                self.health = self.maxHealth

    def upgradeArmour(self):
        if(self.coins >= 1000):
            self.maxHealth += 500
            self.coins -= 1000


# Cannon Ball: #

class Ball(pygame.sprite.Sprite):
    def __init__(self, image : pygame.Surface, x : int, y : int, angle : int):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 5
        self.deltaX = math.cos(self.angle) * self.speed
        self.deltaY = -(math.sin(self.angle)) * self.speed


    def update(self, screenWidth : int, screenHeight : int):
        if(self.rect.right < 0 or self.rect.left > screenWidth or self.rect.bottom < 0 or self.rect.top > screenHeight):
            self.kill()
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY

# Crosshair: #

class Crosshair():
    def __init__(self, image : pygame.Surface):
        self.crosshair = image
        self.rect = self.crosshair.get_rect()
        pygame.mouse.set_visible(False)
        
    def drawCrosshair(self, engineWindow : pygame.Surface):
        position = pygame.mouse.get_pos()
        self.rect.center = (position[0], position[1])
        engineWindow.blit(self.crosshair, self.rect)

# Enemy: #

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health : int, animationList : pygame.Surface, x : int, y : int, speed : int):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.lastAttack = pygame.time.get_ticks()
        self.attackCooldown = 2000
        self.animationList = animationList
        self.frameIndex = 0
        self.action = 0
        self.updateTime = pygame.time.get_ticks()
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, engineWindow : pygame.Surface, fort : pygame.Surface, sound : mixer.Sound):
        if(self.alive):
            if(pygame.sprite.spritecollide(self, cannonBalls, True)):
                self.health -= 25

            if(self.rect.right > fort.rect.left):
                self.updateAction(1)

            if(self.action == 0):
                self.rect.x += self.speed

            if(self.action == 1):
                if(pygame.time.get_ticks() - self.lastAttack > self.attackCooldown):
                    fort.health -= 50
                    if(fort.health < 0):
                        fort.health = 0
                    self.lastAttack = pygame.time.get_ticks()   

            if(self.health <= 0):
                fort.coins += 50
                fort.kills += 1
                self.updateAction(2)
                self.alive = False
                sound.play()

        self.updateAnimation()
        engineWindow.blit(self.image, (self.rect.x, self.rect.y))

    def updateAnimation(self):
        animationTime = 100
        self.image = self.animationList[self.action][self.frameIndex]
        if (pygame.time.get_ticks() - self.updateTime > animationTime):
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
        if(self.frameIndex >= len(self.animationList[self.action])):
            if(self.action == 2):
                self.frameIndex = len(self.animationList[self.action]) - 1
                self.kill()
            else:
                self.frameIndex = 0

    def updateAction(self, newAction : int):
        if(newAction != self.action):
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

# Buttons: #

class Button():
    def __init__(self, x : int, y : int, image : pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def drawButton(self, engineWindow : pygame.Surface):
        action = False
        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if(pygame.mouse.get_pressed()[0] == 1 and self.clicked == False):
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        engineWindow.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Towers: #

class Tower(pygame.sprite.Sprite):
    def __init__(self, firstImage : pygame.Surface, secondImage : pygame.Surface, thirdImage : pygame.Surface, x : int, y : int):
        pygame.sprite.Sprite.__init__(self)
        self.ready = False
        self.angle = 0
        self.lastShot = pygame.time.get_ticks()
        self.image = firstImage
        self.firstImage = firstImage
        self.secondImage = secondImage
        self.thirdImage = thirdImage
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self, engineWindow : pygame.Surface, fort : pygame.Surface, gameEnemies : pygame.sprite.Group, ballSprite : pygame.Surface):
        self.ready = False
        for enemy in gameEnemies:
            if(enemy.alive):
            	targetX, targetY = enemy.rect.midbottom
            	self.ready = True
            	break

        if(self.ready):
            xDistance = (targetX - self.rect.midleft[0])
            yDistance = -(targetY - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(yDistance, xDistance))
            shotCooldown = 1000
            if(pygame.time.get_ticks() - self.lastShot > shotCooldown):
                self.lastShot = pygame.time.get_ticks()
                ball = Ball(ballSprite, self.rect.midleft[0], self.rect.midleft[1]-50, self.angle)
                cannonBalls.add(ball)

        if(fort.health <= 250):
            self.image = self.thirdImage
        elif(fort.health <= 500):
            self.image = self.secondImage
        else:
            self.image = self.firstImage
        engineWindow.blit(self.image, self.rect)