# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys
import globe
from Scene import scene_menu_confirm
from PIL import Image, ImageFilter

# 定义了全局变量: globe.scene_menu_choose, 用于指示暂停菜单的首层选定状况
# 定义了全局变量: globe.scene_menu_flag, 用于向第二层暂停菜单传递首层暂停菜单的选定项
# 这两个全局变量只在 "scene_menu_confirm.py" 中被使用.


class PauseMenu(object):
	"""初始化菜单按钮, 设定菜单内容和淡出切换效果"""
	def __init__(self):
		"""初始化主页面及按键"""
		self.button_rect = []  						# 获取按键的 'rect' 属性
		self.rs = globe.mgame.rsmanager.image		# rs = resource
		self.pause_title = self.rs["menu_title"]
		self.confirm_title = self.rs["confirm_title"]

		# 一层菜单
		self.button_rect.append([100, 220])			# 定位 'Resume_Start' 按键位置
		self.button_rect.append([100, 260])			# 定位 'To_Title_Start' 按键位置
		self.button_rect.append([90, 300])			# 定位 'Retry_Start' 按键位置
		# 二层菜单
		self.button_rect.append([100, 240])				# 定位二层菜单中 'Yes' 按键位置
		self.button_rect.append([100, 280])				# 定位二层菜单中 'No' 按键位置

		self.image = []				# 定义按键贴图, 以列表形式存储
		self.image.append(self.rs["Resume_Start"])			# 0
		self.image.append(self.rs["To_Title_Start"])		# 1
		self.image.append(self.rs["Retry_Start"])			# 2
		# depth = 2
		self.image.append(self.rs["Yes"])		# 3
		self.image.append(self.rs["No"])		# 4

		self.index = 0				# 初始化高亮按键: 默认为 'Resume_Start'
		self.flag = 0				# 一级菜单类型指示器
		globe.scene_menu_choose = False  # 初始化按键选定状态

	def event_control(self):
		"""事件控制函数"""
		if not globe.scene_menu_choose:
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
						if self.index != 2:
							self.index += 1
							self.button_rect[self.index][0] -= 5  # 按键微移动画
							self.button_rect[self.index - 1][0] += 5  # 按键微移动画
							globe.mgame.msmanager.play_SE("select")

					if event.key == K_z:
						globe.scene_menu_choose = True
						globe.mgame.msmanager.play_SE("select")
					if event.key == K_ESCAPE:
						globe.mgame.back()
		else:				# 检测进行按键选择后的状态
			if self.index == 0:
				# 返回游戏
				globe.mgame.back()
			if self.index == 1:
				globe.scene_menu_flag = 1
				globe.mgame.call(scene_menu_confirm.Scene_Menu_Confirm)

			if self.index == 2:
				globe.scene_menu_flag = 2
				globe.mgame.call(scene_menu_confirm.Scene_Menu_Confirm)

	def draw(self, screen):
		"""定义菜单绘制函数"""
		# 绘制 Logo 和屏幕按键
		screen.blit(self.pause_title, (160, 140))
		for i in range(0, 3):  # 0, 1, 2
			screen.blit(self.image[i], self.button_rect[i])


class Scene_Menu(object):
	"""定义暂停菜单页面类"""
	def __init__(self):
		"""初始化暂停菜单页面"""
		self.rs = globe.mgame.rsmanager
		self.menu = PauseMenu()
		self.count = 0			# 图像模糊处理循环标记符, 初始化为 0
		self.fade = pygame.Surface(globe.mgame.screen.get_size())
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
			globe.game_active_bg_blured = imgblur_pygame

	def update(self):
		"""主页面屏幕更新函数"""
		self.menu.event_control()

	def draw(self, screen):
		"""绘制背景"""
		screen.blit(self.imgtmp, (31, 16))
		self.menu.draw(screen)

	def start(self):
		pass

	def stop(self):
		pass
