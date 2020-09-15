# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys
import globe
from Scene import scene_menu, scene_title
from PIL import Image, ImageFilter


class PauseMenu_Confirm(object):
	"""初始化菜单按钮, 设定菜单内容和淡出切换效果"""
	def __init__(self):
		"""初始化主页面及按键"""
		self.button_rect = []  						# 获取按键的 'rect' 属性
		self.rs = globe.mgame.rsmanager.image		# rs = resource
		self.confirm_title = self.rs["confirm_title"]

		# 二层菜单
		self.button_rect.append([170, 240])				# 定位二层菜单中 'Yes' 按键位置
		self.button_rect.append([170, 280])				# 定位二层菜单中 'No' 按键位置

		self.image = []				# 定义按键贴图, 以列表形式存储
		self.image.append(self.rs["Yes"])		# 0
		self.image.append(self.rs["No"])		# 1

		self.index = 1				# 初始化高亮按键: 默认为 'No'
		self.choose = False			# 初始化按键选定状态

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
						globe.scene_menu_choose = False
						globe.mgame.back()
		else:				# 检测进行按键选择后的状态
			if self.index == 0:
				if globe.scene_menu_flag == 1:
					globe.mgame.call(scene_title.Scene_Title)
				elif globe.scene_menu_flag == 2:
					globe.scene_menu_choose = False
					globe.scgame.__init__()
					globe.scgame.update()
					globe.mgame.back()
					globe.mgame.back()
			if self.index == 1:
				globe.scene_menu_choose = False
				globe.mgame.screen.blit(globe.game_active_bg_blured, (31, 16))
				globe.mgame.back()

	def draw(self, screen):
		"""定义菜单绘制函数"""
		screen.blit(globe.game_active_bg_blured, (31, 16))
		# 绘制 Logo 和屏幕按键
		screen.blit(self.confirm_title, (160, 180))
		for i in range(0, 2):		# 0, 1
			screen.blit(self.image[i], self.button_rect[i])


class Scene_Menu_Confirm(object):
	"""定义暂停菜单页面类"""
	def __init__(self):
		"""初始化暂停菜单页面"""
		self.rs = globe.mgame.rsmanager
		self.menu = PauseMenu_Confirm()
		self.fade = pygame.Surface(globe.mgame.screen.get_size())
		self.imtmp = globe.mgame.screen.subsurface(Rect(31, 15, 386, 450)).copy()

	def update(self):
		"""主页面屏幕更新函数"""
		self.menu.event_control()

	def draw(self, screen):
		"""绘制背景"""


		# screen.blit(globe.mgame.scene_menu.imtmp, (31, 16))
		self.menu.draw(screen)

	def start(self):
		pass

	def stop(self):
		pass