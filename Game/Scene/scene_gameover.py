# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys

import globe

from Scene import scene_title, scene_loading
from PIL import Image, ImageFilter


class PauseMenu(object):
	"""初始化菜单按钮, 设定菜单内容和淡出切换效果"""
	def __init__(self):
		"""初始化主页面及按键"""
		self.rs = globe.mgame.rsmanager.image  # rs = resource
		self.button_rect = []  						# 获取按键的 'rect' 属性
		# 一层菜单
		self.button_rect.append([100, 220])			# 定位 'To_Title_Start' 按键位置
		self.button_rect.append([90, 260])			# 定位 'Retry_Start' 按键位置

		self.image = []				# 定义按键贴图, 以列表形式存储
		self.image.append(self.rs["To_Title_Start"])		# 0
		self.image.append(self.rs["Retry_Start"])			# 1
		self.index = 0				# 初始化高亮按键: 默认为 'To_Title_Start'
		self.choose = False

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
						if self.index != 0:
							self.index -= 1
							self.button_rect[self.index][0] -= 5  # 按键微移动画
							self.button_rect[self.index + 1][0] += 5  # 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_DOWN:
						if self.index != 1:
							self.index += 1
							self.button_rect[self.index][0] -= 5  # 按键微移动画
							self.button_rect[self.index - 1][0] += 5  # 按键微移动画
							globe.mgame.msmanager.play_SE("select")

					if event.key == K_z:
						self.choose = True
						globe.mgame.msmanager.play_SE("select")
					if event.key == K_ESCAPE:
						globe.mgame.back()
		else:				# 检测进行按键选择后的状态
			if self.index == 0:
				# To title
				globe.mgame.call(scene_title.Scene_Title)
			if self.index == 1:
				# Replay
				globe.mgame.goto(scene_loading.Scene_Loading)

	def draw(self, screen):
		"""定义菜单绘制函数"""
		# 绘制 Logo 和屏幕按键

		for i in range(0, 2):  # 0, 1, 2
			screen.blit(self.image[i], self.button_rect[i])


class Scene_GameOver(object):

	def __init__(self):
		self.rs = globe.mgame.rsmanager.image  # rs = resource
		self.myfont = pygame.font.SysFont(None, 60)
		self.menu = PauseMenu()
		self.imgtmp = globe.mgame.screen.subsurface(Rect(31, 15, 386, 450)).copy()

		# 使用 'PIL' 库模糊化游戏窗口
		for i in range(0, 3):
			# 转换 PyGame 图像至 PIL 图像
			raw_str = pygame.image.tostring(self.imgtmp, "RGBA", False)
			image = Image.frombytes("RGBA", self.imgtmp.get_size(), raw_str)
			imgblur = image.filter(ImageFilter.BLUR)
			# 转换 PIL 图像至 PyGame 图像
			raw_str = imgblur.tobytes("raw", "RGBA")
			imgblur_pygame = pygame.image.fromstring(raw_str, imgblur.size, "RGBA")
			self.imgtmp = imgblur_pygame

		if globe.scgame.player.life < 0:
			# 满身疮痍
			self.title = self.rs["Dead"]
		else:
			# 演目终演
			self.title = self.rs["Clear"]

	def start(self):
		pass

	def stop(self):
		pass

	def update(self):
		self.menu.event_control()

	def draw(self, screen):
		screen.blit(self.imgtmp, (31, 16))
		screen.blit(self.title, (160, 140))
		self.menu.draw(screen)



