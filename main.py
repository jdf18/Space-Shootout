import engine
import game
from engine.assetsManager import AssetsManager, Asset
from pygame import Vector2, Vector3
from engine.constants import Constants
from engine.objects import Components, Object
from engine.sceneManager import Scene
from engine.util import createPrintCallback
from engine.input import Input
from pygame import BUTTON_LEFT, BUTTON_RIGHT, image, transform
from json import dumps, loads
from random import shuffle

global player, planets

assetsManager = AssetsManager()

window = engine.Window()

handler = engine.EventHandler()
def inc_vel(pos, button, touch):
	dx = (10 if button == BUTTON_LEFT else -10)
	window.sceneManager.current_scene.objects["TestRect"].transform.force += Vector2(dx,0)
handler.onClose = window.__del__
handler.onMouseButtonDown = inc_vel
window.start()

window.handle_events(handler)
window.update()
while window.running:
	window.render()
	dt = window.update()
	window.update_screen()
	window.handle_events(handler)

del window