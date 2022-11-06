from abc import abstractmethod
import numpy as np
from pygame import Surface, Vector2, Vector3, Rect, image
from engine.assetsManager import Asset, AssetsManager
from engine.constants import Constants
from pygame.font import Font
from engine.colliders import Collider, CircleCollider

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
		@abstractmethod
		def __repr__(self) -> str: return ""
	class RComponent(Component):
		RENDER:bool=True
		@abstractmethod
		def render(self, pygame): pass

	class Transform(Component):
		INDEX=0
		NAME="transform"
		def __init__(self, position:Vector2, rotation:float, size:Vector2):
			self.position:Vector2 = position
			self.rotation:float = (rotation % 360)
			self.size:Vector2 = size
			self.velocity:Vector2 = Vector2(0,0)
			self.force:Vector2 = Vector2(0,0)
			self.rect:Rect = Rect(self.position,self.size)
			self.center:Vector2 = self.position + (self.size/2)
		def update(self, dt:float, object):
			self.velocity += (self.force*dt)
			self.position += (self.velocity*dt)
			self.rect:Rect = Rect(self.position,self.size)
			
			self.rotation %= 360
		def __repr__(self) -> str:
			return f"Position: {self.position.__repr__()}\nRotation: {self.rotation.__repr__()}\nSize: {self.size.__repr__()}"

	class Primitive(RComponent):
		INDEX=1
		NAME="primitive"
		def __init__(self, type:int, color:Vector3):
			LIST_OF_TYPES = (Constants.PRIMITIVE_RECTANGLE,Constants.PRIMITIVE_CIRCLE)
			assert type in LIST_OF_TYPES, "ERROR: " + str(type) + " is not a supported primitive type."
			self.type:int = type
			self.color:Vector3 = color
			self.should_render = True
		def init(self, object, assetsManager: AssetsManager):
			self.position:tuple = tuple(object.transform.position)
			self.size:tuple = tuple(object.transform.size)
			self.rect:Rect = Rect(self.position,self.size)
		def update(self, dt:float, object):
			self.position:Vector2 = object.transform.position
			self.size:Vector2 = object.transform.size
			self.rect:Rect = Rect(self.position,self.size)
		def render(self, pygame):
			if not self.should_render: return
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
			self.position = Vector2(0,0)
			self.rotation = 0
			self.should_render = True
		def init(self, object, assetManager: AssetsManager):
			asset:Asset.ImageAsset = assetManager.getAsset(self.image_asset_id)
			self.img = asset.img
			self.img_array:np.ndarray = asset.img_array
			self.dimensions = object.transform.size
		def update(self, dt:float, object):
			self.position = tuple(object.transform.position)
			self.rotation = object.transform.rotation
		def render(self, pygame):
			if not self.should_render: return
			if not self.shader: output_array = self.img_array
			else: output_array = self.shader(self.img_array)
			surface = image.frombuffer(output_array.tobytes(), self.img.size, self.img.mode)
			scale_surf:Surface = pygame.transform.scale(surface,self.dimensions)
			if self.rotation != 0:
				offset:Vector2 = self.dimensions/2
				scale_surf = pygame.transform.rotate(scale_surf,self.rotation)
				offset -= Vector2(scale_surf.get_size())/2
			else:
				offset = Vector2(0,0)
			pygame.display.get_surface().blit(scale_surf, self.position+offset)

	class Text(RComponent):
		INDEX:int=3
		NAME:str="text"
		def __init__(self, text:str, color:Vector3, font_asset_id:int):
			self.font_asset_id:int = font_asset_id
			self.text:str = text
			self.last_text:str = None
			self.color:Vector3 = color
			self.dimensions:Vector2 = None
			self.should_render = True
			self.surface = None
			self.rotation:int = 0
			self.position = Vector2(0,0)
		def init(self, object, assetManager: AssetsManager):
			asset:Asset.FontAsset = assetManager.getAsset(self.font_asset_id)
			self.font:Font = asset.font
			self.dimensions:Vector2 = object.transform.size
		def update(self, dt:float, object):
			if self.last_text != self.text or self.last_text == None:
				self.surface:Surface = self.font.render(self.text, True, self.color)
				self.dimensions:Vector2 = Vector2(*self.surface.get_size())
				self.last_text:str = self.text
			self.position = Vector2(object.transform.position)
			self.rotation:float = object.transform.rotation
		def render(self, pygame):
			if not self.should_render: return
			if not self.surface: 
				self.surface:Surface = self.font.render(self.text, True, self.color)
				self.dimensions:Vector2 = Vector2(*self.surface.get_size())
			scale_surf:Surface = self.surface
			if self.rotation != 0:
				offset:Vector2 = self.dimensions/2
				scale_surf = pygame.transform.rotate(scale_surf,self.rotation)
				offset -= Vector2(scale_surf.get_size())/2
			else:
				offset = Vector2(0,0)
			pygame.display.get_surface().blit(scale_surf, self.position+offset-self.dimensions/2)
		def __repr__(self):
			return f"Text: {self.text}, {self.color}"


	class Clickable(Component):
		INDEX:int=4
		NAME:str="clickable"
		def __init__(self, is_static:bool, collider:Collider):
			self.static:bool = is_static
			self.collider = collider
		def update(self, dt:float, object):
			self.collider.update(object)
		def test_pos(self, position:Vector2) -> bool:
			return self.collider.test(position)


class Object:
	transform:Components.Transform
	primitive:Components.Primitive
	image:Components.Image
	text:Components.Text
	clickable:Components.Clickable
	collider:Collider
	def __init__(self, name:str, position:Vector2, rotation:float=0, size:Vector2=Vector2(1,1), tags:list[str]=["none"]):
		self.name:str = name
		self.added_components:list[str] = ["transform"]
		self.render_components:list[str] = []
		self.transform = Components.Transform(position, rotation, size)
		self.should_render:bool = False
		self.collider:Collider = Collider()
		self.tags:list[str] = tags
	def update(self, dt:float):
		self.collider.update(self)
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
	def __repr__(self):
		out = f"\nObject: {self.name}\nShould render: {str(self.should_render)}\nComponents: {self.added_components}\n"
		for component in self.added_components:
			out += self.__getattribute__(component).__repr__()
		return out