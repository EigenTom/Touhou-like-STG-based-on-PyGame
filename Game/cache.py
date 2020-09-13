# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *

global image
global hue


def cache_init():
	global image
	global hue
	image = {}
	hue = {}


def cache_rotate(img, theta, flag=False):
	global image
	if not (img in image):
		cache_buffer(img)
	if (theta in image[img][0]):
		return image[img][0][theta]
	else:
		if flag:
			image[img][0][theta] = pygame.transform.rotate(img, theta)
			return image[img][0][theta]
		else:
			return pygame.transform.rotate(img, theta)


def cache_inter_change_alpha(img, alpha):
	tmp = pygame.Surface(img.get_size()).convert_alpha()
	tmp.lock()
	for i in range(tmp.get_width()):
		for j in range(tmp.get_height()):
			cl = img.get_at((i, j))
			if cl.a != 0:
				cl.a = int(alpha)
			tmp.set_at((i, j), cl)
	tmp.unlock()
	return tmp


def cache_set_alpha(img, alpha, flag=False):
	global image
	if not (img in image):
		cache_buffer(img)
	if (alpha in image[img][1]):
		return image[img][1][alpha]
	else:
		if flag:
			image[img][1][alpha] = cache_inter_change_alpha(img, alpha)
			image[img][1][alpha].fill((100, 0, 100, 40), None, BLEND_RGB_ADD)
			return image[img][1][alpha]
		else:
			return cache_inter_change_alpha(img, alpha)


def cache_flip(img, flag=False):
	global image
	if not (img in image):
		cache_buffer(img)
	if image[img][2] != None:
		return image[img][2]
	else:
		if not flag:
			tmp = pygame.transform.flip(img, True, False)
			return tmp
		else:
			image[img][2] = pygame.transform.flip(img, True, False)
			return image[img][2]


def cache_create_mask(img, color):
	img.fill(color, None, BLEND_RGB_ADD)


def cache_buffer(img):
	global image
	if (img in image):
		return
	else:
		image[img] = [{}, {}, None]  #第一个是rotate，第二个是transparent，第三个水平翻转


def cache_set_mask(img, color, flag=False):
	if not (img in hue.keys()):
		hue[img] = {}
	if not (color in hue[img]):
		if flag:
			hue[img][color] = img.copy()
			hue[img][color].fill(color, None, BLEND_RGB_ADD)
			return hue[img][color]
		else:
			tmp = img.copy()
			tmp.fill(color, None, BLEND_RGB_ADD)
			return tmp
	else:
		return hue[img][color]