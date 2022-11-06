from abc import abstractmethod
from engine.eventHandler import EventHandler
from typing import Callable
from engine.constants import Constants
from pygame.math import Vector2

class Input:
	def __init__(self, event_handler: EventHandler) -> None:
		event_handler.onKeyDown = self.key_down_callback
		event_handler.onKeyUp = self.key_up_callback
		event_handler.onMouseButtonDown = self.button_down_callback
		event_handler.onMouseButtonUp = self.button_up_callback
		event_handler.onMouseMotion = self.mouse_motion_callback

		self.PG_TO_KEYSTATES_LUT:dict[int,int] = {
			pgCode:Constants.KEY_LUT.index(name) for name, pgCode in Constants.KEY_CODE_LUT
		}

		self.current_scene:str = None

		self.current_keys:dict[str,list[Callable]] = {}
		self.scene_keys:dict[str,dict[str,list[Callable]]] = {}

		self.current_clickables:dict[str,list[Callable]] = {}
		self.scene_clickables:dict[str,dict[str,list[Callable]]] = {}

		self.keystates:list[bool] = [False]*len(Constants.KEY_LUT)

		self.mouse_pos:Vector2 = Vector2(0,0)

	def load_scene(self, scene_name:str):
		if scene_name != self.current_scene:
			self.current_scene = scene_name
			try:
				self.current_clickables = self.scene_clickables[scene_name]
				self.current_keys = self.scene_keys[scene_name]
			except KeyError:
				print("ERROR: "+scene_name+" has not been created for clickable/key callbacks")

	def update(self, window):
		pass

	def key_down_callback(self, window, key:int, mod, unicode, scancode):
		try:
			self.keystates[self.PG_TO_KEYSTATES_LUT[key]] = True
		except:
			pass # TODO
	def key_up_callback(self, window, key:int, mod, unicode, scancode):
		try:
			self.keystates[self.PG_TO_KEYSTATES_LUT[key]] = False
		except:
			pass # TODO
	def get_key(self, key_name:str) -> bool:
		return self.keystates[Constants.KEY_LUT.index(key_name)]

	def button_down_callback(self, window, position, button, touch):
		for name, callbacks in self.current_clickables.items():
			try:
				if window.sceneManager.current_scene.objects[name].clickable.test_pos(position):
					for i, callback in enumerate(callbacks):
						print("input.py - calling", name, i)
						callback(name, window, position, button, touch)
			except:
				pass
	def button_up_callback(self, window, position, button, touch):
		pass

	def mouse_motion_callback(self, window, pos, rel, buttons, touch):
		self.mouse_pos = Vector2(pos)

	def get_mouse_pos(self):
		return self.mouse_pos

	def add_clickable_object(self, sceneName:str, objectName:str):
		if not sceneName in self.scene_clickables.keys():
			self.scene_clickables.update({sceneName:{objectName:[]}})
		elif not objectName in self.scene_clickables[sceneName].keys():
			self.scene_clickables[sceneName].update({objectName:[]})
	def add_clickable_callback(self, sceneName:str, objectName:str, callback:Callable):
		self.add_clickable_object(sceneName, objectName)
		self.scene_clickables[sceneName][objectName].append(callback)
		if sceneName == self.current_scene: self.current_clickables[objectName].append(callback)
	def remove_clickable_callbacks(self, sceneName:str, objectName:str):
		self.add_clickable_object(sceneName, objectName)
		self.scene_clickables[sceneName][objectName] = []
		if sceneName == self.current_scene: self.current_clickables[objectName] = []
		