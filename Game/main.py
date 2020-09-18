# -*- coding: UTF-8 -*-
import pygame
import Managers.resource  	# 导入贴图资源
import globe				# 设定全局变量
import cache				# 导入贴图缓存
from Managers import music
from Scene import scene_init


class Main_Window(object):
	"""定义游戏窗口类"""

	def __init__(self):
		"""定义部分静态窗口属性"""
		# pygame.display.set_icon("")
		pygame.display.set_caption("迫真STG")
		# self.screen = pygame.display.set_mode([640, 480])
		self.screen = pygame.display.set_mode([640, 480], pygame.DOUBLEBUF | pygame.NOFRAME)#pygame.FULLSCREEN) 	# 全屏运行
		self.clock = pygame.time.Clock()
		self.stack = []							# 定义界面栈, 防止scene函数重复调用
		globe.high_score = 0

	def init(self):
		"""初始化函数"""
		pygame.init()							# 初始化游戏窗口
		pygame.mixer.init()						# 初始化混响器(音频支持)
		cache.cache_init()						# 初始化图像缓存
		self.rsmanager = Managers.resource.Resource()		# 定位贴图资源管理器
		self.msmanager = music.MusicManager()				# 定位音频管理器
		self.myfont = pygame.font.SysFont("SimHei", 15)		# 定义用于显示帧速率的字体
		self.goto(scene_init.Scene_Init)					# 切换至加载界面 'init', 开始游戏

	def goto(self, scene):
		"""切换到 'scene'. 注意: 当且仅当游戏冷启动时可用该函数!"""
		self.scene = scene()
		self.scene.update()

	def call(self, scene):
		"""从当前界面切换到 'scene' """
		self.scene.stop()
		self.stack.append(self.scene)			# 新界面入栈
		self.scene = scene()					# 切换到新界面

	def back(self):
		"""切换回原界面"""
		self.scene = self.stack.pop()			# 原界面出栈
		self.scene.start()						# 切换回原界面

	def run(self):
		"""定义刷新函数"""
		while True:
			self.scene.update()					# 刷新屏幕
			self.scene.draw(self.screen)		# 绘制屏幕
			self.clock.tick_busy_loop(60)  		# 定义帧速率为60, 更新时钟
			# 实时在屏幕右下角使用白色字体绘制当前帧速率
			fps_img = self.myfont.render(
				str(int(self.clock.get_fps()*100)*1.0/100) + "fps", True, (255, 255, 255))
			fps_rect = fps_img.get_rect()
			fps_rect.bottomright = (640, 480)
			self.screen.blit(fps_img, fps_rect)

			pygame.display.flip()				# 刷新当前帧, 应用屏幕变动


if __name__ == '__main__':
	globe.mgame = Main_Window()
	globe.mgame.init()
	globe.mgame.run()
