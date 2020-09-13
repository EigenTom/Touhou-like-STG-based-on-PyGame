# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import sys

import globe


class Scene_Menu(object):

	def __init__(self):
		self.myfont = pygame.font.SysFont(None,60)
		self.image = self.myfont.render("Pause", True, (255, 0, 0))

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
					globe.mgame.back()
				elif event.key == pygame.K_r:
					globe.mgame.msmanager.play_SE("cancel")
					globe.scgame.__init__()
					globe.scgame.update()
					globe.mgame.back()

	def draw(self, screen):
		screen.blit(self.image, (250, 240))