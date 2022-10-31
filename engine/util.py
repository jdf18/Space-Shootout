from time import time
from typing import Callable
from pygame.math import Vector2

class Time:
	start_time = time()
	@staticmethod
	def time() -> float:
		return time()

def createPrintCallback(message) -> Callable:
	def callback(*args, **kwargs):
		print(message)
	return callback

def get_lerp(p1:Vector2,p2:Vector2) -> Callable:
	def foo(val:float) -> Vector2:
		return p1 + (val * (p2-p1))
	return foo