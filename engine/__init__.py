import pygame
from engine.eventHandler import EventHandler
from engine.input import Input
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
		self.dimensions:tuple = dimensions
		self.width, self.height = dimensions
		self.title = title

		self.flags = pygame.SHOWN #| pygame.RESIZABLE

		self.sceneManager = SceneManager()

		self.input_manager:Input = None

	def start(self):
		self.begin_time = Time.start_time

		pygame.init()
		assert pygame.get_init(), "Pygame has not been successfully initialized."
		self.screen = pygame.display.set_mode(self.dimensions, self.flags)

	def bind_input_manager(self, input_manager:Input):
		self.input_manager = input_manager

	def update(self) -> float:
		self.end_time = Time.time()
		dt = self.end_time - self.begin_time
		# fps = 1/dt
		self.sceneManager.update(dt)
		self.begin_time = self.end_time
		return dt
	def update_screen(self):
		pygame.display.flip()

	def handle_events(self, handler):
		for event in pygame.event.get():
			handler.handle_event(event, self)

	def render(self):
		self.sceneManager.current_scene.render(pygame)
	
	def draw_line(self, p1,p2):
		pygame.draw.line(self.screen,(0,255,0),p1,p2,1)

	def __del__(self, *args):
		pygame.quit()
		self.running = False









