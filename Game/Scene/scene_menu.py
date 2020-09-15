# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys
import globe
from Scene import scene_loading
from Scene import scene_title
from PIL import Image, ImageFilter




class PauseMenu(object):
	"""初始化菜单按钮, 设定菜单内容和淡出切换效果"""
	def __init__(self):
		"""初始化主页面及按键"""
		self.button_rect = []  						# 获取按键的 'rect' 属性
		self.pause_logo = (pygame.image.load("./Resources/pic/New/ascii/pause.png").convert_alpha()).subsurface(0,0,128,32)
		self.rs = globe.mgame.rsmanager.image		# rs = resource

		self.button_rect.append([100, 220])			# 定位 'Game_Start' 按键位置
		self.button_rect.append([100, 260])			# 定位 'Extra_Start' 按键位置
		self.button_rect.append([90, 300])			# 定位 'Practice Start' 按键位置

		self.image = []				# 定义按键贴图, 以列表形式存储
		self.image.append(self.rs["Resume_Start"])			# 0
		self.image.append(self.rs["To_Title_Start"])			# 1
		self.image.append(self.rs["Retry_Start"])			# 2

		self.index = 0				# 初始化高亮按键: 默认为 'Resume_Start'
		self.choose = False			# 初始化按键选定状态
		self.flash = 0				# 初始化按键闪烁帧
		self.count = 0

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
							self.button_rect[self.index][0] -= 5				# 按键微移动画
							self.button_rect[self.index + 1][0] += 5			# 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_DOWN:
						if self.index != 2:
							self.index += 1
							self.button_rect[self.index][0] -= 5				# 按键微移动画
							self.button_rect[self.index - 1][0] += 5			# 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_z:
						self.choose = True
						globe.mgame.msmanager.play_SE("select")
					if event.key == K_ESCAPE:
						globe.mgame.back()
		else:				# 检测进行按键选择后的状态
			self.flash += 1
			if self.flash >= 20:				# 按键闪烁 20 下后进行页面切换
				if self.index == 0:
					if self.flash >= 40:		# 按键闪烁 40 下后进行页面切换
						# 返回游戏
						globe.mgame.back()
				if self.index == 1:
					globe.mgame.call(scene_title.Scene_Title)
				if self.index == 2:
					globe.scgame.__init__()
					globe.scgame.update()
					globe.mgame.back()



	def draw(self, screen):
		"""定义菜单绘制函数"""
		# 绘制 Logo
		screen.blit(self.pause_logo, (160, 140))

		# 绘制屏幕按键
		for i in range(0, 3):
			screen.blit(self.image[i], self.button_rect[i])


class Scene_Menu(object):
	"""定义主页面类"""
	def __init__(self):
		"""初始化主页面"""
		self.rs = globe.mgame.rsmanager
		self.menu = PauseMenu()
		self.count = 0
		self.fade = pygame.Surface(globe.mgame.screen.get_size())
		self.imtmp = globe.mgame.screen.subsurface(Rect(31, 15, 386, 450)).copy()



	def update(self):
		"""主页面屏幕更新函数"""
		self.menu.event_control()

	def draw(self, screen):
		"""绘制背景"""


		if self.count <= 3:
			# imtmp = globe.mgame.screen.subsurface(globe.game_active_rect).copy()
			# 转换pygame 图像至 pil
			raw_str = pygame.image.tostring(self.imtmp, "RGBA", False)
			image = Image.frombytes("RGBA", self.imtmp.get_size(), raw_str)
			imblur = image.filter(ImageFilter.BLUR)

			raw_str = imblur.tobytes("raw", "RGBA")
			imblur_pygame = pygame.image.fromstring(raw_str, imblur.size, "RGBA")
			self.imtmp = imblur_pygame
		self.count += 1
		screen.blit(self.imtmp, (31, 16))
		self.menu.draw(screen)

	def start(self):
		pass

	def stop(self):
		pass