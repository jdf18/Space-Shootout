from math import cos, degrees, floor, log10, sin, radians, tan
from random import randint
from time import sleep
from threading import Thread

from pygame import Vector2
from pygame.surface import Surface
from engine.assetsManager import AssetsManager
from engine.objects import Object, Components
from engine import Window
from engine.sceneManager import Scene
from engine.colliders import Collider, CircleCollider
from engine.util import get_lerp, lerp

class HealthBar:
	def __init__(self, max_health:int, location:Vector2, init_health=None):
		if init_health == None: init_health = max_health
		self.health = min(max_health, init_health)
		self.max_health = max_health
		self.bar_length = 200
		self.ratio = self.bar_length / self.max_health # pixels per unit health
		self.location = location
		self.height = 25

		self.visual_health = init_health
		self.health_change_speed = 0.5
	def set_health(self, value:int):
		self.health = max(0,min(self.max_health, value))
	def get_health(self) -> int:
		return self.health
	def render(self, screen, pygame):
		#self.visual_health
		#if self.health: pygame.draw.rect(screen, (255,0,0), (self.location.x, self.location.y, self.health*self.ratio, self.height))
		#pygame.draw.rect(screen, (255,255,255), (self.location.x, self.location.y, self.bar_length, self.height), 4)
		# ! this is meant to look good but it doesn't really work
		# TODO
		transition_width = 0
		transition_color = (255,0,0)

		if self.visual_health < self.health:
			self.visual_health += self.health_change_speed
			transition_width = (self.health - self.visual_health)/self.ratio
			transition_color = (0,255,0)
		elif self.visual_health > self.health:
			self.visual_health -= self.health_change_speed
			transition_width = (self.health - self.visual_health)/self.ratio
			transition_color = (255,255,0)

		if self.health: pygame.draw.rect(screen, (255,0,0), (self.location.x+(self.visual_health*self.ratio), self.location.y, (self.health-self.visual_health)*self.ratio, self.height))
		if self.health: pygame.draw.rect(screen, (255,0,0), (self.location.x, self.location.y, self.health*self.ratio, self.height))
		pygame.draw.rect(screen, (255,255,255), (self.location.x, self.location.y, self.bar_length, self.height), 4)

	def __iadd__(self, other:int):
		self.health += other
		return self
	def __isub__(self, other:int):
		self.health -= other
		return self


class Planet:
	def __init__(self, name:str, planetData:dict) -> None:
		self.name:str = name
		self.order:int = planetData["order"]
		self.distance:int = planetData["distance"]
		self.mass:int = planetData["mass"]

		self.position = None
		self.diameter = None
	def bind_image(self, image_asset_id: int):
		self.image_asset_id:int = image_asset_id

	def calculate_position(self, screensize: tuple[int,int], orbitno:int) -> int:
		if self.position == None:
			centre = Vector2(screensize[0]/2,screensize[1]/2)
			if self.distance == 0: self.position = centre - self.size/2
			else:
				MAXDISTANCE = 270000000
				OFFSET = 150
				PLANET_COUNT = 5-1
				theta = 360/PLANET_COUNT * orbitno
				rand_angle = randint(floor(-360/PLANET_COUNT/3),floor(360/PLANET_COUNT/3))
				distance = OFFSET + floor(self.distance/MAXDISTANCE*((min(screensize)-OFFSET)/2-100))
				self.position = centre + Vector2(cos(radians(theta+rand_angle)),sin(radians(theta+rand_angle)))*distance
		self.position -= self.size/2
		return self.position
	def calculate_diameter(self):
		if self.name == "sun": 
			self.diameter = 75
		else:
			MAXMASS = (6.2E24)
			MAXDIAMETER = 25
			DIAMETEROFFSET = 20
			self.diameter = DIAMETEROFFSET + floor((self.mass)/MAXMASS*MAXDIAMETER)
		self.size = Vector2(self.diameter,self.diameter)
		return self.diameter
	def createGameObject(self, window_dimensions: tuple, assetsManager:AssetsManager, orbitno:int) -> Object:
		self.calculate_diameter()
		self.calculate_position(window_dimensions, orbitno)
		self.obj = Object(self.name,self.position, size=self.size, tags=["planet"])
		self.obj.addComponent(Components.Image(self.image_asset_id), assetsManager)
		self.obj.collider = CircleCollider()
		return self.obj

class Player:
	def __init__(self, image_asset_id:int, player_id=0):
		self.position:Vector2 = Vector2(100,100)
		self.image_asset_id:int = image_asset_id

		self.ROTATION_SPEED = 60
		self.ACCEL_SPEED = 0.7
		self.GRAVITY_SCALE = 5e-25
		self.MAX_VELOCITY = 100

		self.cooldown = 0

		self.player_id = player_id
		self.id_str = ('' if player_id == 0 else str(player_id))
		self.objectname = "player" + (str(player_id) if player_id else "")
		self.scene = ("default" if not player_id else "1v1Scene")
		# ! this will probably cause errors
		# TODO 
		self.obj_name = "player"+self.id_str
		print(self.scene,'/',self.obj_name)

		self.keybinds = (
			{'forwards':'w','left':'a','right':'d','shoot':'s'}
			if player_id <= 1 else 
			{'forwards':'UP','left':'LEFT','right':'RIGHT','shoot':'DOWN'}
			)
	def createGameObject(self, assetsManager:AssetsManager) -> Object:
		self.obj = Object(self.obj_name,self.position,size=Vector2(50,50), tags=["player"])
		self.obj.addComponent(Components.Image(self.image_asset_id), assetsManager)
		self.obj.collider = CircleCollider()
		return self.obj
	
	def update(self, planets:list[Planet], window:Window, dt:float):
		screen_dimensions = window.dimensions
		self.controls(window, planets, dt)
		self.check_edges(window, screen_dimensions)
	
	def controls(self, window:Window, planets:list[Planet], dt:float):
		a_pressed = window.input_manager.get_key(self.keybinds['left'])
		d_pressed = window.input_manager.get_key(self.keybinds['right'])
		if a_pressed and (not d_pressed):
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation += self.ROTATION_SPEED*dt
		elif (not a_pressed) and d_pressed:
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation -= self.ROTATION_SPEED*dt

		w_pressed = window.input_manager.get_key(self.keybinds['forwards'])
		if w_pressed:
			accel_force = Vector2(0,0)
			accel_force.from_polar(
				(self.ACCEL_SPEED, 270-window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation)
			)
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.velocity += accel_force
			if randint(1,2):
				for _ in range(5):
					vel, engine_offset = Vector2(0,0), Vector2(0,0)
					engine_offset.from_polar((-25,window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation-90+randint(-10,10)))
					engine_offset.x = -engine_offset.x
					vel.from_polar((0.2,window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation-90+randint(-75,75)))
					window.sceneManager.scenes[self.scene].particle_emitters["engine"+self.id_str].emit(
						list(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position + \
							window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2 + engine_offset),
						list(vel)
					)
		
		s_pressed = window.input_manager.get_key(self.keybinds['shoot'])
		self.cooldown = max(0, self.cooldown-dt)
		RELOAD_TIME = 0.5
		if s_pressed:
			# Fire
			try:
				if self.cooldown <= 0:
					self.cooldown += RELOAD_TIME
					vel, turret_offset = Vector2(0,0), Vector2(0,0)
					turret_offset.from_polar((-25,window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation+90))
					turret_offset.x = -turret_offset.x
					VEL_MAG_DELTA = 75
					vel.from_polar((abs(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.velocity.magnitude())+VEL_MAG_DELTA,
						(-window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.rotation-90+randint(-3,3))))
					window.sceneManager.scenes[self.scene].particle_emitters["turret"+self.id_str].emit(
						list(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position + \
							window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2 + turret_offset),
						list(vel),
						(15,18)
					)
			except:
				pass # Scene not created turret yet

		if window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.velocity.magnitude_squared() >= self.MAX_VELOCITY*self.MAX_VELOCITY:
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.velocity = \
				window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.velocity.normalize()*self.MAX_VELOCITY
		
		window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.force = self.calcualte_resultant_gravity(planets, window)

	def check_edges(self, window:Window, screen_dimensions:tuple):
		player_position = window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position + \
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2
		centre_offset = window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2
		if not 0 <= player_position.x <= screen_dimensions[0]:
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position.x = \
				(screen_dimensions[0] if player_position.x-centre_offset.x<=0 else 0)-centre_offset.x
		elif not 0 <= player_position.y <= screen_dimensions[1]:
			window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position.y = \
				(screen_dimensions[1] if player_position.y-centre_offset.y<=0 else 0)-centre_offset.y
	
	def calcualte_resultant_gravity(self, planets:list[Planet], window:Window):
		gravity = Vector2(0,0)
		for planet in planets:
			delta = (
				(window.sceneManager.scenes[self.scene].objects[planet.name].transform.position + \
					(window.sceneManager.scenes[self.scene].objects[planet.name].transform.size/2)) - \
					(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position + \
						(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2)))
			
			try:
				magnitude = delta.magnitude()
				delta = Vector2(planet.mass*delta.x/magnitude,planet.mass*delta.y/magnitude)*self.GRAVITY_SCALE
			except:
				delta = Vector2(0,0)
			window.draw_line(
				(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position + \
					(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2)),
				(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.position + \
					(window.sceneManager.scenes[self.scene].objects[self.obj_name].transform.size/2))+delta*10
			)
			gravity += delta
		return gravity
	
	def link_health_bar(self, hb:HealthBar):
		self.set_health = hb.set_health
		self.get_health = hb.get_health

class PathPrediction:
	def __init__(self, iterations:int, scene:str, object_name):
		self.MAX_ITERATIONS = iterations
		self.GRAVITY_SCALE = 5e-25
		self.scene = scene
		self.object_name = object_name
	def update(self, planets:list[Planet], window:Window):
		dt=0.25
		last_point:Vector2 = self.get_player_pos(window)
		velocity:Vector2 = window.sceneManager.scenes[self.scene].objects[self.object_name].transform.velocity.copy()
		for i in range(self.MAX_ITERATIONS):
			force = self.calcualte_resultant_gravity(planets, window, last_point)
			velocity += force*dt
			new_point = last_point + velocity*dt
			if not (0 < new_point.x < window.dimensions[0] and 0 < new_point.y < window.dimensions[1]):
				break
			window.draw_line(last_point, new_point)
			last_point = new_point

	def get_player_pos(self, window:Window) -> Vector2:
		return (window.sceneManager.scenes[self.scene].objects[self.object_name].transform.position + \
			   (window.sceneManager.scenes[self.scene].objects[self.object_name].transform.size/2)).copy()

	def calcualte_resultant_gravity(self, planets:list[Planet], window:Window, position:Vector2):
		gravity = Vector2(0,0)
		for planet in planets:
			delta = (
				(window.sceneManager.scenes[self.scene].objects[planet.name].transform.position + \
					(window.sceneManager.scenes[self.scene].objects[planet.name].transform.size/2)) - \
					position)
			try:
				magnitude = delta.magnitude()
				delta = Vector2(planet.mass*delta.x/magnitude,planet.mass*delta.y/magnitude)*self.GRAVITY_SCALE
			except:
				delta = Vector2(0,0)
			gravity += delta
		return gravity

def menuScene_on_update(scene:Scene, dt:float, window:Window):
	# Sets the position of the shuttle when the menu screen is open
	if scene.is_transfer:
		scene.transfer_value += dt / scene.transfer_time
		# TODO Calculate position
		scene.objects["shuttle"].transform.position = Vector2(0,0)
	else:
		scene.orbit_angle += scene.angular_velocity * dt
		# TODO Calculate position
		pos = scene.planet_pos + Vector2(cos(radians(scene.orbit_angle)), sin(radians(scene.orbit_angle)))*scene.orbit_radius
		scene.objects["shuttle"].transform.position = pos
		scene.objects["shuttle"].transform.rotation = 180 - scene.orbit_angle

	pos = window.input_manager.get_mouse_pos()
	# ! This does not work at all (kinda) and looks really janky
	# TODO
	# if scene.storage["waiting"]:
	# 	ang = Vector2(1,0).angle_to(scene.objects["shuttle"].transform.position-scene.planet_pos)
	# 	if ang > scene.storage["wanted_angle"] and scene.storage["angle_reset"]:
	# 		scene.storage["waiting"] = False
	# 	elif ang < scene.storage["wanted_angle"] and scene.storage["angle_reset"]:
	# 		scene.storage["angle_reset"] = True

	if scene.storage["in_transfer"]: #and (not scene.storage["waiting"]):
		scene.storage["transfer_time"] += dt
		scene.objects["shuttle"].transform.position = scene.storage["orbit_transfer"].__call__(scene.storage["transfer_time"]) - (scene.objects["shuttle"].transform.size/2)
		if scene.storage["transfer_time"] > 1:
			scene.storage["in_transfer"] = False
			scene.planet_pos = scene.objects[scene.storage['planet_orbit']].transform.position
			scene.orbit_angle = Vector2(1,0).angle_to(scene.objects["shuttle"].transform.position-scene.planet_pos)
		return # dont check the mouse position again
	# get the planet the mouse is currently over and calculate a orbital path
	for obj in scene.objects.values():
		if "planet" in obj.tags:
			col:bool = obj.collider.test(pos)
			if col:
				if scene.storage["planet_orbit"] != obj.name:
					scene.storage["in_transfer"] = True
					scene.storage["waiting"] = True
					scene.storage["transfer_time"] = 0
					scene.storage["orbit_transfer"], scene.storage["wanted_angle"] = get_transfer(
						scene.objects[obj.name].transform.position + (scene.objects[obj.name].transform.size/2),
						scene.objects[obj.name].transform.size.x/2+scene.orbit_radius,
						scene.objects[scene.storage["planet_orbit"]].transform.position + (scene.objects[scene.storage["planet_orbit"]].transform.size/2),
						scene.objects[scene.storage["planet_orbit"]].transform.size.x/2+scene.orbit_radius,
					)
					scene.storage["angle_reset"] = (Vector2(1,0).angle_to(scene.objects["shuttle"].transform.position-scene.planet_pos) < scene.storage["wanted_angle"])
				scene.storage['planet_orbit'] = obj.name

def get_transfer(c1:Vector2,r1:float,c2:Vector2,r2:float, theta=10) -> tuple[callable, float]:
	# Generate a funciton that returns the position of the shuttle during transfers and angle needed to start one
	P1 = c1 + (c2-c1).normalize().rotate(-90+theta)*r1
	P3 = c2 + (c2-c1).normalize().rotate(-90-theta)*r2
	a = -1/(tan(-90+theta+(c2-c1).as_polar()[1]))
	b = 1/(tan(-90+theta+(c2-c1).as_polar()[1]))*P1.x+P1.y
	c = -1/(tan(-90-theta+(c2-c1).as_polar()[1]))
	d = 1/(tan(-90-theta+(c2-c1).as_polar()[1]))*P3.x+P3.y
	P2 = Vector2(
		(d-b)/(a-c),
		a*(d-b)/(a-c)+b
	)
	def foo(t:float):
		return lerp(t,
			lerp(t,P1,P2),
			lerp(t,P2,P3)
		)
	angle = Vector2(1,0).angle_to(P1-c1)
	return foo, angle

def on_render_1v1Scene(self:Scene, pygame, screen:Surface, dt:float):
	self.storage['player1hb'].render(screen, pygame)
	self.storage['player2hb'].render(screen, pygame)

def bullet_collision_callback(window:Window, name:str, other_name:str, life:float):
	def check_if_kill():
		if window.sceneManager.current_scene.storage["player1hb"].get_health() == 0:
			on_end_game(window, 1)
		elif window.sceneManager.current_scene.storage["player2hb"].get_health() == 0:
			on_end_game(window, 2)
	if window.sceneManager.current_scene_name == "1v1Scene":
		if other_name == "player1" and (not name == "turret1"):
			window.sceneManager.current_scene.storage["player1hb"] -= 1
			check_if_kill()
			return True
		elif other_name == "player2" and (not name == "turret2"):
			window.sceneManager.current_scene.storage["player2hb"] -= 1
			check_if_kill()
			return True
		elif other_name in ['player1', 'player2']:
			return False
		else:
			return True
	return False

def on_object_collision(window:Window, objA:Object, objB:Object):
	if ("player" in objA.tags) and ("planet" in objB.tags):
		#window.sceneManager.current_scene.objects[objA.name]
		window.sceneManager.current_scene.storage[objA.name.lower()+"hb"].set_health(0)
		t1 = Thread(target=on_end_game, args=(window, (1 if objA.name == "player1" else 2)), daemon=True)
		t1.start()
		
def explosion(window:Window, player_id:int):
	for i in range(300):
		pe = window.sceneManager.current_scene.particle_emitters["exp"+str(player_id)]
		vel = Vector2(0,0)
		vel.from_polar((randint(10,50),randint(0,360)))
		pe.emit(
			window.sceneManager.current_scene.objects["player"+str(player_id)].transform.position + (window.sceneManager.current_scene.objects["player"+str(player_id)].transform.size/2),
			vel, (20,30)
		)
		window.sceneManager.current_scene.objects["player"+str(player_id)].image.should_render = False

def on_end_game(window:Window, player_id:int):
	if not window.sceneManager.current_scene.storage['reset_timer']:
		explosion(window, player_id)
		window.sceneManager.current_scene.objects["endMessage"].text.text = f"Player {('2' if player_id == 1 else '1')} Wins!"
		window.sceneManager.current_scene.objects["endMessage"].text.should_render = True
		window.sceneManager.current_scene.objects["msgBox"].primitive.should_render = True
		window.sceneManager.current_scene.storage['reset_timer'] = float(5)
	return

def on_1v1Scene_update(scene:Scene, dt:float, window:Window):
	if type(scene.storage['reset_timer']) == float:
		if scene.storage['reset_timer'] < 0:
			window.sceneManager.reset_scene("MenuScene")
			window.sceneManager.loadScene("MenuScene")
			scene.storage['reset_timer'] = None
		else:
			scene.storage['reset_timer'] -= dt

