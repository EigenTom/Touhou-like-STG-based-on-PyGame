# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys

import globe

from Scene import scene_title


class Scene_GameOver(object):

	def __init__(self):
		globe.mgame.msmanager.pause
		self.myfont = pygame.font.SysFont(None, 60)
		if globe.scgame.player.life < 0:
			self.image = self.myfont.render("GameOver!!", True, (255, 0, 0))
		else:
			self.image = self.myfont.render("You Win!!", True, (255, 0, 0))
		globe.mgame.screen.fill((128, 128, 0), globe.game_active_rect, BLEND_RGB_ADD)

	def start(self):
		pass

	def stop(self):
		pass

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
					pygame.quit()
					sys.exit()
				elif event.key == pygame.K_ESCAPE:
					globe.mgame.msmanager.play_SE("cancel")
					globe.mgame.msmanager.pause()
					globe.mgame.goto(scene_title.SceneTitle)
				elif event.key == pygame.K_r:
					globe.mgame.msmanager.play_SE("cancel")
					globe.scgame.__init__()
					globe.scgame.update()
					globe.mgame.back()

	def draw(self, screen):
		screen.blit(self.image, (250, 240))
