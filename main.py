import engine
from engine.assetsManager import AssetsManager, Asset
from pygame import Vector2, Vector3
from engine.constants import Constants
from engine.objects import Components, Object
from engine.sceneManager import Scene
from engine.util import createPrintCallback
from pygame import BUTTON_LEFT, BUTTON_RIGHT

assetsManager = AssetsManager()
imageasset = assetsManager(Asset.ImageAsset('assets/images/test.png'))

menuScene = Scene("MenuScene", background_color=Vector3(255,255,255))
testrect = Object("TestRect",Vector2(10,10),size=Vector2(100,100))
testrect.addComponent(Components.Primitive(Constants.PRIMITIVE_RECTANGLE, Vector3(255,0,0)))
menuScene.addObject(testrect)
testcirc = Object("TestCirc",Vector2(10,10),size=Vector2(100,100))
testcirc.addComponent(Components.Primitive(Constants.PRIMITIVE_CIRCLE, Vector3(255,255,0)))
menuScene.addObject(testcirc)
testimage = Object("TestImage",Vector2(10,200),size=Vector2(100,100))
testimage.addComponent(Components.Image(imageasset), assetsManager)
menuScene.addObject(testimage)

window = engine.Window()
window.create((1080,720), "Space Shootout")

window.sceneManager.addScene(menuScene)
window.sceneManager.loadScene("MenuScene")

handler = engine.EventHandler()
def inc_vel(pos, button, touch):
	dx = (10 if button == BUTTON_LEFT else -10)
	window.sceneManager.current_scene.objects["TestRect"].transform.velocity += Vector2(dx,0)
handler.onClose = window.__del__
handler.onMouseButtonDown = inc_vel

window.update()
window.handle_events(handler)
while window.running:
	window.render()
	window.update()
	window.handle_events(handler)

del window