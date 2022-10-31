from math import cos, floor, log10, sin, radians
from random import randint
from turtle import distance
from cv2 import magnitude

from pygame import Vector2
from engine.assetsManager import AssetsManager
from engine.objects import Object, Components
from engine import Window
from engine.sceneManager import Scene

class Planet:
	def __init__(self, name:str, planetData:dict) -> None:
		self.name:str = name
		self.order:int = planetData["order"]
		self.distance:int = planetData["distance"]
		self.mass:int = planetData["mass"]

		self.position = None
		self.diameter = None
	def bind_image(self, image_asset_id: int):
		self.image_asset_id:int = image_asset_id

	def calculate_position(self, screensize: tuple[int,int], orbitno:int) -> int:
		if self.position == None:
			centre = Vector2(screensize[0]/2,screensize[1]/2)
			if self.distance == 0: self.position = centre - self.size/2
			else:
				MAXDISTANCE = 270000000
				OFFSET = 150
				PLANET_COUNT = 5-1
				theta = 360/PLANET_COUNT * orbitno
				rand_angle = randint(floor(-360/PLANET_COUNT/3),floor(360/PLANET_COUNT/3))
				distance = OFFSET + floor(self.distance/MAXDISTANCE*((min(screensize)-OFFSET)/2-100))
				self.position = centre + Vector2(cos(radians(theta+rand_angle)),sin(radians(theta+rand_angle)))*distance
		self.position -= self.size/2
		return self.position
	def calculate_diameter(self):
		if self.name == "sun": 
			self.diameter = 75
		else:
			MAXMASS = (6.2E24)
			MAXDIAMETER = 25
			DIAMETEROFFSET = 20
			self.diameter = DIAMETEROFFSET + floor((self.mass)/MAXMASS*MAXDIAMETER)
		self.size = Vector2(self.diameter,self.diameter)
		return self.diameter
	def createGameObject(self, window_dimensions: tuple, assetsManager:AssetsManager, orbitno:int) -> Object:
		self.calculate_diameter()
		self.calculate_position(window_dimensions, orbitno)
		self.obj = Object(self.name,self.position, size=self.size)
		self.obj.addComponent(Components.Image(self.image_asset_id), assetsManager)
		return self.obj
