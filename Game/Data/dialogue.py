# -*- encoding: UTF-8 -*-
import pygame
from pygame.locals import *
from Scene import scene_menu
import globe


global globaltext

global globaltext

globaltext = [
	['练手的小作品, 就不作什么介绍了.'],
	['艺术设计不存在的, 编剧也是不存在的。', '别指望这个游戏的质量, 到处是bug, ', '玩得开心是不可能的...'],
	['所以也没有和神主一样的剧本,', '取而代之的是...'],
	"showright",
	['哈, 这个妖精可真笨哪!'],
	"showleft",
	['你说什么?我可是幻想乡最强,', ' 放马过来吧!'],
	"showright",
	['等等, 我可没说是哪个妖精啊?!'],
	"showleft",
	['我在雾之湖冻了这么多年青蛙,', ' 幻想乡哪个妖精最笨我还不清楚吗?!'],
	"showright",
	['emmm...那好，开打吧。'],
]


class TextPlayer(object):
	def __init__(self):
		self.texts = globaltext
		self.index = 0
		self.lpic = globe.mgame.rsmanager.image["cirno"]
		self.rpic = globe.mgame.rsmanager.image["reimu"]
		self.lpic_av = False
		self.rpic_av = False
		self.font = pygame.font.SysFont(None, 20)
		self.rc = pygame.Rect(
			globe.game_active_rect.left, globe.game_active_rect.bottom-100, globe.game_active_rect.width-128, 100)

	def command(self, cm=None):
		if cm == "next":
			self.index += 1
		else:
			cm = self.texts[self.index]
			if cm == "showleft":
				self.lpic_av = True
				self.rpic_av = False
				self.index += 1
			elif cm == "showright":
				self.rpic_av = True
				self.lpic_av = False
				self.index += 1

	def update(self):
		if self.index < len(self.texts):
			self.command()
		else:
			globe.scgame.time += 1
			globe.scgame.tstart()
			return
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					self.command("next")
				elif event.key == pygame.K_ESCAPE:
					globe.mgame.msmanager.play_SE("pause")
					globe.mgame.call(scene_menu.Scene_Menu)

	def draw(self, screen):
		if globe.scgame.timestop:
			if not self.lpic_av:
				screen.fill((200, 200, 200), self.rc, BLEND_RGB_ADD)
				if type(self.texts[self.index]) == str:
					txtimg = self.font.render(self.texts[self.index], True, (255, 0, 0))
					screen.blit(txtimg,self.rc.topleft)
				elif type(self.texts[self.index]) == list:
					for i in range(len(self.texts[self.index])):
						txtimg = self.font.render(self.texts[self.index][i], True, (255, 0, 0))
						screen.blit(txtimg, (self.rc.left, self.rc.top+i*40))
				if self.rpic_av:
					tprc = self.rpic.get_rect()
					tprc.bottomleft = self.rc.bottomright
					screen.blit(self.rpic, tprc)
				elif self.lpic_av:
					tprc = self.lpic.get_rect()
					tprc.bottomright = self.rc.bottomleft
					screen.blit(self.lpic, tprc)

			else:
				tp = self.rc.copy()
				tp.left += 128
				screen.fill((200, 200, 200), tp, BLEND_RGB_ADD)

				if type(self.texts[self.index]) == str:
					txtimg = self.font.render(self.texts[self.index], True, (255, 0, 0))
					screen.blit(txtimg,tp.topleft)
				elif type(self.texts[self.index]) == list:
					for i in range(len(self.texts[self.index])):
						txtimg = self.font.render(self.texts[self.index][i], True, (255, 0, 0))
						screen.blit(txtimg, (tp.left, tp.top+i*40))
				if self.rpic_av:
					tprc = self.rpic.get_rect()
					tprc.bottomleft = tp.bottomright
					screen.blit(self.rpic, tprc)
				elif self.lpic_av:
					tprc = self.lpic.get_rect()
					tprc.bottomright = tp.bottomleft
					screen.blit(self.lpic, tprc)
