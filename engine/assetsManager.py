from abc import abstractmethod
from PIL import Image
import numpy as np
from pygame import Vector2, Vector3, image
from pygame import font
from json import dumps, loads

from engine.constants import Constants

class Asset:
	class Asset:
		_type:int = Constants.ASSET_TYPE_NONE
		def __init__(self, filename:str, *args, **kwargs):
			self.filename:str = filename
			self.init(*args, **kwargs)
		@abstractmethod
		def init(self): pass
	@classmethod
	def create(cls, filename: str):
		extension:str = filename[filename.rindex('.'):]
		if extension == '.png':
			cls.ImageAsset(filename)
	class ImageAsset(Asset):
		_type:int = Constants.ASSET_TYPE_IMAGE
		def init(self):
			self.img = Image.open(self.filename).convert("RGBA")
			self.img_array:np.ndarray = np.array(self.img)
	class ShaderAsset(Asset):
		_type:int = Constants.ASSET_TYPE_SHADER
		def init(self):
			self.code = compile(self.generate_source(), '', 'eval')
			def foo(input_array):
				exec(self.code, {"np":np,"Vector2":Vector2,"Vector3":Vector3}, {})
				return eval("output")
			self.func = foo
		@abstractmethod
		def func(input_array: np.ndarray) -> np.ndarray: return
		def generate_source(self) -> str:
			with open(self.filename, 'rb') as file:
				contents = file.read()
				# TODO 
				return contents
	class TextAsset(Asset):
		def init(self, size:int):
			self.size = size
			font.init()
			self.font = font.Font(self.filename, size)
	class JSONAsset(Asset):
		def init(self):
			with open(self.filename) as file:
				self.contents = loads(file.read())
		def __call__(self):
			return self.contents


class AssetsManager:
	def __init__(self):
		self.next_id:int = 0
		self.assets:list[Asset.Asset] = []
	def addAsset(self, asset:Asset.Asset) -> int:
		self.assets.append(asset)
		self.next_id += 1
		return self.next_id - 1
	__call__ = addAsset
	def getAsset(self, asset_id:int) -> Asset.Asset:
		return self.assets[asset_id]