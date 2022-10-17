from abc import abstractmethod
from pygame.constants import *

class EventHandler:
	def __init__(self):
		pass
	def handle_events(self, event):
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
			self.onMouseButtonUp(event.pos, event.buttons, event.touch)
		elif event.type == MOUSEBUTTONDOWN:
			self.onMouseButtonDown(event.pos, event.buttons, event.touch)
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
	def onClose(): pass
	@abstractmethod
	def onActiveEvent(gain, state): pass
	@abstractmethod
	def onKeyDown(key, mod, unicode, scancode): pass
	@abstractmethod
	def onKeyUp(key, mod, unicode, scancode): pass
	@abstractmethod
	def onMouseMotion(pos, rel, buttons, touch): pass
	@abstractmethod
	def onMouseButtonUp(pos, buttons, touch): pass
	@abstractmethod
	def onMouseButtonDown(pos, buttons, touch): pass
	@abstractmethod
	def onJoyAxisMotion(instance_id, axis, value): pass
	@abstractmethod
	def onJoyBallMotion(instance_id, ball, rel): pass
	@abstractmethod
	def onJoyHatMotion(instance_id, hat, value): pass
	@abstractmethod
	def onJoyButtonUp(instance_id, button): pass
	@abstractmethod
	def onJoyButtonDown(instance_id, button): pass
	@abstractmethod
	def onVideoResize(size, w, h): pass
	@abstractmethod
	def onVideoExpose(): pass
	@abstractmethod
	def onUserEvent(code): pass
	# When compiled with SDL2:
	@abstractmethod
	def onAudioDeviceAdded(which, iscapture): pass
	@abstractmethod
	def onAudioDeviceRemoved(which, iscapture): pass
	@abstractmethod
	def onFingerMotion(touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onFingerDown(touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onFingerUp(touch_id, finger_id, x, y, dx, dy): pass
	@abstractmethod
	def onMouseWheel(which, flipped, x, y, touch, precise_x, precise_y): pass
	@abstractmethod
	def onMultigesture(touch_id, x, y, pinched, rotated, num_fingers): pass
	@abstractmethod
	def onTextEditing(text, start, length): pass
	@abstractmethod
	def onTextInput(text): pass
	# Added in Pygame 2:
	@abstractmethod
	def onDropFile(file): pass
	@abstractmethod
	def onDropBegin(): pass
	@abstractmethod
	def onDropComplete(): pass
	@abstractmethod
	def onDropText(text): pass
	def onMidiIn(): pass
	def onMidiOut(): pass
	@abstractmethod
	def onControllerDeviceAdded(device_index): pass
	@abstractmethod
	def onJoyDeviceAdded(device_index): pass
	@abstractmethod
	def onControllerDeviceRemoved(instance_id): pass
	@abstractmethod
	def onJoyDeviceRemoved(instance_id): pass
	@abstractmethod
	def onControllerDeviceRemapped(instance_id): pass
	# Window events (PG 2.0.1)
	@abstractmethod
	def onWindowShown(window): pass
	@abstractmethod
	def onWindowHidden(window): pass
	@abstractmethod
	def onWindowExposed(window): pass
	@abstractmethod
	def onWindowMoved(window, x, y): pass
	@abstractmethod
	def onWindowResized(window, x, y): pass
	@abstractmethod
	def onWindowSizeChanged(window): pass
	@abstractmethod
	def onWindowMinimized(window): pass
	@abstractmethod
	def onWindowMaximised(window): pass
	@abstractmethod
	def onWindowRestored(window): pass
	@abstractmethod
	def onWindowEnter(window): pass
	@abstractmethod
	def onWindowLeave(window): pass
	@abstractmethod
	def onWindowFocusGained(window): pass
	@abstractmethod
	def onWindowFocusLost(window): pass
	@abstractmethod
	def onWindowClose(window): pass
	@abstractmethod
	def onWindowTakeFocus(window): pass
	@abstractmethod
	def onWindowHitTest(window): pass
	@abstractmethod
	def onWindowIccProfileChanged(window): pass
	@abstractmethod
	def onWindowDisplayChanged(window, display_index): pass
	# Added in Pygame 2.1.3:
	@abstractmethod
	def onKeyMapChanged(): pass
	@abstractmethod
	def onClipboardUpdate(): pass
	@abstractmethod
	def onRenderTargetsReset(): pass
	@abstractmethod
	def onRenderDeviceReset(): pass
	@abstractmethod
	def onLocaleChanged(): pass
	# On Android (PG 2.1.3)
	@abstractmethod
	def onAppTerminating(): pass
	@abstractmethod
	def onAppLowMemory(): pass
	@abstractmethod
	def onAppWillEnterBackground(): pass
	@abstractmethod
	def onAppEnteredBackground(): pass
	@abstractmethod
	def onAppWillEnterForeground(): pass
	@abstractmethod
	def onAppEnteredForeground(): pass
	@abstractmethod
	def onUnknownEvent(): pass