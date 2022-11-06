from abc import abstractmethod
from pygame.constants import *
from pygame.event import Event

from engine import Window

class EventHandler:
	def __init__(self):
		pass
	def handle_event(self, event: Event, window:Window):
		# Pygame 1:
		if event.type == QUIT:
			self.onClose(window, )
		elif event.type == ACTIVEEVENT: #! legacy
			self.onActiveEvent(window, event.gain, event.state)
		elif event.type == KEYDOWN:
			self.onKeyDown(window, event.key, event.mod, event.unicode, event.scancode)
		elif event.type == KEYUP:
			self.onKeyUp(window, event.key, event.mod, event.unicode, event.scancode)
		elif event.type == MOUSEMOTION:
			self.onMouseMotion(window, event.pos, event.rel, event.buttons, event.touch)
		elif event.type == MOUSEBUTTONUP:
			self.onMouseButtonUp(window, event.pos, event.button, event.touch)
		elif event.type == MOUSEBUTTONDOWN:
			self.onMouseButtonDown(window, event.pos, event.button, event.touch)
		elif event.type == JOYAXISMOTION:
			self.onJoyAxisMotion(window, event.instance_id, event.axis, event.value)
		elif event.type == JOYBALLMOTION:
			self.onJoyBallMotion(window, event.instance_id, event.ball, event.rel)
		elif event.type == JOYHATMOTION:
			self.onJoyHatMotion(window, event.instance_id, event.hat, event.value)
		elif event.type == JOYBUTTONUP:
			self.onJoyButtonUp(window, event.instance_id, event.button)
		elif event.type == JOYBUTTONDOWN:
			self.onJoyButtonDown(window, event.instance_id, event.button)
		elif event.type == VIDEORESIZE: #! Legacy - use window resized
			self.onVideoResize(window, event.size, event.w, event.h)
		elif event.type == VIDEOEXPOSE: #! legacy - use window exposed
			self.onVideoExpose(window, )
		elif event.type == USEREVENT:
			self.onUserEvent(window, event.code)
		# When compiled with SDL2:
		elif event.type == AUDIODEVICEADDED:
			self.onAudioDeviceAdded(window, event.which, event.iscapture)
		elif event.type == AUDIODEVICEREMOVED:
			self.onAudioDeviceRemoved(window, event.which, event.iscapture)
		elif event.type == FINGERMOTION:
			self.onFingerMotion(window, event.touch_id, event.finger_id, event.x, event.y, event.dx, event.dy)
		elif event.type == FINGERDOWN:
			self.onFingerDown(window, event.touch_id, event.finger_id, event.x, event.y, event.dx, event.dy)
		elif event.type == FINGERUP:
			self.onFingerUp(window, event.touch_id, event.finger_id, event.x, event.y, event.dx, event.dy)
		elif event.type == MOUSEWHEEL:  # TODO which throws error
			self.onMouseWheel(window, event.which, event.flipped, event.x, event.y, event.touch, event.precise_x, event.precise_y)
		elif event.type == MULTIGESTURE:
			self.onMultigesture(window, event.touch_id, event.x, event.y, event.pinched, event.rotated, event.num_fingers)
		elif event.type == TEXTEDITING:
			self.onTextEditing(window, event.text, event.start, event.length)
		elif event.type == TEXTINPUT:
			self.onTextInput(window, event.text)
		# Added in Pygame 2:
		elif event.type == DROPFILE:
			self.onDropFile(window, event.file)
		elif event.type == DROPBEGIN:
			self.onDropBegin(window, )          # SDL >= 2.0.5
		elif event.type == DROPCOMPLETE:
			self.onDropComplete(window, )       # SDL >= 2.0.5
		elif event.type == DROPTEXT:
			self.onDropText(window, event.text) # SDL >= 2.0.5
		elif event.type == MIDIIN:
			self.onMidiIn(window, )  # reserved for midi
		elif event.type == MIDIOUT:
			self.onMidiOut(window, ) # reserved for midi
		elif event.type == CONTROLLERDEVICEADDED:
			self.onControllerDeviceAdded(window, event.device_index)
		elif event.type == JOYDEVICEADDED:
			self.onJoyDeviceAdded(window, event.device_index)
		elif event.type == CONTROLLERDEVICEREMOVED:
			self.onControllerDeviceRemoved(window, event.instance_id)
		elif event.type == JOYDEVICEREMOVED:
			self.onJoyDeviceRemoved(window, event.instance_id)
		elif event.type == CONTROLLERDEVICEREMAPPED:
			self.onControllerDeviceRemapped(window, event.instance_id)
		# Window events (window, PG 2.0.1)
		elif event.type == WINDOWSHOWN:
			self.onWindowShown(window, event.window)
		elif event.type == WINDOWHIDDEN:
			self.onWindowHidden(window, event.window)	
		elif event.type == WINDOWEXPOSED:
			self.onWindowExposed(window, event.window)
		elif event.type == WINDOWMOVED:
			self.onWindowMoved(window, event.window, event.x, event.y)
		elif event.type == WINDOWRESIZED:
			self.onWindowResized(window, event.window, event.x, event.y)
		elif event.type == WINDOWSIZECHANGED:
			self.onWindowSizeChanged(window, event.window)
		elif event.type == WINDOWMINIMIZED:
			self.onWindowMinimized(window, event.window)
		elif event.type == WINDOWMAXIMIZED:
			self.onWindowMaximised(window, event.window)
		elif event.type == WINDOWRESTORED:
			self.onWindowRestored(window, event.window)
		elif event.type == WINDOWENTER:
			self.onWindowEnter(window, event.window)
		elif event.type == WINDOWLEAVE:
			self.onWindowLeave(window, event.window)
		elif event.type == WINDOWFOCUSGAINED:
			self.onWindowFocusGained(window, event.window)
		elif event.type == WINDOWFOCUSLOST:
			self.onWindowFocusLost(window, event.window)
		elif event.type == WINDOWCLOSE:
			self.onWindowClose(window, event.window)
		elif event.type == WINDOWTAKEFOCUS:
			self.onWindowTakeFocus(window, event.window) # SDL >= 2.0.5
		elif event.type == WINDOWHITTEST:
			self.onWindowHitTest(window, event.window)   # SDL >= 2.0.5
		elif event.type == WINDOWICCPROFCHANGED:
			self.onWindowIccProfileChanged(window, event.window)                 # SDL >= 2.0.18
		elif event.type == WINDOWDISPLAYCHANGED:
			self.onWindowDisplayChanged(window, event.window, event.display_index) # SDL >= 2.0.18
		# Added in Pygame 2.1.3:
		elif event.type == KEYMAPCHANGED:
			self.onKeyMapChanged(window, )
		elif event.type == CLIPBOARDUPDATE:
			self.onClipboardUpdate(window, )
		elif event.type == RENDER_TARGETS_RESET:
			self.onRenderTargetsReset(window, )
		elif event.type == RENDER_DEVICE_RESET:
			self.onRenderDeviceReset(window, )
		elif event.type == LOCALECHANGED:
			self.onLocaleChanged(window, )
		# On Android (window, PG 2.1.3)
		elif event.type == APP_TERMINATING:
			self.onAppTerminating(window, )
		elif event.type == APP_LOWMEMORY:
			self.onAppLowMemory(window, )
		elif event.type == APP_WILLENTERBACKGROUND:
			self.onAppWillEnterBackground(window, )
		elif event.type == APP_DIDENTERBACKGROUND:
			self.onAppEnteredBackground(window, )
		elif event.type == APP_WILLENTERFOREGROUND:
			self.onAppWillEnterForeground(window, )
		elif event.type == APP_DIDENTERFOREGROUND:
			self.onAppEnteredForeground(window, )
		else:
			self.onUnknownEvent(window, )


	# Pygame 1:
	@abstractmethod
	def onClose(self, window): pass
	@abstractmethod
	def onActiveEvent(self, window, gain, state): pass
	@abstractmethod
	def onKeyDown(self, window, key, mod, unicode, scancode): pass
	@abstractmethod
	def onKeyUp(self, window, key, mod, unicode, scancode): pass
	@abstractmethod
	def onMouseMotion(self, window, pos, rel, buttons, touch): pass
	@abstractmethod
	def onMouseButtonUp(self, window, pos, buttons, touch): pass
	@abstractmethod
	def onMouseButtonDown(self, window, pos, buttons, touch): pass
	@abstractmethod
	def onJoyAxisMotion(self, window, instance_id, axis, value): pass
	@abstractmethod
	def onJoyBallMotion(self, window, instance_id, ball, rel): pass
	@abstractmethod
	def onJoyHatMotion(self, window, instance_id, hat, value): pass
	@abstractmethod
	def onJoyButtonUp(self, window, instance_id, button): pass
	@abstractmethod
	def onJoyButtonDown(self, window, instance_id, button): pass
	@abstractmethod
	def onVideoResize(self, window, size, w, h): pass
	@abstractmethod
	def onVideoExpose(self, window): pass
	@abstractmethod
	def onUserEvent(self, window, code): pass
	# When compiled with SDL2:
	@abstractmethod
	def onAudioDeviceAdded(self, window, which, iscapture): pass
	@abstractmethod
	def onAudioDeviceRemoved(self, window, which, iscapture): pass
	@abstractmethod
	def onFingerMotion(self, window, touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onFingerDown(self, window, touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onFingerUp(self, window, touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onMouseWheel(self, window, which, flipped, x, y, touch, precise_x, precise_y): pass
	@abstractmethod
	def onMultigesture(self, window, touch_id, x, y, pinched, rotated, num_fingers): pass
	@abstractmethod
	def onTextEditing(self, window, text, start, length): pass
	@abstractmethod
	def onTextInput(self, window, text): pass
	# Added in Pygame 2:
	@abstractmethod
	def onDropFile(self, window, file): pass
	@abstractmethod
	def onDropBegin(self, window): pass
	@abstractmethod
	def onDropComplete(self, window): pass
	@abstractmethod
	def onDropText(self, window, text): pass
	def onMidiIn(self, window): pass
	def onMidiOut(self, window): pass
	@abstractmethod
	def onControllerDeviceAdded(self, window, device_index): pass
	@abstractmethod
	def onJoyDeviceAdded(self, window, device_index): pass
	@abstractmethod
	def onControllerDeviceRemoved(self, window, instance_id): pass
	@abstractmethod
	def onJoyDeviceRemoved(self, window, instance_id): pass
	@abstractmethod
	def onControllerDeviceRemapped(self, window, instance_id): pass
	# Window events (window, PG 2.0.1)
	@abstractmethod
	def onWindowShown(self, window, screen): pass
	@abstractmethod
	def onWindowHidden(self, window, screen): pass
	@abstractmethod
	def onWindowExposed(self, window, screen): pass
	@abstractmethod
	def onWindowMoved(self, window, screen, x, y): pass
	@abstractmethod
	def onWindowResized(self, window, screen, x, y): pass
	@abstractmethod
	def onWindowSizeChanged(self, window, screen): pass
	@abstractmethod
	def onWindowMinimized(self, window, screen): pass
	@abstractmethod
	def onWindowMaximised(self, window, screen): pass
	@abstractmethod
	def onWindowRestored(self, window, screen): pass
	@abstractmethod
	def onWindowEnter(self, window, screen): pass
	@abstractmethod
	def onWindowLeave(self, window, screen): pass
	@abstractmethod
	def onWindowFocusGained(self, window, screen): pass
	@abstractmethod
	def onWindowFocusLost(self, window, screen): pass
	@abstractmethod
	def onWindowClose(self, window, screen): pass
	@abstractmethod
	def onWindowTakeFocus(self, window, screen): pass
	@abstractmethod
	def onWindowHitTest(self, window, screen): pass
	@abstractmethod
	def onWindowIccProfileChanged(self, window, screen): pass
	@abstractmethod
	def onWindowDisplayChanged(self, window, screen, display_index): pass
	# Added in Pygame 2.1.3:
	@abstractmethod
	def onKeyMapChanged(self, window): pass
	@abstractmethod
	def onClipboardUpdate(self, window): pass
	@abstractmethod
	def onRenderTargetsReset(self, window): pass
	@abstractmethod
	def onRenderDeviceReset(self, window): pass
	@abstractmethod
	def onLocaleChanged(self, window): pass
	# On Android (window, PG 2.1.3)
	@abstractmethod
	def onAppTerminating(self, window): pass
	@abstractmethod
	def onAppLowMemory(self, window): pass
	@abstractmethod
	def onAppWillEnterBackground(self, window): pass
	@abstractmethod
	def onAppEnteredBackground(self, window): pass
	@abstractmethod
	def onAppWillEnterForeground(self, window): pass
	@abstractmethod
	def onAppEnteredForeground(self, window): pass
	@abstractmethod
	def onUnknownEvent(self, window): pass