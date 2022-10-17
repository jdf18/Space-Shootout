from abc import abstractmethod
import pygame
from engine.util import Time

class Window:
	__instance = None
	def __init__(self):
		assert Window.__instance == None, "Window instance has already been creted."
		Window.__instance = self
	@classmethod
	def get_instance(cls):
		return cls.__instance
	
	def create(self, dimensions, title):
		self.running = True
		self.dimensions = dimensions
		self.width, self.height = dimensions
		self.title = title

		self.flags = pygame.RESIZABLE | pygame.SHOWN

		pygame.init()
		assert pygame.get_init(), "Pygame has not been successfully initialized."

		pygame.display.set_mode(self.dimensions, self.flags)

	def update(self):
		pygame.display.flip()

	def __del__(self):
		pygame.quit()
		self.running = False


class EventHandler:
	def __init__(self):
		pass
	def poll_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.onClose()
	@abstractmethod
	def onClose(self):
		pass
