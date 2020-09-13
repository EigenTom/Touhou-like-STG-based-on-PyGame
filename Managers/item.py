# -*- coding: UTF-8 -*-
import pygame
from math import *

import globe

global itstatus
global resource
global player
itstatus = {"normal": 0, "fly": 1}


class ItemManager(object):
	"""物品管理器, 维护Bonus物品属性"""
	def __init__(self):
		global resource
		global player
		resource = globe.mgame.rsmanager.image["resource"]
		player = globe.scgame.player

		self.item = set()
		self.speed = 1
		self.fspeed = 10

	def create(self, itype, point):
		"""物品创建函数"""
		tmp = itype(point)
		if tmp.rect.right >= globe.game_active_rect.right:
			tmp.rect.right = globe.game_active_rect.right
		if tmp.rect.left <= globe.game_active_rect.left:
			tmp.rect.left = globe.game_active_rect.left
		self.item.add(tmp)

	def update(self):
		tmp = []
		for i in self.item:
			if i.status == itstatus["normal"]:
				if i.frame <= 60:
					speed = self.speed*(-1)
				else:
					speed = self.speed
				i.rect.top += speed
				if i.rect.colliderect(globe.scgame.player.rect):
					i.buffer()
					tmp.append(i)
				if i.rect.top > globe.game_active_rect.bottom:
					tmp.append(i)
				if i.rect.left < globe.game_active_rect.left or i.rect.right > globe.game_active_rect.right:
					tmp.append(i)
				i.frame += 1
			else:
				dx = player.point[0] - i.rect.centerx
				dy = player.point[1] - i.rect.centery
				dist = sqrt(dx**2+dy**2)
				if dist == 0:
					dist = 0.0001
				i.vx = int(self.fspeed*dx/dist)
				i.vy = int(self.fspeed*dy/dist)
				i.rect.left += i.vx
				i.rect.top += i.vy
				if i.rect.collidepoint(player.point):
					i.buffer()
					tmp.append(i)
		for i in tmp:
			self.item.remove(i)

	def getitem(self):
		"""收点函数"""
		for i in self.item:
			i.status = itstatus["fly"]

	def draw(self, screen):
		"""绘制物品函数"""
		for i in self.item:
			screen.blit(i.image,i.rect)


class SPowerItem(object):
	"""定义并维护低点数物品类"""
	def __init__(self, point):
		self.vx = 0
		self.vy = 0
		self.image = resource[0][0]
		self.rect = self.image.get_rect()
		self.rect.center = point
		self.status = itstatus["normal"]
		self.frame = 0

	def buffer(self):
		"""定义加点数值"""
		if globe.scgame.player.power < 495:
			player.power += 5
		else:
			player.power = 500


class LPowerItem(object):
	"""定义撞弹补偿物品类"""
	def __init__(self, point):
		self.vx = 0
		self.vy = 0
		self.image = resource[2][1]
		rc = self.image.get_rect()
		rc.width = int(rc.width*0.7)
		rc.height = int(rc.height*0.7)
		self.image = pygame.transform.scale(self.image, rc.size)
		self.rect = self.image.get_rect()
		self.rect.center = point
		self.status = itstatus["normal"]
		self.frame = 0

	def buffer(self):
		"""定义加点数值"""
		if globe.scgame.player.power < 400:
			player.power += 100
		else:
			player.power = 500


class PointItem(object):
	"""定义常规落点"""
	def __init__(self, point):
		self.vx = 0
		self.vy = 0
		self.image = resource[0][1]
		self.rect = self.image.get_rect()
		self.rect.center = point
		self.status = itstatus["normal"]
		self.frame = 0

	def buffer(self):
		"""定义加点数值"""
		globe.scgame.score += 50


class LifeItem(object):
	"""定义LV up 物品"""
	def __init__(self, point):
		self.vx = 0
		self.vy = 0
		self.image = resource[3][0]
		self.rect = self.image.get_rect()
		self.rect.center = point
		self.status = itstatus["normal"]
		self.frame = 0

	def buffer(self):
		"""定义加命数值"""
		player.life += 1
		globe.mgame.msmanager.play_SE("extend")


class CleanBlItem(object):
	def __init__(self, point):
		self.vx = 0
		self.vy = 0
		self.image = resource[3][1]
		self.rect = self.image.get_rect()
		self.rect.center = point
		self.status = itstatus["normal"]
		self.frame = 0

	def buffer(self):
		"""定义加点数值"""
		globe.scgame.score += 50