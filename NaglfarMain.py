import sys
import pygame
import sqlite3
import NewGame_Sol
import math
from pygame.locals import *


import time
import random


#clock = pygame.time.Clock()

current_system = "Sol"
zoom_scale = 1
vertical_scroll_modifier = 0
horizontal_scroll_modifier = 0
scroll_accel_x = 0
scroll_accel_y = 0
vertical_scroll_speed = 0
horizontal_scroll_speed = 0

conn = sqlite3.connect('NewGame.db')    #Connection object that represents using connect() function of sqlite3 module. Also creates'NewGame.db'.
c = conn.cursor()

NewGame_Sol.initSol(conn, c)
draw_bodies_current_row = 1

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Naglfar")

def draw_background_colour():
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 128))
	screen.blit(background, (0,0))
	return

then = time.time() #Time before the operations start


def draw_bodies():      #Draw all bodies in current system
	number_of_bodies_to_draw_query = "SELECT COUNT(*) FROM bodies WHERE parent_system = '" +current_system+ "'"
	c.execute(number_of_bodies_to_draw_query)
	number_of_bodies_to_draw = c.fetchone()[0] #Get the number of bodies in the system so it knows how many times to run the draw loop
	draw_bodies_current_row = 1

	while draw_bodies_current_row <= number_of_bodies_to_draw: #Draw every body in the system
		x_position_query = "SELECT x_position FROM bodies WHERE rowid = " +str(draw_bodies_current_row)+ " AND parent_system = '" +current_system+ "'"
		y_position_query = "SELECT y_position FROM bodies WHERE rowid = " +str(draw_bodies_current_row)+ " AND parent_system = '" +current_system+ "'"
		c.execute(x_position_query)
		x_position = c.fetchone()[0]
		x_body_draw = round(x_position*zoom_scale) + round(horizontal_scroll_modifier)
		c.execute(y_position_query)
		y_position = c.fetchone()[0]
		y_body_draw = round(y_position*zoom_scale) + round(vertical_scroll_modifier)
		pygame.draw.circle(screen, (255, 255, 0), (x_body_draw, y_body_draw), 10)
		draw_bodies_current_row = draw_bodies_current_row + 1
	return


#DO YOUR OPERATIONS HERE

now = time.time() #Time after it finished

print("It took: ", now-then, " seconds")









def update_all_body_positions():

	number_of_bodies_query = "SELECT COUNT(*) FROM bodies"
	c.execute(number_of_bodies_query)
	number_of_bodies_to_update = c.fetchone()[0]

	update_bodies_current_row = 1
	update_all_body_orbit_angles_query = "UPDATE bodies SET current_orbit_angle = current_orbit_angle + orbit_angle_change_per_second"
	c.execute(update_all_body_orbit_angles_query)

	while update_bodies_current_row <= number_of_bodies_to_update:

		get_body_current_orbit_angle_query = "SELECT current_orbit_angle FROM bodies WHERE rowid = " +str(update_bodies_current_row)+ ""
		get_body_orbit_distance_query = "SELECT orbit_distance FROM bodies WHERE rowid = " +str(update_bodies_current_row)+ ""

		c.execute(get_body_current_orbit_angle_query)
		body_current_orbit_angle = c.fetchone()[0]

		#Stops body_current_orbit_angle from getting too big and crashing everything
		if body_current_orbit_angle > (2*math.pi):
			body_current_orbit_angle = body_current_orbit_angle - (2*math.pi)

		c.execute(get_body_orbit_distance_query)
		body_orbit_distance = c.fetchone()[0]

		get_parent_body_query = "SELECT parent_body FROM bodies WHERE rowid = " +str(update_bodies_current_row)+ "" #Get name of parent body
		c.execute(get_parent_body_query)
		parent_body_name = c.fetchone()[0]

		if parent_body_name != "None":

			get_parent_body_x_position_query = "SELECT x_position FROM bodies WHERE body_name = '" +parent_body_name+ "'"
			c.execute(get_parent_body_x_position_query)
			parent_body_x_position = c.fetchone()[0]

			get_parent_body_y_position_query = "SELECT y_position FROM bodies WHERE body_name = '" +parent_body_name+ "'"
			c.execute(get_parent_body_y_position_query)
			parent_body_y_position = c.fetchone()[0]

			new_body_x_position = parent_body_x_position + (body_orbit_distance*(math.cos(body_current_orbit_angle)))
			new_body_y_position = parent_body_y_position + (body_orbit_distance*(math.sin(body_current_orbit_angle)))

			update_body_x_position_query = "UPDATE bodies SET x_position = " +str(new_body_x_position)+ " WHERE rowid = " +str(update_bodies_current_row)+ ""
			update_body_y_position_query = "UPDATE bodies SET y_position = " +str(new_body_y_position)+ " WHERE rowid = " +str(update_bodies_current_row)+ ""
			c.execute(update_body_x_position_query)
			c.execute(update_body_y_position_query)

			update_bodies_current_row = update_bodies_current_row + 1
		
		else:

			update_bodies_current_row = update_bodies_current_row + 1

#Main loop of game
while True:

	draw_background_colour()
	update_all_body_positions()
	draw_bodies()
	pygame.display.update()






	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == pygame.K_KP_PLUS:
				zoom_scale = zoom_scale - 0.2
				if zoom_scale < 0.2:
					zoom_scale = 0.2
					print(zoom_scale)
			if event.key == pygame.K_KP_MINUS:
				zoom_scale = zoom_scale + 0.2
				if zoom_scale > 5:
					zoom_scale = 5
					print(zoom_scale)


	scroll_key = pygame.key.get_pressed()				
	if scroll_key[pygame.K_UP]:
		scroll_up = True
		if scroll_up == True:
			scroll_accel_y = 0.05
			vertical_scroll_speed = vertical_scroll_speed + scroll_accel_y
			if vertical_scroll_speed > 3:
				vertical_scroll_speed = 3
	else:
		scroll_up = False

	if scroll_key[pygame.K_DOWN]:
		scroll_down = True
		if scroll_down == True:
			scroll_accel_y = -0.05
			vertical_scroll_speed = vertical_scroll_speed + scroll_accel_y
			if vertical_scroll_speed < -3:
				vertical_scroll_speed = -3
	else:
		scroll_down = False

	if scroll_key[pygame.K_LEFT]:
		scroll_left = True
		if scroll_left == True:
			scroll_accel_x = 0.05
			horizontal_scroll_speed = horizontal_scroll_speed + scroll_accel_x
			if horizontal_scroll_speed > 3:
				horizontal_scroll_speed = 3
	else:
		scroll_left = False

	if scroll_key[pygame.K_RIGHT]:
		scroll_right = True
		if scroll_right == True:
			scroll_accel_x = -0.05
			horizontal_scroll_speed = horizontal_scroll_speed + scroll_accel_x
			if horizontal_scroll_speed < -3:
				horizontal_scroll_speed = -3
	else:
		scroll_right = False

	if vertical_scroll_speed > 0 and scroll_up == False:
		scroll_accel_y = -0.05
		vertical_scroll_speed = vertical_scroll_speed + scroll_accel_y
		if vertical_scroll_speed <= 0.05:
			vertical_scroll_speed = 0.00

	if vertical_scroll_speed < 0 and scroll_down == False:
		scroll_accel_y = 0.05
		vertical_scroll_speed = vertical_scroll_speed + scroll_accel_y
		if vertical_scroll_speed >= -0.05:
			vertical_scroll_speed = 0.00

	if horizontal_scroll_speed > 0 and scroll_left == False:
		scroll_accel_x = -0.05
		horizontal_scroll_speed = horizontal_scroll_speed + scroll_accel_x
		if horizontal_scroll_speed <= 0.05:
			horizontal_scroll_speed = 0.00

	if horizontal_scroll_speed < 0 and scroll_right == False:
		scroll_accel_x = 0.05
		horizontal_scroll_speed = horizontal_scroll_speed + scroll_accel_x
		if horizontal_scroll_speed >= -0.05:
			horizontal_scroll_speed = 0.00


	vertical_scroll_modifier = vertical_scroll_modifier + vertical_scroll_speed
	horizontal_scroll_modifier = horizontal_scroll_modifier + horizontal_scroll_speed

