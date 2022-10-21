import engine
from pygame import Vector2, Vector3
from engine.constants import Constants
from engine.util import createPrintCallback
from pygame import BUTTON_LEFT, BUTTON_RIGHT

window = engine.Window()
window.create((1080,720), "Space Shootout")

window.sceneManager.addScene(menuScene)
window.sceneManager.loadScene("MenuScene")

handler = engine.EventHandler()
handler.onClose = window.__del__
handler.onMouseButtonDown = createPrintCallback("MBD")
while window.running:
	window.render()
	window.update()
	window.handle_events(handler)

del window