# -*- coding: UTF-8 -*-
import pygame
import sys
from Scene import scene_game
import globe
from random import *

maples = []
clock = pygame.time.Clock()
print(sys.path)


class Scene_Loading(object):
	screen = pygame.display.set_mode((640, 480))
	res = pygame.image.load("./Resources/pic/New/ascii/loading.png").convert_alpha()
	loading = res.subsurface(4, 0, 124, 57)

	def __init__(self):
		self.count = 0
		# 设定页面切换效果: 淡出
		self.fade = pygame.Surface(globe.mgame.screen.get_size())  # 设定遮罩尺寸
		self.fade.fill((0, 0, 0))  # 以纯黑色填充遮罩

		# bg = pygame.image.load().convert_alpha()

	def draw(self, screen):
		screen.blit(self.fade, (0, 0))
		for maple in maples:
			now = maple.image
			nowRect = now.get_rect()
			new = pygame.transform.rotate(now, maple.rinit)
			newRect = new.get_rect(center=nowRect.center)
			newRect.center = (maple.rect.x, maple.rect.y)
			screen.blit(new, newRect)
		screen.blit(self.loading, [460, 380])
		if self.count >= 120:
			self.fade.set_alpha((self.count - 120) * 12)  # 对黑色遮罩进行透明化
			screen.blit(self.fade, (0, 0))

	def update(self):
		pygame.init()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			else:
				pass
		if (self.count % 13 == 0) and (len(maples) <= 10):
			maple = Maple()
			print(maple)
			maples.append(maple)
		maple_update()
		self.count += 1
		if self.count >= 150:
			globe.mgame.goto(scene_game.Scene_Game)

class Maple(object):

	def __init__(self):
		self.xspeed = 2*random()
		self.yspeed = 1
		self.rinit = 1
		self.rspeed = randint(1, 6)
		self.image = Scene_Loading.res.subsurface(0, 64, 33, 33)
		self.rect = self.image.get_rect()
		self.rect.x = randint(460, 520)
		self.rect.y = 360.0


def maple_update():
	for maple in maples:
		maple.rinit += maple.rspeed
		maple.rect.y += maple.yspeed
		maple.rect.x += maple.xspeed
		if (maple.rect.y >= 440) or (maple.rect.x >= 590) or (maple.rect.x <= 460):
			maples.remove(maple)