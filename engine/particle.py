from pygame.math import Vector2
from pygame import Surface
from random import randint
from engine.colliders import Collider


class ParticleEmitter:
	def __init__(self, name:str, surfaces:tuple[Surface], single:bool=False, callback:callable=lambda *a,**kw : False):
		self.name = name

		# position, velocity style, timer
		self.particles:list[list[int,int],list[int,int],int,float] = []
		self.surfaces:tuple[Surface] = tuple(surfaces)
		self.single:bool = single

		self.screen_dim = None

		self.callback:callable = callback
	def update(self, screen:Surface, dt):
		if not self.screen_dim: self.screen_dim = (screen.get_width(), screen.get_width())

		for particle in self.particles:
			particle[0][0] += particle[1][0]*dt
			particle[0][1] += particle[1][1]*dt
			particle[3] -= 0.2
			if particle[0][0] < 0: particle[0][0] += self.screen_dim[0]
			if particle[0][0] >= self.screen_dim[0]: particle[0][0] -= self.screen_dim[0]
			if particle[0][1] < 0: particle[0][1] += self.screen_dim[1]
			if particle[0][1] >= self.screen_dim[1]: particle[0][1] -= self.screen_dim[1]
			screen.blit(self.surfaces[particle[2]],particle[0])
		for particle in self.particles:
			if particle[3] <= 0:
				self.particles.remove(particle)

	def check_collisions(self, window, colliders:list[Collider]):
		#print(colliders)
		remove:list[int] = []
		for i, particle in enumerate(self.particles):
			u_remove:bool = False
			for collider in colliders:
				if not collider: continue
				collided: bool = collider.test(Vector2(particle[0][0], particle[0][1]))
				if collided:
					t_remove:bool = bool(self.callback.__call__(window, self.name, collider.name, particle[3]))
					if t_remove: print("coll", self.name, collider.name)
					if not u_remove: u_remove:bool = t_remove
			if u_remove: remove.append(i)
		
		offset:int = 0
		for index in remove:
			self.particles.pop(index - offset)
			offset += 1

	def emit(self, location:tuple, velocity:tuple, timeout=(10,12)):
		if self.single: style:int = 0
		else: style:int = randint(0,len(self.surfaces) - 1)
		location = Vector2(location) - Vector2(self.surfaces[style].get_rect().size)/2
		particle = [list(location),list(velocity),style,randint(*timeout)]
		# TODO Centre
		self.particles.append(particle)
