import pygame
from engine.eventHandler import EventHandler
from engine.util import Time
from engine.sceneManager import SceneManager

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
		self.begin_time = Time.start_time

		self.sceneManager = SceneManager()

		pygame.init()
		assert pygame.get_init(), "Pygame has not been successfully initialized."

		pygame.display.set_mode(self.dimensions, self.flags)

	def update(self):
		self.end_time = Time.time()
		dt = self.end_time - self.begin_time
		# fps = 1/dt
		self.sceneManager.update(dt)
		self.begin_time = self.end_time
		pygame.display.flip()

	def handle_events(self, handler):
		for event in pygame.event.get():
			handler.handle_event(event)

	def render(self):
		self.sceneManager.current_scene.render(pygame)

	def __del__(self):
		pygame.quit()
		self.running = False









