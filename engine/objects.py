from abc import abstractmethod
import numpy as np
from pygame import Vector2, Vector3, Rect, image
from engine.assetsManager import Asset, AssetsManager
from engine.constants import Constants

class Components:
	class Component:
		INDEX:int=None
		RENDER:bool=False
		NAME:str=None
		@abstractmethod
		def __init__(self): pass
		@abstractmethod
		def init(self, object, assetsManager:AssetsManager): pass
		@abstractmethod
		def update(self, dt:float, object): pass
	class RComponent:
		RENDER:bool=True
		@abstractmethod
		def render(self, pygame): pass

	class Transform(Component):
		INDEX=0
		NAME="transform"
		def __init__(self, position:Vector2, rotation:Vector2, size:Vector2):
			self.position = position
			self.rotation = rotation
			self.size = size
			self.velocity = Vector2(0,0)
			self.force = Vector2(0,0)
		def update(self, dt:float, object):
			self.velocity += (self.force*dt)
			self.position += (self.velocity*dt)
	class Primitive(RComponent):
		INDEX=1
		NAME="primitive"
		def __init__(self, type:int, color:Vector3):
			LIST_OF_TYPES = (Constants.PRIMITIVE_RECTANGLE,Constants.PRIMITIVE_CIRCLE)
			assert type in LIST_OF_TYPES, "ERROR: " + str(type) + " is not a supported primitive type."
			self.type:int = type
			self.color:Vector3 = color
		def init(self, object, assetsManager: AssetsManager):
			self.position:tuple = tuple(object.transform.position)
			self.size:tuple = tuple(object.transform.size)
			self.rect:Rect = Rect(self.position,self.size)
		def update(self, dt:float, object):
			self.position:Vector2 = object.transform.position
			self.size:Vector2 = object.transform.size
			self.rect:Rect = Rect(self.position,self.size)
		def render(self, pygame):
			window = pygame.display.get_surface()
			if self.type == Constants.PRIMITIVE_RECTANGLE:
				pygame.draw.rect(window, tuple(self.color), tuple(self.rect))
			elif self.type == Constants.PRIMITIVE_CIRCLE:
				pygame.draw.circle(window, self.color,
					self.position + (self.size/2),
					(self.size/2).magnitude())
	class Image(RComponent):
		INDEX:int=2
		NAME:str="image"
		def __init__(self, image_asset_id:int):
			self.image_asset_id = image_asset_id
			self.img = None
			self.img_array = None
			self.shader = None
		def init(self, object, assetManager: AssetsManager):
			asset:Asset.ImageAsset = assetManager.getAsset(self.asset_id)
			self.img = asset.img
			self.img_array:np.ndarray = asset.img_array

		def update(self, dt:float, object):
			self.position = tuple(object.transform.position)
		def render(self, pygame):
			if not self.shader: output_array = self.img_array
			else: output_array = self.shader(self.img_array)
			surface = image.frombuffer(output_array.tobytes(), self.img.size, self.img.mode)
			pygame.display.get_surface().blit(surface, self.position)

class Object:
	def __init__(self, name:str, position:Vector2, rotation:Vector2=Vector2(0,0), size:Vector2=Vector2(1,1)):
		self.name:str = name
		self.added_components:list[str] = ["transform"]
		self.render_components:list[str] = []
		self.transform = Components.Transform(position, rotation, size)
		self.should_render:bool = False
	def update(self, dt:float):
		for component in self.added_components:
			self.__getattribute__(component).update(dt, self)
	def addComponent(self, component: Components.Component, assetManager:AssetsManager=None):
		self.added_components.append(component.NAME)
		self.__setattr__(component.NAME, component)
		if component.RENDER:
			self.render_components.append(component.NAME)
			self.should_render:bool = True
		self.__getattribute__(component.NAME).init(self, assetManager)
	def render(self, pygame):
		if not self.should_render: return
		for component_name in self.render_components:
			self.__getattribute__(component_name).render(pygame)