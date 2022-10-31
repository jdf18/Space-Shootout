from pygame.math import Vector2
from pygame import Surface
from random import randint

class ParticleEmitter:
	def __init__(self, surfaces:tuple[Surface], single:bool=False):
		# position, velocity style, timer
		self.particles:list[list[int,int],list[int,int],int,float] = []
		self.surfaces:tuple[Surface] = tuple(surfaces)
		self.single:bool = single
	def update(self, screen:Surface):
		for particle in self.particles:
			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1]
			particle[3] -= 0.2
			screen.blit(self.surfaces[2],particle[0])
		for particle in self.particles:
			if particle[3] <= 0:
				self.particles.remove(particle)
	def emit(self, location:tuple, velocity:tuple):
		if self.single: style:int = 0
		else: style:int = randint(0,len(self.surfaces) - 1)
		location = Vector2(location) - Vector2(self.surfaces[style].get_rect().size)/2
		particle = [list(location),list(velocity),style,randint(10,12)]
		# TODO Centre
		self.particles.append(particle)
