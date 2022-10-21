import pygame
from engine.maths import Vector3
from engine.objects import Object

class Scene:
	def __init__(self, name:str, background_color=Vector3(255,255,255)):
		self.name:str = name
		self.background_color:tuple[int] = (background_color.x,background_color.y,background_color.z)
		self.objects:dict[str,Object] = {}
	def update(self, dt:float):
		for obj in self.objects.values():
			obj.update(dt)
	def addObject(self, object:Object):
		self.objects.update({object.name:object})
	def render(self, pygame):
		pygame.display.get_surface().fill(self.background_color)
		for obj in self.objects.values():
			obj.render(pygame)

class SceneManager:
	def __init__(self):
		self.current_scene:Scene = None
		self.scenes:dict[str,Scene] = {'default':Scene("default")}
		self.loadScene("default")
	def addScene(self, scene:Scene):
		if not scene.name in self.scenes.keys():
			self.scenes.update({scene.name: scene})
		else:
			self.scenes[scene.name] = scene
	def loadScene(self, name:str) -> Scene:
		self.current_scene:Scene = self.scenes[name]
		return self.current_scene
	def __get_item__(self, query:str) -> Scene:
		return self.scenes[query]
	def update(self, dt:float):
		self.current_scene.update(dt)

