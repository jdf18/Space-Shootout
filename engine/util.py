from time import time, sleep
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
	
def lerp(t:float, p1:Vector2,p2:Vector2) -> Vector2:
	return p1 + (t * (p2-p1))
	

import types, functools

def copy_func(f):
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g