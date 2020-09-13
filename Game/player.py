# -*- coding: UTF-8 -*-
import pygame
import globe
import cache
from Managers import item
from Scene import scene_gameover
from pygame.locals import *
from math import *
global resource
global cstatus
global canime


class Player(object):
	"""定义自机类: 点数, 能量值, 状态, 运动, 动画, 帧刷新"""

	def __init__(self):
		global resource						# 全局变量: 资源管理器
		global canime  						# 全局变量: 自机动画
		global cstatus  					# 全局变量: 自机状态
		resource = globe.mgame.rsmanager
		self.game_active_rect = globe.game_active_rect
		self.point = [224.0, 450.0]			# 初始化到屏幕底部中央
		self.rect = Rect(0, 0, 10, 10)		# 获取自机图像矩形遮罩

		cstatus = {}
		cstatus["normal"] = 0
		cstatus["wudi"] = 1
		cstatus["crash"] = 2
		cstatus["sc"] = 3
		cstatus["scwudi"] = 4
		cstatus["hit"] = 5
		self.status = cstatus["normal"]
		globe.cstatus = cstatus

		canime = {}
		canime["stay"] = resource.anime["player"][0]
		canime["toleft"] = resource.anime["player"][1]
		canime["toright"] = resource.anime["player"][2]
		canime["panding"] = resource.anime["player"][3]
		self.anime = canime["stay"]			# 自机动画, 初始化为 'stay' 类型
		self.aindex = 0						# 自机动画的当前播放帧, 初始化为0

		self.power = 200					# 初始化自机能量值
		self.life = 8						# 初始化自机命数
		self.frame = 0						# 初始化帧数计数器
		self.tcount = 0						# 初始化计时器

	def fire(self):
		"""定义开火动作, 维护子弹数量与频率, 自机子弹类"""
		if not globe.scgame.timestop:
			tm = globe.scgame.tmmanager
			bl = globe.scgame.blmanager
			if (self.frame % 5 == 0):
				bl.create_plbl(self.rect.inflate(-12, -8).topleft, 0)
				bl.create_plbl(self.rect.inflate(-12, -8).topright, 0)
			tp = self.power/100
			if tp >= 5:
				tp = 4
			for i in range(int(tp)):
				if (self.frame % 6 == 0):
					bl.create_plbl(tm.rect[i].center, 1)
					bl.create_plbl(tm.rect[i].center, 2)

	def throwbomb(self):
		"""定义Bomb行为, 维护Bomb设定"""
		if (self.power >= 100 and self.status != cstatus["sc"]) and (
				self.status != cstatus["scwudi"]) and (not globe.scgame.timestop):
			self.power -= 100
			self.status = cstatus["sc"]
			globe.mgame.msmanager.play_SE("wudi")

	def miss(self):
		"""定义自机中弹行为, 维护中弹行为"""
		if self.status == cstatus["hit"]:
			globe.scgame.anmanager.create_anime(resource.anime["bubble"], self.rect.topleft, 5)
			globe.scgame.blmanager.clear_enbl()
			rc = self.rect.copy()
			rc.left -= 20
			globe.scgame.itmanager.create(item.LPowerItem, rc.topleft)
			rc.left += 20
			globe.scgame.itmanager.create(item.LPowerItem, rc.midtop)
			rc.left += 20
			globe.scgame.itmanager.create(item.LPowerItem, rc.topright)

			self.status = cstatus["crash"]
			self.tmppd = [0, 0]
			self.tmppd[0] = self.point[0]
			self.tmppd[1] = self.point[1]
			self.rect.midtop = self.game_active_rect.midbottom
			self.point[0] = self.rect.centerx
			self.point[1] = self.rect.centery
			self.tcount = 0
			self.life -= 1
			self.power -= 200
			if self.power <= 0:
				self.power = 0

	def move(self):
		"""定义和控制自机移动行为, 维护移动检测函数, 高速/低速模式切换, 穿墙功能和顶上收点机能"""
		keys = self.keys
		if keys[pygame.K_z]:
			self.fire()
		if keys[pygame.K_x]:
			self.throwbomb()
		if keys[pygame.K_LSHIFT]:
			self.speed = 1.5
		else:
			self.speed = 8
		if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
			self.speed /= sqrt(2)
		if keys[pygame.K_DOWN]:
			self.point[1] += self.speed
		if keys[pygame.K_UP]:
			self.point[1] -= self.speed
		if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
			if self.anime != canime["stay"]:
				self.anime = canime["stay"]
				self.aindex = 0
		elif keys[pygame.K_RIGHT]:
			if self.anime != canime["toright"]:
				self.anime = canime["toright"]
				self.aindex = 0
			self.point[0] += self.speed
		elif keys[pygame.K_LEFT]:
			if self.anime != canime["toleft"]:
				self.anime = canime["toleft"]
				self.aindex = 0
			self.point[0] -= self.speed
		if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
			if self.anime != canime["stay"]:
				self.anime = canime["stay"]
				self.aindex = 0

		self.rect.size = self.anime[self.aindex].get_size()
		self.rect.center = (int(self.point[0]), int(self.point[1]))

		# 限位
		if self.rect.top < self.game_active_rect.top:
			self.rect.top = self.game_active_rect.top
			self.point[1] = self.rect.centery
		elif self.rect.bottom > self.game_active_rect.bottom:
			self.rect.bottom = self.game_active_rect.bottom
			self.point[1] = self.rect.centery

		# 穿墙
		if self.rect.centerx <= self.game_active_rect.left:
			self.rect.centerx = self.game_active_rect.right
			self.point[0] = self.rect.centerx
			globe.mgame.msmanager.play_SE("select")
		elif self.rect.centerx >= self.game_active_rect.right:
			self.rect.centerx = self.game_active_rect.left
			self.point[0] = self.rect.centerx
			globe.mgame.msmanager.play_SE("select")

		# 顶上收点系统
		if self.rect.top < 100:
			globe.scgame.itmanager.getitem()

		# 自动循环播放自机动画
		if self.frame % 6 == 0:
			self.aindex += 1
		if self.aindex >= len(self.anime):
			if self.anime == canime["stay"]:
				self.aindex = 0
			else:
				self.aindex -= 4

	def hit(self):
		"""定义撞弹后动作"""
		if self.status == cstatus["normal"]:
			globe.mgame.msmanager.play_SE("miss")
			self.tcount = 0
			self.status = cstatus["hit"]

	def update(self):
		"""自机刷新函数"""
		# 限制自机能量阈值为500
		if self.power > 500:
			self.power = 500
		self.keys = pygame.key.get_pressed()
		if self.status == cstatus["hit"]:
			if self.tcount >= 20:
				self.miss()
			else:
				self.tcount += 1

		if self.status != cstatus["crash"]:
			self.move()
		else:
			self.tcount += 1
			if self.life < 0 and self.tcount == 20:
				globe.hiscore = globe.scgame.high_score
				globe.mgame.call(scene_gameover.Scene_GameOver)
			if self.tcount <= 60:
				self.point[1] -= 1
			else:
				self.status = cstatus["wudi"]
				self.tcount = 0

		if self.status == cstatus["wudi"]:
			self.tcount += 1
			if self.tcount > 300:
				self.status = cstatus["normal"]
				self.tcount = 0
		elif self.status == cstatus["sc"]:
			self.tcount += 1
			if self.tcount > 360:
				self.status = cstatus["scwudi"]
				globe.scgame.blmanager.clear_enbl()
				self.tcount = 0
		elif self.status == cstatus["scwudi"]:
			self.tcount += 1
			if self.tcount > 180:
				self.status = cstatus["normal"]
				self.tcount = 0
		self.frame += 1

	def draw(self, screen):
		"""定义屏幕绘制函数"""
		self.rect.centerx = int(self.point[0])
		self.rect.centery = int(self.point[1])

		if self.status != cstatus["normal"] and self.status != cstatus["hit"]:
			tmp = cache.cache_set_alpha(self.anime[self.aindex], (int(self.frame % 15)*60/15+100), True)
			tmp = cache.cache_set_mask(tmp, (100, 0, 100, 40), True)
			screen.blit(tmp, self.rect)
		else:
			screen.blit(self.anime[self.aindex], self.rect)

		tmp = cache.cache_rotate(canime["panding"], self.frame, True)
		if self.keys[pygame.K_LSHIFT]:	
			if self.status != cstatus["crash"]:
				tprect = tmp.get_rect()
				tprect.center = self.rect.center
				screen.blit(tmp, tprect)
		if self.status == cstatus["crash"]:
			tmp.get_rect().center = self.tmppd
			screen.blit(tmp, tmp.get_rect())
