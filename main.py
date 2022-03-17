import pygame
import math


pygame.init()

WIDTH, HEIGHT = 600,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")
WHITE = (255,255,255)
ORANGE = (255,165,0)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY = (80,78,91)
GOLD = (255,215,0)
Earth_radius = 16
masses ={"sun":1.98892*10**30 , "earth": 5.9742*10**24, "mars": 6.39*10**23,"mercury": 0.330*10**24,
"venus": 4.8685*10**24}

FONT = pygame.font.SysFont("comicsans",16)


#Pygame eventloop

def draw_window(win):
	win.fill((0,0,0))
	mercury_text = FONT.render("MERCURY",1,WHITE)
	venus_text = FONT.render("VENUS",1,WHITE)
	earth_text = FONT.render("EARTH",1,WHITE)
	mars_text = FONT.render("MARS",1,WHITE)

	pygame.draw.circle(win,DARK_GREY,(10,18),5)
	WIN.blit(mercury_text, (20,Earth_radius))

	pygame.draw.circle(win,GOLD,(10,36),5)
	WIN.blit(venus_text, (20,2*Earth_radius))

	pygame.draw.circle(win,BLUE,(10,54),5)
	WIN.blit(earth_text, (20,3*Earth_radius))

	pygame.draw.circle(win,RED,(10,72),5)
	WIN.blit(mars_text, (20,4*Earth_radius))
	


	
	


class Planet:

	AU = 149.6e6*1000#Astronomical unit [m]
	G = 6.67428e-11
	SCALE = 170/AU #1 AU is equal to 100 pixels
	TIMESTEP = 3600*24 #1 DAY

	def __init__(self,x,y,radius,color,mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass #kg

		self.sun = False#wheteher it's or it's not the sun
		self.distance_to_sun = 0

		self.orbit = []#track to all of the points this planet has traveled
		self.x_vel = 0
		self.y_vel = 0

	def draw(self,win):
		x = self.x*self.SCALE + WIDTH/2
		y = self.y*self.SCALE + HEIGHT/2

		if len(self.orbit)> 2:
			updated_points=[]#list of updated points
			for point in self.orbit:
				x,y = point
				x = x*self.SCALE+WIDTH/2
				y = y*self.SCALE + HEIGHT/2
				updated_points.append((x,y))

			
			for i in range(len(updated_points)-1):
				alpha = 1 if i > 50 else i/50
				color_a = (self.color[0]*alpha, self.color[1]*alpha, self.color[2]*alpha)
				pygame.draw.line(win,color_a,updated_points[i],updated_points[i+1])#False to not enclose the lines



		#legend
		 

		pygame.draw.circle(win,self.color,(x,y),self.radius)
		sun_text = FONT.render("SUN",1,WHITE)
		WIN.blit(sun_text, (-sun_text.get_width()/2+WIDTH/2,-sun_text.get_height()/2+HEIGHT/2))

		if not self.sun:
			distance_text=FONT.render(f"{round(self.distance_to_sun/1000),1} km",1,WHITE)
			WIN.blit(distance_text,(x-distance_text.get_width()/2,y-distance_text.get_height()/2))



	def attraction(self,other):
		other_x,other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y- self.y
		distance = math.sqrt(distance_x**2 + distance_y**2)

		if other.sun:
			self.distance_to_sun = distance

		force = self.G*self.mass*other.mass/distance**2
		theta = math.atan2(distance_y,distance_x)
		force_x = math.cos(theta)*force
		force_y = math.sin(theta)*force
		return force_x,force_y

	def update_position(self,planets):
		total_fx = total_fy = 0
		#sum the forces over all planets
		for planet in planets:
			if self==planet:
				continue


			fx,fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx/self.mass*self.TIMESTEP#a = F/m, vx = a_x*t
		self.y_vel += total_fy /self.mass*self.TIMESTEP #vy = a_y*t

		#upadte x and y position
		self.x += self.x_vel*self.TIMESTEP
		self.y += self.y_vel*self.TIMESTEP

		self.orbit.append((self.x,self.y))
		#
		if len(self.orbit) > 150:
			self.orbit.pop(0)


def main():

	run = True
	sun = Planet(0,0,50,ORANGE, masses["sun"])
	sun.sun = True

	earth = Planet(-1*Planet.AU,0,Earth_radius,BLUE,masses["earth"])
	earth.y_vel = 29.873*1000#m/s
	mars = Planet(-1.524*Planet.AU,0,Earth_radius-4, RED,masses["mars"])
	mars.y_vel = 24.077*1000

	mercury = Planet(0.387*Planet.AU,0, Earth_radius/2,DARK_GREY, masses["mercury"])
	mercury.y_vel = -47.4*1000

	venus= Planet(0.723*Planet.AU,0, Earth_radius-2,GOLD, masses["venus"])
	venus.y_vel=-35.02*1000 #m/s



	planets = [sun,earth,mars,mercury,venus]

	clock = pygame.time.Clock()
	while run:
		clock.tick(60)#updates for second
		draw_window(WIN)
		#

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)


		pygame.display.update()
	pygame.quit()

if __name__ == "__main__": #we only run the game when we run this file 
	main()
