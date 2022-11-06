from abc import abstractmethod
from pygame import Vector2

class Collider:
	def __init__(self):
		name:str = None
	@abstractmethod
	def test(self, position:Vector2) -> bool:
		return 0
	@abstractmethod
	def update(self,update):
		pass
	@abstractmethod
	def copy(self):
		return self

class CircleCollider (Collider):
	def __init__(self):
		self.center:Vector2 = Vector2(0,0)
		self.radius:float = 1
		self.name:str = None
	def update(self, object):
		self.center:Vector2 = object.transform.position + (object.transform.size/2)
		self.radius:float = max(object.transform.size.x, object.transform.size.y)/2
		if not self.name: self.name:str = object.name
	def test(self, position:Vector2) -> bool:
		# return true if does collide
		delta: Vector2 = (position - self.center)
		return bool(delta.magnitude_squared() <= (self.radius * self.radius))
	def __repr__(self):
		return f"{self.center}, {self.radius}\n"
	def copy(self):
		cc = CircleCollider()
		cc.center = self.center
		cc.radius = self.radius
		cc.name = self.name
		return cc