#Script to build new Sol system for a new game.

def initSol(conn, c):
	c.execute('''DROP TABLE IF EXISTS system_list''')
	c.execute('''CREATE TABLE system_list (system_name TEXT NOT NULL PRIMARY KEY,primary_star_name TEXT NOT NULL,x_position REAL NOT NULL,y_position REAL NOT NULL)''')
	c.execute('''INSERT INTO system_list VALUES ('Sol','Sol','0','0')''')

	c.execute('''DROP TABLE IF EXISTS bodies''')
	c.execute('''CREATE TABLE bodies (parent_system TEXT NOT NULL,parent_body TEXT NOT NULL,body_name TEXT NOT NULL PRIMARY KEY,orbit_distance REAL NOT NULL,current_orbit_angle REAL NOT NULL,orbit_angle_change_per_second REAL NOT NULL,x_position REAL NOT NULL,y_position REAL NOT NULL)''')
	c.execute('''INSERT INTO bodies VALUES ('Sol','None','Sol','0','0','0','400','300')''')
	c.execute('''INSERT INTO bodies VALUES ('Sol','Sol','Earth','200','0','0.002','0','0')''')
	c.execute('''INSERT INTO bodies VALUES ('Sol','Earth','Moon','50','0','0.005','0','0')''')

	conn.commit()
#	conn.close()
