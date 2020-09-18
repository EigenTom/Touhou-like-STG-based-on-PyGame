# -*- coding: UTF-8 -*-
from math import *
import globe
import cache


class StraightBullet(object):
	def __init__(self, point, theta, speed, bltype):
		self.theta = theta
		self.speed = speed
		self.point = [0, 0]
		self.point[0] = point[0]
		self.point[1] = point[1]

	def update(self, bltype):
		self.point[0] += self.speed*cos((self.theta+90)/180.0*pi)
		self.point[1] -= self.speed*sin((self.theta+90)/180.0*pi)


class SelfSniper(object):
	def __init__(self, point, speed, bltype):
		self.point = [0, 0]
		self.point[0] = point[0]
		self.point[1] = point[1]

		plpt = globe.scgame.player.point

		dx = plpt[0]-point[0]
		dy = plpt[1]-point[1]
		dis = sqrt(dx**2+dy**2)

		if dis == 0:
			dis = 1

		self.speedx = speed*dx/dis
		self.speedy = speed*dy/dis

		if dx > 0:
			self.theta = -asin(dy/dis)*180/pi-90
		else:
			self.theta = asin(dy/dis)*180/pi-180-90

	def update(self, bltype):
		self.point[0] += self.speedx
		self.point[1] += self.speedy

	def gettheta(self):
		return self.theta


class EnemyBase(object):
	def update(self, enemy):
		self.frame = enemy.frame
		if enemy.status == globe.enstatus["dead"] and globe.BOSSING == False:
			enemy.status = globe.enstatus["del"]
			globe.scgame.anmanager.create_anime(globe.mgame.rsmanager.anime["bubble"], enemy.rect.topleft, 5)
		else:
			if not globe.game_active_rect.inflate(64, 64).collidepoint(self.point):
				enemy.status = globe.enstatus["del"]
		self.update_orbit()
		self.update_enemy(enemy)
		self.create_bullet(self)
		enemy.frame += 1


class StraightEnemy(EnemyBase):
	def copy(self):
		tmp = StraightEnemy(self.point, self.speed[0], self.speed[1])
		tmp.create_bullet = self.create_bullet
		return tmp

	def __init__(self, point, speedx, speedy):
		self.point = [0, 0]
		self.point[0] = point[0]
		self.point[1] = point[1]
		self.speed = (speedx, speedy)

	def update_enemy(self, enemy):
		tp = enemy.entype.anime["stay"]
		enemy.image = tp[int(enemy.frame/5) % len(tp)]
		enemy.rect = enemy.image.get_rect()
		enemy.rect.center = self.point

	def update_orbit(self):
		self.point[0] += self.speed[0]
		self.point[1] += self.speed[1]


class L1P3_StraightStopEnemy(EnemyBase):
	def copy(self):
		tmp = L1P3_StraightStopEnemy(self.fr, self.tg, self.v, self.wtime)
		tmp.create_bullet = self.create_bullet
		return tmp

	def __init__(self, p1, p2, speed, time):
		self.point = [p1[0], p1[1]]
		self.fr = p1
		self.tg = p2
		dist = sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
		if dist == 0:
			dist = 1
		self.v = speed
		self.speed = (speed*(p2[0]-p1[0])/dist, speed*(p2[1]-p1[1])/dist)

		self.proc = 0
		self.wtime = time
		self.tcount = 0

	def refresh(self):
		self.point = [self.fr[0], self.fr[1]]
		dist = sqrt((self.fr[0]-self.tg[0])**2+(self.fr[1]-self.tg[1])**2)
		if dist == 0:
			dist = 1
		self.speed = (self.v*(self.tg[0]-self.fr[0])/dist, self.v*(self.tg[1]-self.fr[1])/dist)
		self.proc = 0
		self.tcount = 0

	def update_enemy(self, enemy):
		tp = enemy.entype.anime["stay"]
		enemy.image = tp[int(enemy.frame/5) % len(tp)]
		enemy.rect = enemy.image.get_rect()
		enemy.rect.center = self.point

	def update_orbit(self):
		if self.proc == 0:
			if (self.point[0]-self.tg[0])**2+(self.point[1]-self.tg[1])**2 < self.v**2:
				self.proc = 1
			else:
				self.point[0] += self.speed[0]
				self.point[1] += self.speed[1]
		elif self.proc == 1:
			self.tcount += 1
			if self.tcount >= self.wtime:
				self.proc = 2
		elif self.proc == 2:
			self.point[0] -= self.speed[0]
			self.point[1] -= self.speed[1]


class L1P1_CurveVert(EnemyBase):
	def copy(self):
		tmp = type(self)(self.p1, self.p2, self.speed)
		tmp.create_bullet = self.create_bullet
		return tmp

	def __init__(self, p1, p2, speed):
		self.point = [0, 0]
		self.point[0] = p1[0]
		self.point[1] = p1[1]
		self.p1 = p1
		self.p2 = p2
		self.speed = speed

		if p1[1] < p2[1]:
			self.updown = 1
		else:
			self.updown = -1

		if p1[0] < p2[0]:
			self.leftright = 1
		else:
			self.leftright = -1

		self.radius = abs(p2[0]-p1[0])
		self.status = 0
		self.wspeed = speed*1.0/self.radius
		self.theta = 0

		self.create_bullet = None

	def update_orbit(self):
		if self.status == 0:
			self.point[1] += self.updown*self.speed
			if (self.point[1]-self.p2[1])*self.updown >= 0:
				self.status = 1
		elif self.status == 1:
			self.theta += self.wspeed
			self.point[0] = self.p2[0]+self.leftright*self.radius*cos(self.theta+pi)
			self.point[1] = self.p2[1]+self.updown*self.radius*sin(self.theta)

			if (self.point[0]-self.p2[0])*self.leftright >= 0:
				self.status = 2

		elif self.status == 2:
			self.point[0] += self.leftright*self.speed

	def update_enemy(self, enemy):
		pass


class L1P1_CurveVertMaoyu(L1P1_CurveVert):
	def update_enemy(self, enemy):
		enemy.image = cache.cache_rotate(enemy.entype.anime, enemy.frame*18)
		enemy.rect = enemy.image.get_rect()
		enemy.rect.center = self.point


class L1P4_DeadSprite(EnemyBase):
	def copy(self):
		tmp = L1P4_DeadSprite(self.point, self.delay1, self.delay2)
		tmp.create_bullet = self.create_bullet
		tmp.kill = self.kill
		return tmp

	def __init__(self, point, delay1, delay2):
		self.point = point
		self.delay1 = delay1
		self.delay2 = delay2
		self.mtheta = 0
		self.kill = False

	def update(self, enemy):
		self.frame = enemy.frame
		self.status = enemy.status
		if enemy.status == globe.enstatus["dead"]:
			if self.frame-self.delay1 >= self.delay2:
				enemy.status = globe.enstatus["del"]
		if enemy.health <= 0 and self.kill == False:
			self.frame = self.delay1
			enemy.frame = self.delay1
			self.kill = True
		self.update_orbit()
		self.update_enemy(enemy)
		self.create_bullet(self)
		enemy.frame += 1

	def update_orbit(self):
		pass

	def update_enemy(self, enemy):
		tp = enemy.entype.anime["stay"]
		enemy.image = tp[int(enemy.frame/3) % len(tp)]
		enemy.rect = enemy.image.get_rect()
		enemy.rect.center = self.point
		if self.frame >= self.delay1:
			if self.frame == self.delay1:
				globe.scgame.anmanager.create_anime(globe.mgame.rsmanager.anime["bubble"], enemy.rect.topleft, 5)
				enemy.crash()
			self.create_bullet(self)


class L1BossRunInto(L1P3_StraightStopEnemy):
	def update_enemy(self, enemy):
		if self.proc == 0:
			tp = enemy.entype.anime["toleft"]
			enemy.image = tp[int(enemy.frame/10) % len(tp)]
			enemy.rect = enemy.image.get_rect()
			enemy.rect.center = self.point
		else:
			tp = enemy.entype.anime["stay"]
			enemy.image = tp[int(enemy.frame/10) % len(tp)]
			enemy.rect = enemy.image.get_rect()
			enemy.rect.center = self.point

	def update_orbit(self):
		if self.proc == 0:
			if (self.point[0]-self.tg[0])**2+(self.point[1]-self.tg[1])**2 < self.v**2:
				self.proc = 1
			else:
				self.point[0] += self.speed[0]
				self.point[1] += self.speed[1]


class L1BossNSC1(EnemyBase):
	def update(self, enemy):
		self.frame = enemy.frame
		if enemy.status == globe.enstatus["dead"]:
			enemy.status = globe.enstatus["del"]
		else:
			if globe.game_active_rect.inflate(64,64).collidepoint(self.point) == False:
				enemy.status = globe.enstatus["del"]
		self.update_orbit()
		self.update_enemy(enemy)
		self.create_bullet(self)
		enemy.frame += 1

	def update_orbit(self):
		pass

	def update_enemy(self, enemy):
		tp = enemy.entype.anime["stay"]
		enemy.image = tp[int(enemy.frame/10) % len(tp)]
		enemy.rect = enemy.image.get_rect()
		enemy.rect.center = self.point


def quickcreate(id, **arg):
	if id == 0:
		return StraightBullet(arg["point"], arg["theta"], arg["speed"], arg["bltype"])
	if id == 1:
		return SelfSniper(arg["point"], arg["speed"], arg["bltype"])

	if id == 101:
		return StraightEnemy(arg["point"], arg["speedx"], arg["speedy"])
	if id == 102:
		return L1P1_CurveVertMaoyu(arg["p1"], arg["p2"], arg["speed"])
	if id == 103:
		return L1P3_StraightStopEnemy(arg["p1"], arg["p2"], arg["speed"], arg["time"])
	if id == 104:
		return L1P4_DeadSprite(arg["point"], arg["delay1"], arg["delay2"])