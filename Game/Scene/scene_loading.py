# -*- coding: UTF-8 -*-
import pygame
from Scene import scene_game
import globe


class Scene_Loading (object):
	"""定义淡出效果"""
	def __init__(self):
		self.rs = globe.mgame.rsmanager.image		# rs = resource
		self.time = -20
		self.fade_out = pygame.Surface(globe.mgame.screen.get_size())

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
					pygame.quit()
					sys.exit()
		if self.time >= 60:
			globe.mgame.goto(scene_game.Scene_Game)
		self.time += 1

	def draw(self, screen):
		screen.fill((255, 255, 255))
		screen.blit(self.rs["loading"], (0, 0))
		if self.time < 0:
			self.fade_out.set_alpha(-12 * (self.time))
			screen.blit(self.fade_out, (0, 0))


