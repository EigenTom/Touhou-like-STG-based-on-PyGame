# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys
import globe
from Scene import scene_loading


class TitleMenu(object):
	"""初始化菜单按钮, 设定菜单内容和淡出切换效果"""
	def __init__(self):
		"""初始化主页面及按键"""
		self.button_rect = []  						# 获取按键的 'rect' 属性
		self.logo = (pygame.image.load("./Resources/pic/New/title/title_logo.png").convert_alpha()).subsurface(0,128,324,80)
		self.rs = globe.mgame.rsmanager.image		# rs = resource

		self.button_rect.append([400, 150])			# 定位 'Game_Start' 按键位置
		self.button_rect.append([410, 185])			# 定位 'Extra_Start' 按键位置
		self.button_rect.append([420, 220])			# 定位 'Practice Start' 按键位置
		self.button_rect.append([430, 255])			# 定位 'Replay' 按键位置
		self.button_rect.append([440, 290])			# 定位 'Player Data' 按键位置
		self.button_rect.append([450, 325])			# 定位 'Music Room' 按键位置
		self.button_rect.append([460, 360])			# 定位 'Option' 按键位置
		self.button_rect.append([470, 395])			# 定位 'Quit' 按键位置

		self.image = []				# 定义按键贴图, 以列表形式存储
		self.image.append(self.rs["Game_Startb"])			# 0
		self.image.append(self.rs["Game_Startd"])			# 1
		self.image.append(self.rs["Extra_Startb"])			# 2
		self.image.append(self.rs["Extra_Startd"])			# 3
		self.image.append(self.rs["Practise_Startb"])		# 4
		self.image.append(self.rs["Practise_Startd"])		# 5
		self.image.append(self.rs["Replayb"])				# 6
		self.image.append(self.rs["Replayd"])				# 7
		self.image.append(self.rs["Player_Datab"])			# 8
		self.image.append(self.rs["Player_Datad"])			# 9
		self.image.append(self.rs["Music_Roomb"])			# 10
		self.image.append(self.rs["Music_Roomd"])			# 11
		self.image.append(self.rs["Optionb"])				# 12
		self.image.append(self.rs["Optiond"])				# 13
		self.image.append(self.rs["Quitb"])					# 14
		self.image.append(self.rs["Quitd"])					# 15

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
						if self.index != 0:
							self.index -= 1
							self.button_rect[self.index][0] -= 5				# 按键微移动画
							self.button_rect[self.index + 1][0] += 5			# 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_DOWN:
						if self.index != 7:
							self.index += 1
							self.button_rect[self.index][0] -= 5				# 按键微移动画
							self.button_rect[self.index - 1][0] += 5			# 按键微移动画
							globe.mgame.msmanager.play_SE("select")
					if event.key == K_z:
						self.choose = True
						globe.mgame.msmanager.play_SE("select")
		else:				# 检测进行按键选择后的状态
			self.flash += 1
			if self.flash >= 20:				# 按键闪烁 20 下后进行页面切换
				if self.index == 0:
					if self.flash >= 40:		# 按键闪烁 40 下后进行页面切换
						globe.mgame.goto(scene_loading.Scene_Loading)
				if self.index == 1:
					print("Extra_Start_Debug")
				if self.index == 2:
					print("Practise_Start_Debug")
				if self.index == 3:
					print("Replay_Debug")
				if self.index == 4:
					print("Player_Data_Debug")
				if self.index == 5:
					print("Music_Room_Debug")
				if self.index == 6:
					print("Option_Debug")
				if self.index == 7:
					pygame.quit()
					sys.exit()

			if (self.flash % 2) == 0 and (self.flash <= 40):		# 控制按键闪烁效果
				tmp = self.image[self.index*2]
				self.image[self.index*2] = self.image[self.index*2+1]
				self.image[self.index*2+1] = tmp

	def draw(self, screen):
		"""定义菜单绘制函数"""
		# 绘制 Logo
		screen.blit(self.logo, (32, 200))

		# 绘制屏幕按键
		for i in range(0, 8):
			screen.blit(self.image[2*i + 1], self.button_rect[i])
		screen.blit(self.image[2*self.index], self.button_rect[self.index])

		# 定义淡出效果遮罩循环
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