# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys
import globe
from Scene import scene_loading
count = 0


class TitleMenu(object):
	"""初始化菜单按钮, 设定菜单内容和淡出切换效果"""
	def __init__(self):
		"""初始化主页面及按键"""
		self.button_rect = []  						# 获取按键的 'rect' 属性
		self.rs = globe.mgame.rsmanager.image		# rs = resource
		self.button_rect.append([280, 320])			# 定位 'Start' 按键位置
		self.button_rect.append([280, 360])			# 定位 'Quit' 按键位置
		"""
		self.button_rect.append([, ])
		self.button_rect.append([, ])
		"""

		self.image = []				# 定义按键贴图, 以列表形式存储
		self.image.append(self.rs["startb"])
		self.image.append(self.rs["startd"])
		self.image.append(self.rs["quitb"])
		self.image.append(self.rs["quitd"])
		"""
		self.image.append(self.rs["settingb"])
		self.image.append(self.rs["settingd"])
		self.image.append(self.rs["highscoreb"])
		self.image.append(self.rs["highscored"])
		self.image.append(self.rs["musicroomb"])
		self.image.append(self.rs["musicroomd"])
		"""

		self.index = 0				# 初始化高亮按键: 默认为 'Start'
		self.choose = False			# 初始化按键选定状态

		self.flash = 0				# 初始化按键闪烁帧

		# 设定页面切换效果: 淡出
		self.fade = pygame.Surface(globe.mgame.screen.get_size())		# 设定遮罩尺寸
		self.fade.fill((0, 0, 0))		# 以纯黑色填充遮罩

	def event_control(self):
		"""事件控制函数"""
		if not self.choose:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
						pygame.quit()
						sys.exit()
					if event.key == K_UP:
						if self.index == 1:
							self.index = 0
							self.button_rect[0][0] -= 5				# 按键微移动画
							self.button_rect[1][0] += 5				# 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_DOWN:
						if self.index == 0:
							self.index = 1
							self.button_rect[0][0] += 5				# 按键微移动画
							self.button_rect[1][0] -= 5				# 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_z:
						self.choose = True
						globe.mgame.msmanager.play_SE("select")
		else:				# 检测进行按键选择后的状态
			self.flash += 1
			if self.flash >= 20:				# 按键闪烁 20 下后进行页面切换
				if self.index == 1:
					pygame.quit()
					sys.exit()
				else:
					if self.flash >= 40:		# 按键闪烁 40 下后进行页面切换
						globe.mgame.goto(scene_loading.Scene_Loading)
			if (self.flash % 2) == 0 and (self.flash <= 40):		# 控制按键闪烁效果
				tmp = self.image[self.index*2]
				self.image[self.index*2] = self.image[self.index*2+1]
				self.image[self.index*2+1] = tmp

	def draw(self, screen):
		"""定义菜单绘制函数"""
		screen.blit(self.image[self.index], self.button_rect[0])
		screen.blit(self.image[3-self.index], self.button_rect[1])
		if self.flash >= 20:
			self.fade.set_alpha((self.flash-20)*12)			# 对黑色遮罩进行透明化
			screen.blit(self.fade, (0, 0))					# 在屏幕上绘制半透明遮罩模拟淡出效果


class Scene_Title(object):
	"""定义主页面类"""
	def __init__(self):
		"""初始化主页面"""
		self.rs = globe.mgame.rsmanager
		self.menu = TitleMenu()
		self.count = 0
		self.fade = pygame.Surface(globe.mgame.screen.get_size())
	def update(self):
		"""主页面屏幕更新函数"""

		self.menu.event_control()

	def draw(self, screen):
		"""绘制背景"""
		screen.blit(self.rs.image["background"], (0, 0))
		self.menu.draw(screen)

		# 淡入效果 
		if self.count <= 40:
			self.fade.set_alpha((255 - (self.count) * 12))  # 对黑色遮罩进行透明化
			screen.blit(self.fade, (0, 0))
			self.count += 1