# -*- coding: UTF-8 -*-
import pygame

from math import *

import globe
import cache
from Managers import item

global plpoint


def bl_inter_collide(embullet):
	global plpoint
	blpoint = embullet.orbit.point
	area = embullet.bltype.area

	if type(area) == float or type(area) == int:
		if ((blpoint[0]-plpoint[0])**2+(blpoint[1]-plpoint[1])**2) < area**2:
			return True
	else:
		theta = embullet.orbit.theta
		if type(area) == pygame.Rect:
			rctuple = (area.left, area.top, area.width, area.height)
		else:
			rctuple = area
		disx = plpoint[0]-blpoint[0]
		disy = plpoint[1]-blpoint[1]
		if abs(cos(theta/180.0*pi)*disx+sin(theta/180.0*pi)*disy) < rctuple[3]/2 and abs(
				sin(theta/180.0*pi)*disx-cos(theta/180.0*pi)*disy) < rctuple[2]/2:
			return True
	return False


def bl_inter_outscr(embullet):
	blpoint = embullet.orbit.point
	if not globe.game_active_rect.inflate(50, 50).collidepoint(blpoint):
		return True


class BulletManager(object):
	#time


	#plbullet1=set of rect
	#plimg={}
	#plrc
	#plspeed

	def __init__(self):
		self.time = 0
		self.plimg = []
		self.plimg.append(cache.cache_set_alpha(
			cache.cache_rotate(globe.mgame.rsmanager.anime["player"][5], 90), 128))
		self.plimg.append(cache.cache_set_alpha(
			cache.cache_rotate(globe.mgame.rsmanager.anime["player"][6], 90), 128))
		self.plimg.append(cache.cache_set_alpha(
			cache.cache_flip(self.plimg[1]), 128))
		self.plbullet = []
		self.plrc = self.plimg[0].get_rect()
		self.plspeed = 10
		self.enbullet = set()
		global plpoint
		plpoint = globe.scgame.player.point

	def create_plbl(self, point, bltype):
		tp = self.plrc.copy()
		tp.midbottom = point
		tp.top += self.plspeed
		self.plbullet.append((tp, bltype))

	def create_enbl(self, bltype, orbit):
		self.enbullet.add(EnemyBullet(bltype, orbit))

	def update(self):
		enbl_tmp = []
		for i in self.plbullet:
			i[0].top -= self.plspeed
			if i[0].bottom < globe.game_active_rect.top:
				self.plbullet.remove(i)

		if globe.scgame.player.status == globe.cstatus["sc"]:
			for i in self.enbullet:
				i.orbit.update(i.bltype)
				if bl_inter_outscr(i):
					enbl_tmp.append(i)
		else:
			for i in self.enbullet:
				if bl_inter_collide(i):
					#globe.mgame.call(scene_menu.Scene_Menu)
					enbl_tmp.append(i)
					globe.scgame.player.hit()
				else:
					i.orbit.update(i.bltype)
					if bl_inter_outscr(i):
						enbl_tmp.append(i)

		for i in enbl_tmp:
			self.enbullet.remove(i)
		self.time += 1

	def draw(self, screen):
		for i in self.plbullet:
			screen.blit(self.plimg[i[1]], i[0])

		for i in self.enbullet:
			if i.orbit.theta != 0:
				tpimg = cache.cache_rotate(i.bltype.image, i.orbit.theta)
				tprc = tpimg.get_rect()
			else:
				tpimg = i.bltype.image
				tprc = tpimg.get_rect()
			tprc.center = i.orbit.point
			screen.blit(tpimg, tprc)

	def clear_enbl(self):
		for i in self.enbullet:
			globe.scgame.itmanager.create(item.CleanBlItem, i.orbit.point)
			globe.scgame.itmanager.getitem()
		for i in globe.scgame.enmanager.enemy:
			if i.health*0.2 <= 2000:
				i.health -= 2000
			else:
				i.health *= 0.8
		self.enbullet.clear()


class EnemyBullet(object):
	def __init__(self, bltype, orbit):
		self.bltype = bltype
		self.orbit = orbit


class BulletType(object):
	def __init__(self, img, area):
		self.image = img
		self.area = area
		self.rect = img.get_rect()

