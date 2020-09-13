# -*- coding: UTF-8 -*-
import pygame
import globe

global entype


class EnemyType(object):
	def __init__(self, anime, maxhealth, fbuff=None):
		#anime:
		#anime["stay"]
		#anime["left"]
		#anime["right"]
		#anime["toleft"]
		#anime["toright"]
		self.anime = anime
		self.maxhealth = maxhealth
		self.fbuff = fbuff

	def copy(self):
		return EnemyType(self.anime, self.maxhealth, self.fbuff)

	def buff(self, point):
		if self.fbuff != None:
			self.fbuff(point)


class Enemy(object):
	def __init__(self, entype, orbit, oristatus, bump=False, wdtime=0):
		self.entype = entype
		self.orbit = orbit
		self.health = self.entype.maxhealth

		if type(self.entype.anime) == dict:
			self.image = self.entype.anime["stay"][0]
			self.rect = self.image.get_rect()
			self.rect.center = orbit.point
		elif type(self.entype.anime) == pygame.Surface:
			self.image = self.entype.anime
			self.rect = self.image.get_rect()
			self.rect.center = orbit.point
		self.frame = 0
		self.status = oristatus
		self.bump = bump
		self.wdtime = wdtime
		if wdtime > 0:
			self.wudi = True
		else:
			self.wudi = False

	def crash(self):
		if not self.wudi:
			if self.health <= 0 and self.status == globe.enstatus["normal"]:
				self.entype.buff(self.orbit.point)
			self.status = globe.enstatus["dead"]

	def tishu(self):
		if self.bump == False:
			self.health = 0
			self.crash()
		elif self.bump == True:
			globe.scgame.player.hit()
		elif self.bump == None:
			pass

class Boss(object): #Single Object
	def __init__(self, entypes, orbits, callbacks, oristatus, life=2, bump=True, wdtime=0):
		self.life = life
		self.entypes = entypes
		self.orbits = orbits
		self.status = oristatus
		self.callbacks = callbacks
		self.bump = bump
		self.wdtime = wdtime
		self.entype = entypes[0]
		self.orbit = orbits[0]
		self.index = 0
		self.frame = 0

		if type(self.entype.anime) == dict:
			self.image = self.entype.anime["stay"][0]
			self.rect = self.image.get_rect()
			self.rect.center = self.orbit.point
		elif type(self.entype.anime) == pygame.Surface:
			self.image = self.entype.anime
			self.rect = self.image.get_rect()
			self.rect.center = orbit.point

		if wdtime > 0:
			self.wudi = True
		else:
			self.wudi = False
		self.health = self.entype.maxhealth

	def crash(self):
		if self.wudi == False:
			if self.health <= 0 and self.status == globe.enstatus["normal"]:
				self.entype.buff(self.orbit.point)
			if self.life > 0:
				self.frame = 0
				self.index += 1
				self.entype = self.entypes[self.index]
				self.orbit = self.orbits[self.index]
				self.health = self.entype.maxhealth
				if self.callbacks[self.index] != None:
					self.callbacks[self.index](self)


class EnemyManager(object):
	def __init__(self):
		global entype
		self.frame = 0
		enstatus = {}
		enstatus["normal"] = 0
		enstatus["wudi"] = 1
		enstatus["dead"] = 2
		enstatus["del"] = 3
		globe.enstatus = enstatus

		self.enemy = []
		res = globe.mgame.rsmanager.anime
		entype = {}
		for i in range(8):
			tp = "sprite"+str(i)
			anime = {}
			anime["stay"] = res["enemy"][i][0]
			anime["toright"] = res["enemy"][i][1]
			anime["right"] = res["enemy"][i][2]
			anime["toleft"] = res["enemy"][i][3]
			anime["left"] = res["enemy"][i][4]
			entype[tp] = EnemyType(anime,6000)
		anime = {}
		anime["stay"] = res["enemy"][8]
		entype["butterfly"] = EnemyType(anime,60000)
		for i in range(4):
			tp = "maoyu" + str(i)
			entype[tp] = EnemyType(res["enemy"][9+i], 6000)

		for i in range(4):
			tp = "guihuo"+str(i)
			anime = {}
			anime["stay"] = res["enemy2"][i]
			entype[tp] = EnemyType(anime, 6000)

		anime = {}
		anime["stay"] = res["cirno"][0]
		anime["toleft"] = res["cirno"][1]
		anime["toright"] = res["cirno"][2]
		entype["cirno"] = EnemyType(anime, 0)

		globe.entype = entype


	def create_enemy(self, entype, orbit, oristatus=0, bump=False, wdtime=0):
		tp = Enemy(entype, orbit, oristatus, bump, wdtime)
		self.enemy.append(tp)
		return tp

	def create_boss(self, entypes, orbits, callbacks, oristatus=0, life=2, bump=True, wdtime=0):
		tp = Boss(entypes, orbits, callbacks, oristatus, life, bump, wdtime)
		self.enemy.append(tp)
		return tp

	def update(self):
		if globe.scgame.player.power >= 500:
			damage = 700
		else:
			damage = 550+int((globe.scgame.player.power % 100)*20)
		for i in self.enemy:
			if i.orbit.update != None:
				i.orbit.update(i)
			if i.wudi == True:
				i.wdtime -= 1
				if i.wdtime <= 0:
					i.wudi = False
			if i.status == globe.enstatus["normal"]:
				if i.rect.collidepoint(globe.scgame.player.point):
					i.tishu()
				else:
					for j in globe.scgame.blmanager.plbullet:
						if j[0].colliderect(i.rect) and i.status == globe.enstatus["normal"]:
							globe.scgame.blmanager.plbullet.remove(j)
							globe.scgame.score += damage
							if not i.wudi:
								i.health -= damage
								if i.health <= 0:
									i.crash()
		self.frame += 1
		for i in self.enemy:
			if i.status == globe.enstatus["del"]:
				self.enemy.remove(i)

	def draw(self, screen):
		for i in self.enemy:
			if (i.status != globe.enstatus["del"]) and (i.status != globe.enstatus["dead"]):
				screen.blit(i.image, i.rect)