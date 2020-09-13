# -*- coding: UTF-8 -*-
import player
from Managers import background, enemy, bullet, animation, item, tama
from Data import dialogue
from Scene.hud import *
from Scene import scene_menu

from Data.Levels import level1


class Scene_Game(object):
	"""定义并维护游戏场景类"""
	def __init__(self):
		globe.scgame = self					# scgame = SceneGame
		self.rs = globe.mgame.rsmanager		# rs = Resource
		globe.game_active_rect = Rect(32, 16, 384, 448)			# 确定活动的屏幕区域
		self.hud = Hud()					# 初始化游戏信息显示区域
		self.time = -60
		self.player = player.Player()		# 定义自机
		self.player.power = 200				# 定义自机初始状态之点数
		self.bgmanager = background.BackgroundManager()			# 定义背景图管理器
		self.itmanager = item.ItemManager()						# 定义贴图管理器
		self.tmmanager = tama.TamaManager()						# 定义僚机管理器
		self.blmanager = bullet.BulletManager()					# 定义子弹管理器
		self.anmanager = animation.AnimeManager()				# 定义动画管理器
		self.enmanager = enemy.EnemyManager()					# 定义敌机管理器
		self.txplayer= dialogue.TextPlayer()						# 定义对话播放器
		self.score = 0							# 初始得点数为零
		self.high_score = globe.high_score		# 传入累计最高点数
		print(globe.high_score)					# Debug: 输出累计最高点数
		self.pause = False						# 初始化: 终止游戏为假
		self.timestop = False					# 初始化: 暂停游戏为假
		globe.BOSSING = False					# 初始化: BOSS战为假

		level1.init()							# 进入一面
	# 	#globe.mgame.msmanager.play_BGM("abc.mp3")

	def stop(self):
		"""终止游戏"""
		self.pause = True

	def start(self):
		"""开始游戏"""
		self.pause = False

	def tstop(self):
		"""暂停游戏"""
		self.timestop = True

	def tstart(self):
		"""继续游戏"""
		self.timestop = False

	def update(self):
		"""定义更新函数"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
					pygame.quit()
					sys.exit()
				elif event.key == pygame.K_ESCAPE:
					globe.mgame.msmanager.play_SE("pause")
					globe.mgame.call(scene_menu.Scene_Menu)
				elif event.key == K_z and self.timestop:
					self.txplayer.command("next")
		if not self.pause:
			self.bgmanager.update()
			self.player.update()
			self.itmanager.update()
			self.tmmanager.update()
			self.blmanager.update()
			self.anmanager.update()
			self.enmanager.update()
			level1.update(self.time)							# LV1
			if not self.timestop:
				self.time += 1
			else:
				self.txplayer.update()

	def draw(self, screen):
		screen.fill((255, 255, 255))
		self.bgmanager.draw(screen)
		self.itmanager.draw(screen)
		self.enmanager.draw(screen)
		self.player.draw(screen)
		self.tmmanager.draw(screen)
		self.anmanager.draw(screen)
		self.blmanager.draw(screen)
		self.hud.draw(screen)

		if self.timestop:
			self.txplayer.draw(screen)
