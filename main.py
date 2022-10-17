import engine

window = engine.Window()
window.create((1080,720), "Space Shootout")
#window.attachSceneManager()

handler = engine.EventHandler()
handler.onClose = window.__del__
while window.running:
	window.update()
	window.handle_events(handler)