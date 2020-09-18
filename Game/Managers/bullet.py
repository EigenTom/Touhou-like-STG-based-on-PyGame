# -*- coding: UTF-8 -*-
import pygame

from math import *

import globe
import cache
from Managers import item

global player_point


def bullet_inter_collide(enemy_bullet):
	"""碰撞检测函数, 使用判定点间距离检测是否碰撞"""
	global player_point						
	bullet_point = enemy_bullet.orbit.point		
	area = enemy_bullet.bullet_type.area			

	if type(area) == float or type(area) == int:
		if ((bullet_point[0]-player_point[0])**2+(bullet_point[1]-player_point[1])**2) < area**2:
			return True
	else:
		theta = enemy_bullet.orbit.theta
		if type(area) == pygame.Rect:
			rctuple = (area.left, area.top, area.width, area.height)
		else:
			rctuple = area
		disx = player_point[0]-bullet_point[0]
		disy = player_point[1]-bullet_point[1]
		if abs(cos(theta/180.0*pi)*disx+sin(theta/180.0*pi)*disy) < rctuple[3]/2 and abs(
				sin(theta/180.0*pi)*disx-cos(theta/180.0*pi)*disy) < rctuple[2]/2:
			return True
	return False


def bullet_inter_outscr(enemy_bullet):
	bullet_point = enemy_bullet.orbit.point
	if not globe.game_active_rect.inflate(50, 50).collidepoint(bullet_point):
		return True


class BulletManager(object):
	"""子弹管理器, 维护子弹位置, 子弹创建和清屏"""
	def __init__(self):
		self.time = 0
		self.plimg = []
		self.plimg.append(cache.cache_set_alpha(
			cache.cache_rotate(globe.mgame.rsmanager.anime["player"][5], 90), 128))
		self.plimg.append(cache.cache_set_alpha(
			cache.cache_rotate(globe.mgame.rsmanager.anime["player"][6], 90), 128))
		self.plimg.append(cache.cache_set_alpha(
			cache.cache_flip(self.plimg[1]), 128))
		self.player_bullet = []
		self.plrc = self.plimg[0].get_rect()
		self.plspeed = 10
		self.enemy_bullet = set()
		global player_point
		player_point = globe.scgame.player.point

	def create_plbl(self, point, bullet_type):
		tp = self.plrc.copy()
		tp.midbottom = point
		tp.top += self.plspeed
		self.player_bullet.append((tp, bullet_type))

	def create_enbl(self, bullet_type, orbit):
		self.enemy_bullet.add(EnemyBullet(bullet_type, orbit))

	def update(self):
		enbl_tmp = []
		for i in self.player_bullet:
			i[0].top -= self.plspeed
			if i[0].bottom < globe.game_active_rect.top:
				self.player_bullet.remove(i)

		if globe.scgame.player.status == globe.cstatus["sc"]:
			for i in self.enemy_bullet:
				i.orbit.update(i.bullet_type)
				if bullet_inter_outscr(i):
					enbl_tmp.append(i)
		else:
			for i in self.enemy_bullet:
				if bullet_inter_collide(i):
					enbl_tmp.append(i)
					globe.scgame.player.hit()
				else:
					i.orbit.update(i.bullet_type)
					if bullet_inter_outscr(i):
						enbl_tmp.append(i)

		for i in enbl_tmp:
			self.enemy_bullet.remove(i)
		self.time += 1

	def draw(self, screen):
		"""子弹绘制函数, 维护全部的子弹绘制"""
		for i in self.player_bullet:
			screen.blit(self.plimg[i[1]], i[0])

		for i in self.enemy_bullet:
			if i.orbit.theta != 0:
				tpimg = cache.cache_rotate(i.bullet_type.image, i.orbit.theta)
				tprc = tpimg.get_rect()
			else:
				tpimg = i.bullet_type.image
				tprc = tpimg.get_rect()
			tprc.center = i.orbit.point
			screen.blit(tpimg, tprc)

	def clear_enbl(self):
		"""清屏函数"""
		for i in self.enemy_bullet:
			globe.scgame.itmanager.create(item.CleanBlItem, i.orbit.point)
			globe.scgame.itmanager.getitem()
		for i in globe.scgame.enmanager.enemy:
			if i.health*0.2 <= 2000:
				i.health -= 2000
			else:
				i.health *= 0.8
		self.enemy_bullet.clear()


class EnemyBullet(object):
	def __init__(self, bullet_type, orbit):
		self.bullet_type = bullet_type
		self.orbit = orbit


class BulletType(object):
	def __init__(self, img, area):
		self.image = img
		self.area = area
		self.rect = img.get_rect()

