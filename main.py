import engine
from engine.util import createPrintCallback

window = engine.Window()
window.create((1080,720), "Space Shootout")
#window.attachSceneManager()

handler = engine.EventHandler()
handler.onClose = window.__del__
handler.onMouseButtonDown = createPrintCallback("MBD")
while window.running:
	window.update()
	window.handle_events(handler)