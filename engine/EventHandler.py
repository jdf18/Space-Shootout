from abc import abstractmethod
from pygame.constants import *

class EventHandler:
	def __init__(self):
		pass
	def handle_event(self, event):
		# Pygame 1:
		if event.type == QUIT:
			self.onClose()
		elif event.type == ACTIVEEVENT: #! legacy
			self.onActiveEvent(event.gain, event.state)
		elif event.type == KEYDOWN:
			self.onKeyDown(event.key, event.mod, event.unicode, event.scancode)
		elif event.type == KEYUP:
			self.onKeyUp(event.key, event.mod, event.unicode, event.scancode)
		elif event.type == MOUSEMOTION:
			self.onMouseMotion(event.pos, event.rel, event.buttons, event.touch)
		elif event.type == MOUSEBUTTONUP:
			self.onMouseButtonUp(event.pos, event.button, event.touch)
		elif event.type == MOUSEBUTTONDOWN:
			self.onMouseButtonDown(event.pos, event.button, event.touch)
		elif event.type == JOYAXISMOTION:
			self.onJoyAxisMotion(event.instance_id, event.axis, event.value)
		elif event.type == JOYBALLMOTION:
			self.onJoyBallMotion(event.instance_id, event.ball, event.rel)
		elif event.type == JOYHATMOTION:
			self.onJoyHatMotion(event.instance_id, event.hat, event.value)
		elif event.type == JOYBUTTONUP:
			self.onJoyButtonUp(event.instance_id, event.button)
		elif event.type == JOYBUTTONDOWN:
			self.onJoyButtonDown(event.instance_id, event.button)
		elif event.type == VIDEORESIZE: #! Legacy - use window resized
			self.onVideoResize(event.size, event.w, event.h)
		elif event.type == VIDEOEXPOSE: #! legacy - use window exposed
			self.onVideoExpose()
		elif event.type == USEREVENT:
			self.onUserEvent(event.code)
		# When compiled with SDL2:
		elif event.type == AUDIODEVICEADDED:
			self.onAudioDeviceAdded(event.which, event.iscapture)
		elif event.type == AUDIODEVICEREMOVED:
			self.onAudioDeviceRemoved(event.which, event.iscapture)
		elif event.type == FINGERMOTION:
			self.onFingerMotion(event.touch_id, event.finger_id, event.x, event.y, event.dx, event.dy)
		elif event.type == FINGERDOWN:
			self.onFingerDown(event.touch_id, event.finger_id, event.x, event.y, event.dx, event.dy)
		elif event.type == FINGERUP:
			self.onFingerUp(event.touch_id, event.finger_id, event.x, event.y, event.dx, event.dy)
		elif event.type == MOUSEWHEEL:
			self.onMouseWheel(event.which, event.flipped, event.x, event.y, event.touch, event.precise_x, event.precise_y)
		elif event.type == MULTIGESTURE:
			self.onMultigesture(event.touch_id, event.x, event.y, event.pinched, event.rotated, event.num_fingers)
		elif event.type == TEXTEDITING:
			self.onTextEditing(event.text, event.start, event.length)
		elif event.type == TEXTINPUT:
			self.onTextInput(event.text)
		# Added in Pygame 2:
		elif event.type == DROPFILE:
			self.onDropFile(event.file)
		elif event.type == DROPBEGIN:
			self.onDropBegin()          # SDL >= 2.0.5
		elif event.type == DROPCOMPLETE:
			self.onDropComplete()       # SDL >= 2.0.5
		elif event.type == DROPTEXT:
			self.onDropText(event.text) # SDL >= 2.0.5
		elif event.type == MIDIIN:
			self.onMidiIn()  # reserved for midi
		elif event.type == MIDIOUT:
			self.onMidiOut() # reserved for midi
		elif event.type == CONTROLLERDEVICEADDED:
			self.onControllerDeviceAdded(event.device_index)
		elif event.type == JOYDEVICEADDED:
			self.onJoyDeviceAdded(event.device_index)
		elif event.type == CONTROLLERDEVICEREMOVED:
			self.onControllerDeviceRemoved(event.instance_id)
		elif event.type == JOYDEVICEREMOVED:
			self.onJoyDeviceRemoved(event.instance_id)
		elif event.type == CONTROLLERDEVICEREMAPPED:
			self.onControllerDeviceRemapped(event.instance_id)
		# Window events (PG 2.0.1)
		elif event.type == WINDOWSHOWN:
			self.onWindowShown(event.window)
		elif event.type == WINDOWHIDDEN:
			self.onWindowHidden(event.window)	
		elif event.type == WINDOWEXPOSED:
			self.onWindowExposed(event.window)
		elif event.type == WINDOWMOVED:
			self.onWindowMoved(event.window, event.x, event.y)
		elif event.type == WINDOWRESIZED:
			self.onWindowResized(event.window, event.x, event.y)
		elif event.type == WINDOWSIZECHANGED:
			self.onWindowSizeChanged(event.window)
		elif event.type == WINDOWMINIMIZED:
			self.onWindowMinimized(event.window)
		elif event.type == WINDOWMAXIMIZED:
			self.onWindowMaximised(event.window)
		elif event.type == WINDOWRESTORED:
			self.onWindowRestored(event.window)
		elif event.type == WINDOWENTER:
			self.onWindowEnter(event.window)
		elif event.type == WINDOWLEAVE:
			self.onWindowLeave(event.window)
		elif event.type == WINDOWFOCUSGAINED:
			self.onWindowFocusGained(event.window)
		elif event.type == WINDOWFOCUSLOST:
			self.onWindowFocusLost(event.window)
		elif event.type == WINDOWCLOSE:
			self.onWindowClose(event.window)
		elif event.type == WINDOWTAKEFOCUS:
			self.onWindowTakeFocus(event.window) # SDL >= 2.0.5
		elif event.type == WINDOWHITTEST:
			self.onWindowHitTest(event.window)   # SDL >= 2.0.5
		elif event.type == WINDOWICCPROFCHANGED:
			self.onWindowIccProfileChanged(event.window)                 # SDL >= 2.0.18
		elif event.type == WINDOWDISPLAYCHANGED:
			self.onWindowDisplayChanged(event.window, event.display_index) # SDL >= 2.0.18
		# Added in Pygame 2.1.3:
		elif event.type == KEYMAPCHANGED:
			self.onKeyMapChanged()
		elif event.type == CLIPBOARDUPDATE:
			self.onClipboardUpdate()
		elif event.type == RENDER_TARGETS_RESET:
			self.onRenderTargetsReset()
		elif event.type == RENDER_DEVICE_RESET:
			self.onRenderDeviceReset()
		elif event.type == LOCALECHANGED:
			self.onLocaleChanged()
		# On Android (PG 2.1.3)
		elif event.type == APP_TERMINATING:
			self.onAppTerminating()
		elif event.type == APP_LOWMEMORY:
			self.onAppLowMemory()
		elif event.type == APP_WILLENTERBACKGROUND:
			self.onAppWillEnterBackground()
		elif event.type == APP_DIDENTERBACKGROUND:
			self.onAppEnteredBackground()
		elif event.type == APP_WILLENTERFOREGROUND:
			self.onAppWillEnterForeground()
		elif event.type == APP_DIDENTERFOREGROUND:
			self.onAppEnteredForeground()
		else:
			self.onUnknownEvent()


	# Pygame 1:
	@abstractmethod
	def onClose(self, ): pass
	@abstractmethod
	def onActiveEvent(self, gain, state): pass
	@abstractmethod
	def onKeyDown(self, key, mod, unicode, scancode): pass
	@abstractmethod
	def onKeyUp(self, key, mod, unicode, scancode): pass
	@abstractmethod
	def onMouseMotion(self, pos, rel, buttons, touch): pass
	@abstractmethod
	def onMouseButtonUp(self, pos, buttons, touch): pass
	@abstractmethod
	def onMouseButtonDown(self, pos, buttons, touch): pass
	@abstractmethod
	def onJoyAxisMotion(self, instance_id, axis, value): pass
	@abstractmethod
	def onJoyBallMotion(self, instance_id, ball, rel): pass
	@abstractmethod
	def onJoyHatMotion(self, instance_id, hat, value): pass
	@abstractmethod
	def onJoyButtonUp(self, instance_id, button): pass
	@abstractmethod
	def onJoyButtonDown(self, instance_id, button): pass
	@abstractmethod
	def onVideoResize(self, size, w, h): pass
	@abstractmethod
	def onVideoExpose(self, ): pass
	@abstractmethod
	def onUserEvent(self, code): pass
	# When compiled with SDL2:
	@abstractmethod
	def onAudioDeviceAdded(self, which, iscapture): pass
	@abstractmethod
	def onAudioDeviceRemoved(self, which, iscapture): pass
	@abstractmethod
	def onFingerMotion(self, touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onFingerDown(self, touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onFingerUp(self, touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onMouseWheel(self, which, flipped, x, y, touch, precise_x, precise_y): pass
	@abstractmethod
	def onMultigesture(self, touch_id, x, y, pinched, rotated, num_fingers): pass
	@abstractmethod
	def onTextEditing(self, text, start, length): pass
	@abstractmethod
	def onTextInput(self, text): pass
	# Added in Pygame 2:
	@abstractmethod
	def onDropFile(self, file): pass
	@abstractmethod
	def onDropBegin(self, ): pass
	@abstractmethod
	def onDropComplete(self, ): pass
	@abstractmethod
	def onDropText(self, text): pass
	def onMidiIn(self, ): pass
	def onMidiOut(self, ): pass
	@abstractmethod
	def onControllerDeviceAdded(self, device_index): pass
	@abstractmethod
	def onJoyDeviceAdded(self, device_index): pass
	@abstractmethod
	def onControllerDeviceRemoved(self, instance_id): pass
	@abstractmethod
	def onJoyDeviceRemoved(self, instance_id): pass
	@abstractmethod
	def onControllerDeviceRemapped(self, instance_id): pass
	# Window events (self, PG 2.0.1)
	@abstractmethod
	def onWindowShown(self, window): pass
	@abstractmethod
	def onWindowHidden(self, window): pass
	@abstractmethod
	def onWindowExposed(self, window): pass
	@abstractmethod
	def onWindowMoved(self, window, x, y): pass
	@abstractmethod
	def onWindowResized(self, window, x, y): pass
	@abstractmethod
	def onWindowSizeChanged(self, window): pass
	@abstractmethod
	def onWindowMinimized(self, window): pass
	@abstractmethod
	def onWindowMaximised(self, window): pass
	@abstractmethod
	def onWindowRestored(self, window): pass
	@abstractmethod
	def onWindowEnter(self, window): pass
	@abstractmethod
	def onWindowLeave(self, window): pass
	@abstractmethod
	def onWindowFocusGained(self, window): pass
	@abstractmethod
	def onWindowFocusLost(self, window): pass
	@abstractmethod
	def onWindowClose(self, window): pass
	@abstractmethod
	def onWindowTakeFocus(self, window): pass
	@abstractmethod
	def onWindowHitTest(self, window): pass
	@abstractmethod
	def onWindowIccProfileChanged(self, window): pass
	@abstractmethod
	def onWindowDisplayChanged(self, window, display_index): pass
	# Added in Pygame 2.1.3:
	@abstractmethod
	def onKeyMapChanged(self, ): pass
	@abstractmethod
	def onClipboardUpdate(self, ): pass
	@abstractmethod
	def onRenderTargetsReset(self, ): pass
	@abstractmethod
	def onRenderDeviceReset(self, ): pass
	@abstractmethod
	def onLocaleChanged(self, ): pass
	# On Android (self, PG 2.1.3)
	@abstractmethod
	def onAppTerminating(self, ): pass
	@abstractmethod
	def onAppLowMemory(self, ): pass
	@abstractmethod
	def onAppWillEnterBackground(self, ): pass
	@abstractmethod
	def onAppEnteredBackground(self, ): pass
	@abstractmethod
	def onAppWillEnterForeground(self, ): pass
	@abstractmethod
	def onAppEnteredForeground(self, ): pass
	@abstractmethod
	def onUnknownEvent(self, ): pass