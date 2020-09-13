# -*- coding: UTF-8 -*-
import pygame
import globe

global se


class MusicManager(object):

	def __init__(self):
		global se
		se = globe.mgame.rsmanager.se

	def play_BGM(self,filename,volume=0.2):
		pygame.mixer.music.load(filename)
		pygame.mixer.music.set_volume(volume)
		pygame.mixer.music.play()

	def pause(self):
		pygame.mixer.music.pause()

	def unpause(self):
		pygame.mixer.music.unpause()

	def stop(self):
		pygame.mixer.music.stop()

	def play_SE(self, file, volume=0.1):
		global se
		se[file].set_volume(volume)
		se[file].play()
