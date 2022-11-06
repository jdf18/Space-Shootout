import engine
import game
from engine.assetsManager import AssetsManager, Asset
from pygame import Vector2, Vector3
from engine.constants import Constants
from engine.objects import Components, Object
from engine.sceneManager import Scene
from engine.util import createPrintCallback, copy_func
from engine.input import Input
from engine.particle import ParticleEmitter
from pygame import BUTTON_LEFT, BUTTON_RIGHT, image, transform
from json import dumps, loads
from random import shuffle
from engine.colliders import CircleCollider

global player, planets

assetsManager = AssetsManager()

window = engine.Window()
window.create((1024,1024), "Space Shootout")

handler = engine.EventHandler()
input_manager = Input(handler)

handler.onClose = window.__del__
window.bind_input_manager(input_manager)

def initMenuScene():
	screensize = window.dimensions
	menuScene = Scene("MenuScene", background_color=Vector3(42,52,64))

	menuScene.is_transfer:bool = False
	menuScene.orbit_angle:float = 0
	menuScene.transfer_value:float = 0
	menuScene.angular_velocity:float = 20
	menuScene.transfer_time:float = 5
	menuScene.orbit_radius:int = 200
	menuScene.planet_pos = Vector2(screensize[0]/2, screensize[1]/2)
	menuScene.on_update = game.menuScene_on_update
	menuScene.storage = {'planet_orbit':"sun","orbit_transfer":lambda a:Vector2(0,0),"transfer_time":0,"in_transfer":False,"waiting":False,"wanted_angle":0,"angle_reset":False}

	shuttle = Object("shuttle",Vector2(0,0),rotation=0, size=Vector2(50,50))
	shuttle.addComponent(Components.Image(assetsManager.addAsset(Asset.ImageAsset("assets/images/player.bmp"))),assetsManager)
	menuScene.addObject(shuttle)

	menuScene.planet_pos -= shuttle.transform.size/2

	planets_data = Asset.JSONAsset("assets/config/menu_planets.json")
	planets_data:dict[str,dict] = planets_data()
	planets = []
	def planet_click_callback(planet_name:str, window:engine.Window):
		#print("pcc", planet_name)
		if planet_name == "mars":
			window.sceneManager.reset_scene("1v1Scene")
			s = init1v1Scene()
			window.load_scene("1v1Scene")
			
	for name, data in planets_data.items():
		planetObj = game.Planet(name, data)
		planetObj.bind_image(assetsManager(Asset.ImageAsset(data["image"])))
		planets.append(planetObj)
		planetObj.position = Vector2(
			data["position"][0][0] + (data["position"][1][0] * screensize[0]),
			data["position"][0][1] + (data["position"][1][1] * screensize[1])
			)
		planetGObj = planetObj.createGameObject(window.dimensions, assetsManager, 0)
		def callback(name, window, position, button, touch, *args, **kwargs):
			planet_click_callback(name, window)
			createPrintCallback(name).__call__()
		window.input_manager.add_clickable_object("MenuScene", name)
		window.input_manager.add_clickable_callback("MenuScene", name, copy_func(callback))
		planetGObj.addComponent(Components.Clickable(True, CircleCollider()))
		menuScene.addObject(planetGObj)

		textObj = Object(name+"text",planetObj.position + Vector2(0,100*(-1 if data["position"][1][1] <= 0.5 else 1)), 0, Vector2(0,0))
		textObj.addComponent(Components.Text(data["text"],Vector3(230,230,230), assetsManager(Asset.TextAsset("assets/fonts/ROBOTO-THIN.TTF",32))), assetsManager)
		menuScene.addObject(textObj)

	return menuScene
def initSingleScene():
	global player, planets
	gameScene = Scene("GameScene", background_color=Vector3(42,52,64))

	player = game.Player(assetsManager(Asset.ImageAsset("assets/images/player.bmp")))
	player_obj = player.createGameObject(assetsManager)
	gameScene.addObject(player_obj)

	planets_data = Asset.JSONAsset("assets/config/planets.json")
	planets_data:dict[str,dict] = planets_data()
	planet_cull = lambda data : data["order"] < 5
	planets = []
	planetnos = [0,1,2,3]
	shuffle(planetnos)
	for i, (planet, data) in enumerate(planets_data.items()):
		if planet_cull(data):
			# create planet
			planetObj = game.Planet(planet, data)
			planetObj.bind_image(assetsManager(Asset.ImageAsset(data["image"])))
			planets.append(planetObj)
			if planetObj.name == "sun":
				gameObj = planetObj.createGameObject(window.dimensions, assetsManager, 0)
			else:
				gameObj = planetObj.createGameObject(window.dimensions, assetsManager, planetnos.pop())
			gameScene.addObject(gameObj)
	
	surfaces = []
	surf = transform.scale(image.load("assets/images/particle1.bmp"), (2,2))
	surfaces.append(surf)
	for i in range(3):
		surf = transform.rotate(surf, 30)
		surfaces.append(surf)
	gameScene.add_particle_emitter("engine",ParticleEmitter("engine", tuple(surfaces)))

	return gameScene

def init1v1Scene():
	global player1, player2, planets, player1hb, player2hb
	gameScene = Scene("1v1Scene", background_color=Vector3(42,52,64))
	gameScene.storage['reset_timer'] = None

	player1 = game.Player(assetsManager(Asset.ImageAsset("assets/images/player.bmp")),1)
	player1hb = game.HealthBar(3, Vector2(10,10))
	player1.link_health_bar(player1hb)
	player1_obj = player1.createGameObject(assetsManager)
	gameScene.addObject(player1_obj)
	gameScene.storage.update({"player1hb" : player1hb})

	player2 = game.Player(assetsManager(Asset.ImageAsset("assets/images/player.bmp")),2)
	player2.position = Vector2(*window.dimensions) - player1.position
	player2hb = game.HealthBar(3, Vector2(window.dimensions[0]-200-10, 10))
	player2.link_health_bar(player2hb)
	player2_obj = player2.createGameObject(assetsManager)
	gameScene.addObject(player2_obj)
	gameScene.storage.update({'player2hb' : player2hb})

	planets_data = Asset.JSONAsset("assets/config/planets.json")
	planets_data:dict[str,dict] = planets_data()
	planet_cull = lambda data : data["order"] < 5
	planets = []
	planetnos = [0,1,2,3]
	shuffle(planetnos)
	for i, (planet, data) in enumerate(planets_data.items()):
		if planet_cull(data):
			# create planet
			planetObj = game.Planet(planet, data)
			planetObj.bind_image(assetsManager(Asset.ImageAsset(data["image"])))
			planets.append(planetObj)
			if planetObj.name == "sun":
				gameObj = planetObj.createGameObject(window.dimensions, assetsManager, 0)
			else:
				gameObj = planetObj.createGameObject(window.dimensions, assetsManager, planetnos.pop())
			gameScene.addObject(gameObj)
	
	surfaces = []
	surf = transform.scale(image.load("assets/images/particle1.bmp"), (2,2))
	surfaces.append(surf)
	for i in range(3):
		surf = transform.rotate(surf, 30)
		surfaces.append(surf)
	surf = transform.scale(image.load("assets/images/particle2.bmp"), (2,2))
	surfaces.append(surf)
	for i in range(3):
		surf = transform.rotate(surf, 30)
		surfaces.append(surf)
	gameScene.add_particle_emitter("engine1",ParticleEmitter("engine1", tuple(surfaces)))
	gameScene.add_particle_emitter("engine2",ParticleEmitter("engine2", tuple(surfaces)))

	gameScene.add_particle_emitter("exp1",ParticleEmitter("engine1", tuple(surfaces)))
	gameScene.add_particle_emitter("exp2",ParticleEmitter("engine2", tuple(surfaces)))

	surf = transform.scale(image.load("assets/images/particle3.bmp"), (4,4))
	gameScene.add_particle_emitter("turret1",ParticleEmitter("turret1", (surf,None),single=True, callback=game.bullet_collision_callback))
	gameScene.add_particle_emitter("turret2",ParticleEmitter("turret2", (surf,None),single=True, callback=game.bullet_collision_callback))

	msgBox = Object("msgBox",Vector2(*window.dimensions)/4,size=Vector2(window.dimensions[0]/2,window.dimensions[1]/2))
	msgBox.addComponent(Components.Primitive(Constants.PRIMITIVE_RECTANGLE, (15,15,15,200)))
	msgBox.primitive.should_render = False
	gameScene.addObject(msgBox)

	endMessage = Object("endMessage",Vector2(*window.dimensions)/2,size=Vector2(window.dimensions[0]/2, window.dimensions[1]/2))
	endMessage.addComponent(Components.Text("msg",Vector3(225,220,220),assetsManager(Asset.TextAsset("assets/fonts/ROBOTO-THIN.TTF",48))),assetsManager)
	endMessage.text.should_render = False
	gameScene.addObject(endMessage)

	gameScene.on_update = game.on_1v1Scene_update

	gameScene.on_render = game.on_render_1v1Scene
	gameScene.object_collision_callback = game.on_object_collision

	return gameScene


menuScene = initMenuScene()
window.sceneManager.addScene(menuScene, reset=initMenuScene)
game1v1Scene = init1v1Scene()
window.sceneManager.addScene(game1v1Scene, reset=init1v1Scene)
gameSingleScene = initSingleScene()
window.sceneManager.addScene(gameSingleScene)

window.start()

window.load_scene("MenuScene")
window.handle_events(handler)
window.update()
pp = game.PathPrediction(20)
while window.running:
	window.render()
	dt = window.update()
	current_scene = window.sceneManager.current_scene_name
	if current_scene == "MenuScene":
		pass
	elif current_scene == "1v1Scene":
		player.update(planets, window, dt)
		pp.update(planets, window)
	window.update_screen()
	window.handle_events(handler)

del window