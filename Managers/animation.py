# -*- coding: UTF-8 -*-
class Anime(object):
	"""维护动画类"""
	def __init__(self, anime, pos, fps=1):
		self.anime = anime
		self.frame = len(anime)
		self.fps = fps
		self.now_frame = 0
		self.now_pic = 0
		self.pos = pos


class AnimeManager(object):
	"""动画管理器"""
	def __init__(self):
		self.La = []		# 存储动画: LAnimation
		self.Lf = []		# 存储单帧: LFrame
		self.frame = 0		# 初始化帧为0

	def create_anime(self, anime, pos, fps=1):			# 位置pos为List，tuple，rect貌似都可以
		self.La.append(Anime(anime, pos, fps))			# 图片，位置，剩余帧数,+1是为了让第一帧播放

	def create_pic(self, pic, frame, pos):
		self.Lf.append([pic, frame, pos, 0])

	def update(self):
		for i in self.La:
			i.now_frame += 1
			if i.now_frame % i.fps == 0:
				i.now_pic += 1
				if i.now_pic >= i.frame:
					self.La.remove(i)
		for i in self.Lf:
			if i[3] >= i[1]:
				self.Lf.remove(i)
		self.frame += 1

	def draw(self, screen):
		for i in self.La:
			screen.blit(i.anime[i.now_pic], i.pos)

		for i in self.Lf:
			screen.blit(i.pic, i.pos)
