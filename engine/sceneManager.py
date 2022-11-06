from abc import abstractmethod
import pygame
from engine.maths import Vector3
from engine.objects import Object
from engine.particle import ParticleEmitter
from engine.colliders import Collider, CircleCollider

class Scene:
	def __init__(self, name:str, background_color=Vector3(255,255,255)):
		self.name:str = name
		self.background_color:tuple[int] = (background_color.x,background_color.y,background_color.z)
		self.objects:dict[str,Object] = {}
		self.particle_emitters:dict[str,ParticleEmitter] = {}
		self.storage = {}
		self.object_collision_callback:callable = lambda *a,**kw:None

	def update(self, window, dt:float):
		for obj in self.objects.values():
			obj.update(dt)
		self.on_update(self, dt, window)

		self.check_particle_collisions(window)

	def check_particle_collisions(self, window):
		if self.particle_emitters.values():
			colliders = [obj.collider.copy() for obj in self.objects.values()]
			for emitter in self.particle_emitters.values():
				emitter.check_collisions(window, colliders)
	
	def check_object_collisions(self, window):
		for objA in self.objects.values():
			for objB in self.objects.values():
				if objA == objB: continue
				if type(objA.collider) == CircleCollider and type(objB.collider) == CircleCollider:
					if (objA.transform.position+(objA.transform.size/2)-objB.transform.position-(objB.transform.size/2)).magnitude_squared() \
						< (objA.collider.radius + objB.collider.radius)**2:
						self.object_collision_callback(window, objA, objB)
				

	@staticmethod
	def on_update(self, dt:float): pass
	@staticmethod
	def on_render(self, pygame, screen, dt): pass

	def updateObject(self, object:Object):
		self.objects[object.name] = object

	def addObject(self, object:Object):
		self.objects.update({object.name:object})

	def render(self, pygame, dt):
		pygame.display.get_surface().fill(self.background_color)
		for obj in self.objects.values():
			obj.render(pygame)
		for particleEmitter in self.particle_emitters.values():
			particleEmitter.update(pygame.display.get_surface(), dt)
		self.on_render(self, pygame, pygame.display.get_surface(), dt)

	def add_particle_emitter(self, name, particleEmitter:ParticleEmitter):
		self.particle_emitters.update({name:particleEmitter})

class SceneManager:
	def __init__(self, window):
		self.current_scene:Scene = None
		self.current_scene_name:str = "default"
		self.scenes:dict[str,Scene] = {'default':Scene("default")}
		self.resets:dict[str,callable] = {}

		self.loadScene("default")

	def addScene(self, scene:Scene, reset=lambda *a,**kw:None):
		if not scene.name in self.scenes.keys(): 
			self.scenes.update({scene.name: scene})
		else: self.scenes[scene.name] = scene

		if reset: self.resets.update({scene.name:reset})

	def loadScene(self, name:str) -> Scene:
		self.current_scene_name:str = name
		self.current_scene:Scene = self.scenes[name]
		return self.current_scene
	
	def __get_item__(self, query:str) -> Scene:
		return self.scenes[query]

	def update(self, window, dt:float):
		self.current_scene.update(window, dt)
		self.current_scene.check_object_collisions(window)

	def reset_scene(self, name):
		scene = self.resets[name].__call__()
		self.scenes[name] = scene


