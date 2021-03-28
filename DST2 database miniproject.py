# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 00:44:39 2020

@author: Eleanor
"""

from psycopg2 import connect, sql
user_name = "postgres" #the username for accessing your postgreSQL
user_pass = "***" #the password for accessing your postgreSQL

import sys
import re
import pygame
from pygame.locals import *

# Set the DB name, table, and table data to 'None'
db_name = "covid19"
country = None
date=None
rank = None
month=None
date_input=None

# Initialize the output with None
month_ranking_return = None
country_return = None
newly_confirmed_return = None
worldwide_return = None

#Set the width and height of the displaying screen
display_width = 650
display_height = 700

#Define the color
WHITE = (255, 255, 255)
RED = (255, 0, 0)
gray = (128,128,128)
black = (0, 0, 0, 255)

#Set the location of the picture for the start screen
bg_location = '~/Image for start screen.jpg'

pygame.init()

# create a class for the buttons and labels
class Button():

    # empty list for button registry
    registry = []

    # selected button (will have outline rect)
    selected = None

    # pygame RGBA colors
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    red = (255, 0, 0, 255)
    green = (50, 205, 50, 255)
    light_blue = (173, 216, 230, 255)

    # default font color for buttons/labels is white
    def __init__(self, name, loc, color=white):

        # add button to registry
        self.registry.append(self)

        # paramater attributes
        self.name = name
        self.loc = loc
        self.color = color

        # text attr for button
        self.text = ""

        # size of button changes depending on length of text
        self.size = (int(len(self.text)*200), 200)

        # font.render(text, antialias, color, background=None) -> Surface
        self.font = font.render (
            self.name + " " + self.text, # display text
            True, # antialias on
            self.color, # font color
            self.black # background color
        )

        # rect for button
        self.rect = self.font.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        
#Create a class for the buttons on the start screen
class Button1(object):
	def __init__(self, text, color, x=None, y=None, **kwargs):
        #set the surface, width and height for button displaying
		self.surface = font.render(text, True, color)
		self.WIDTH = self.surface.get_width()
		self.HEIGHT = self.surface.get_height()
        #Define attributes to allow the button to be displayed at the centre of the screen.
		if 'centered_x' in kwargs and kwargs['centered_x']:
			self.x = display_width // 2 - self.WIDTH // 2
		else:
			self.x = x
		if 'centered_y' in kwargs and kwargs['cenntered_y']:
			self.y = display_height // 2 - self.HEIGHT // 2
		else:
			self.y = y
    #Define a function to display the button on the screen
	def display(self):
		screen.blit(self.surface, (self.x, self.y))
    #Define a function to check whether the user click or pass on the button
	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
		y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
		if x_match and y_match:
			return True
		else:
			return False
        

def connect_postgres(db):

    # connect to PostgreSQL
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            dbname = db,
            user = user_name,
            host = "localhost",
            password = user_pass
        )
    except Exception as err:
        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    # return the connection object
    return conn


def return_increase_rate_records(conn):
    if country== None or country== '':
        return None
    SQLquery='SELECT country_data.iso2,country_data.iso3,daily_report.country,daily_report.newly_confirmed FROM daily_report \
    INNER JOIN country_data ON daily_report.country=country_data.country \
    WHERE CAST(date AS VARCHAR(50))= \''+str(date)+'\' AND (country_data.iso2 = \''+str(country)+'\' OR country_data.iso3=\''+str(country)+'\' OR daily_report.country = \''+str(country)+'\')'
    print(SQLquery)
    # instantiate a new cursor object
    cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        SQLquery
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        newly_confirmed_return = cursor.fetchall()

        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        newly_confirmed_return = None

    return newly_confirmed_return


def return_ranking_records(conn):
    if rank== None or rank== '':
        return None
    SQLquery='SELECT * FROM get_increase_rate(\''+str(rank)+'\',\''+str(month)+'\');'
    print(SQLquery)
    # instantiate a new cursor object
    cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        SQLquery
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        month_ranking_return = cursor.fetchall()

        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        month_ranking_return = None

    return month_ranking_return


def return_worldwide(conn):
    if date_input==None or date_input=='':
        return None
    SQLquery='SELECT increase_rate_w FROM worldwide_daily_increase_rate WHERE CAST(date AS VARCHAR(50))=\''+str(date_input)+'\';'
    print(SQLquery)
    cursor = conn.cursor()
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        SQLquery
    )
    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        worldwide_return = cursor.fetchall()

        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        worldwide_return = None

    return worldwide_return


def return_country_records(conn):
    if date_input== None or date_input== '':
        return None
    SQLquery='SELECT daily_report.country,daily_report.increase_rate  FROM daily_report \
    INNER JOIN worldwide_daily_increase_rate ON daily_report.date=worldwide_daily_increase_rate.date \
    WHERE CAST(daily_report.date AS VARCHAR(50))=\''+str(date_input)+'\' AND daily_report.increase_rate > worldwide_daily_increase_rate.increase_rate_w \
    ORDER BY daily_report.increase_rate DESC \
    LIMIT 8;'

    print(SQLquery)
    # instantiate a new cursor object
    cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        SQLquery
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        country_return = cursor.fetchall()
        
        
        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        country_return = None

    return country_return


#Define a function to create the start screen of the software
def starting_screen():
	pygame.init()
	pygame.display.set_caption("2020 DST2 Final Project ", "2020 DST2 Final Project")
	screen.blit(bg, (92,48)) #Display the image
    #Create buttons for three queries
	Query1_button = Button1('Country daily report', WHITE, None, 405, centered_x=True)
	Query2_button = Button1('Increase rate ranking', WHITE, None, 495, centered_x=True)
	Query3_button = Button1('Increase rate higher than worldwide', WHITE, None, 585, centered_x=True)
    #Display the buttons created
	Query1_button.display()
	Query2_button.display()
	Query3_button.display()
    #Update
	pygame.display.update()

    #Check if the mouse post on a speific button, and make the button turn red when there is a mouse posting on it.
	while True:
		if Query1_button.check_click(pygame.mouse.get_pos()):
			Query1_button = Button1('Country daily report', RED, None, 405, centered_x=True)
		else:
			Query1_button = Button1('Country daily report', WHITE, None, 405, centered_x=True)

		if Query2_button.check_click(pygame.mouse.get_pos()):
			Query2_button = Button1('Increase rate ranking', RED, None, 495, centered_x=True)
		else:
			Query2_button = Button1('Increase rate ranking', WHITE, None, 495, centered_x=True)
        
		if Query3_button.check_click(pygame.mouse.get_pos()):
			Query3_button = Button1('Increase rate higher than worldwide', RED, None, 585, centered_x=True)
		else:
			Query3_button = Button1('Increase rate higher than worldwide', WHITE, None, 585, centered_x=True)
       
        #Display the buttons
		Query1_button.display()
		Query2_button.display()
		Query3_button.display()
		pygame.display.update()
        
        #Check for the quit event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				raise SystemExit
        
        #Check whick button is clicked, and change to the corresponding query screen.
		if pygame.mouse.get_pressed()[0]:
			if Query1_button.check_click(pygame.mouse.get_pos()):
				Query_1()
				break
			if Query2_button.check_click(pygame.mouse.get_pos()):
				Query_2()
				break
			if Query3_button.check_click(pygame.mouse.get_pos()):
				Query_3()
				break
       
        
#Define a function for the first query (get the newly confirmed number of a country on a specific day)
def Query_1():
    #Set the global variables
    global country
    country=None
    global date
    global newly_confirmed_return
    pygame.init()
    pygame.display.set_mode((1000, 1000))

    # change the caption for the Pygame app
    pygame.display.set_caption("2020 DST2 Final Project ", "2020 DST2 Final Project ")

    # create a pygame resizable screen
    screen = pygame.display.set_mode(
    (display_width,display_height),
    HWSURFACE | DOUBLEBUF| RESIZABLE
)
    try:
        font = pygame.font.SysFont('Arial', 20)
    except Exception as err:
        print ("pygame.font ERROR:", err)
        font = pygame.font.SysFont('Calibri', 20)

    # create buttons for PostgreSQL database and table, and the button for returning to the starting screen
    country_button = Button("Country and date:", (10, 50))
    return_button = Button("Back: click here and press return",(350,650))
    connection = None

    # begin the pygame loop
    app_running = True
    while app_running == True:

        # reset the screen
        screen.fill( Button.black )

        # set the clock FPS for app
        clock = pygame.time.Clock()

        # iterate over the pygame events
        for event in pygame.event.get():

            # user clicks the quit button on app window
            if event.type == QUIT:
                app_running = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                quit()

            # user presses a key on keyboard
            if event.type == KEYDOWN:

                if Button.selected != None:

                    # get the selected button
                    b = Button.selected

                    # user presses the return key
                    if event.key == K_RETURN:
                        newly_confirmed_return = None
                        # Check if the button is for the first query
                        if "Country" in b.name:
                            country = str(re.findall('(\D+)&',b.text))[2:-2]
                            date = str(re.findall('&(\S+)',b.text))[2:-2]
                        #If the return button is pressed
                        if "return" in b.name:
                            #Create a refresh button to avoid messages duplication
                            refresh_button = Button("                                                                                     ",(10, 50))
                            screen.blit(refresh_button.font,refresh_button.rect)
                            #Back to the start screen
                            starting_screen()
                            break
                        connection = connect_postgres( db_name )
                        newly_confirmed_return = return_increase_rate_records(connection)
                        Button.selected = None
                        print(newly_confirmed_return)
                        
                    else:
                        # get the key pressed
                        key_press = pygame.key.get_pressed()
                        # iterate over the keypresses
                        for keys in range(255):
                            if key_press[keys]:
                                if keys == 8: # backspace
                                    b.text = b.text[:-1]
                                else:
                                    # convert key to unicode string
                                    b.text += event.unicode
                                    print ("KEYPRESS:", event.unicode)

                    # append the button text to button font object
                    b.font = font.render(b.name + " " + b.text, True, Button.white, Button.black)

            # check for mouse button down events
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                print ("\nMOUSE CLICK:", event)

                # iterate over the button registry list
                for b in Button.registry:

                    # check if the mouse click collided with button
                    if b.rect.collidepoint(event.pos) == 1:
                        # store button object under selected attr
                        Button.selected = b

        # iterate over the button registry list
        for b in Button.registry:

            # blit the button's font to screen
            screen.blit(b.font, b.rect)

            # check if the button has been clicked by user
            if Button.selected == b:

                # blit an outline around button if selected
                rect_pos = (b.rect.x-5, b.rect.y-5, b.rect.width+1000, b.rect.height+10)
                pygame.draw.rect(screen, Button.white, rect_pos, 3) # width 3 pixels
        
        if country == None:
            #Blit the hint message for user to perform the query successfully
            blit_text = "Please type in your query (sample format:AF&2020-03-13)"
            blit_textb = "You can input either the iso or the full name of the country."
            blit_text2 = "And please press enter to start the query :)"
            conn_msg = font.render(blit_text, True, Button.green, Button.black)
            conn_m = font.render(blit_textb, True, Button.green, Button.black)
            conn_ms = font.render(blit_text2,True,Button.green,Button.black)
            screen.blit(conn_msg, (10, 150))
            screen.blit(conn_m, (10,200))
            screen.blit(conn_ms,(10,250))

        else:
            # connection is valid, but the data doesn't exist
            if connection != None and country!=None and date!=None and (newly_confirmed_return == None or len(newly_confirmed_return)==0):
                #if the queried month is earlier than 12 and the database doesn't have the data, this means the confirmed number is 0 (which has been deleted to avoid duplication when designing the database).
                if int(str(re.findall('-(\S+)-',date)[0])) < 12 :
                    blit_text = "The newly confirmed number of "+country+" on "+date+" is 0."
                    color = Button.light_blue
                else:
                    blit_text = "The PostgreSQL table does not have the record on this day."
                    color = Button.red
                # blit the message to the pygame screen
                conn_msg = font.render(blit_text, True, color, Button.black)
                screen.blit(conn_msg, (66, 180))
            #Invalid connection
            elif connection == None:
                blit_text = "PostgreSQL connection is invalid."
                color = Button.red
                # blit the message to the pygame screen
                conn_msg = font.render(blit_text, True, color, Button.black)
                screen.blit(conn_msg, (10, 300))
                
            if newly_confirmed_return != None :
                # enumerate the list of tuple rows
                for num, row in enumerate(newly_confirmed_return):
                    # blit the table data to Pygame window in a specific format
                    blit_text = (str(row).split("'")[1]+" | "+str(row).split("'")[3]+" | "+str(row).split("'")[5]+" | "+ "Newly confirmed:"+str(row).split("'")[6].split(",")[1].split(")")[0]).encode("utf-8","ignore")
                    table_font = font.render(blit_text, True, Button.light_blue, Button.black)
                    screen.blit(table_font, (140, 150+int(num*50)))
        # set the clock FPS for application
        clock.tick(20)
        # use the flip() method to display text on surface
        pygame.display.flip()
        pygame.display.update()
        
        
#Define the function for the second query (The increae rate in a specific month of a country, of a specific rank)
def Query_2():
    
    #Set the global variables
    global month
    global rank
    rank= None
    global month_ranking_return
    pygame.init()
    pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("2020 DST2 Final Project ", "2020 DST2 Final Project ")

#   create a pygame resizable screen
    screen = pygame.display.set_mode(
    (display_width,display_height),
    HWSURFACE | DOUBLEBUF| RESIZABLE
)
    try:
        font = pygame.font.SysFont('Arial', 20)
    except Exception as err:
        print ("pygame.font ERROR:", err)
        font = pygame.font.SysFont('Calibri', 20)
        
    #Create the buttons
    ranking_button = Button("Rank and month:", (10, 50))
    return_button = Button("Back: click here and press return",(350,650))
    
    connection = None

    # begin the pygame loop
    app_running = True
    while app_running == True:

        # reset the screen
        screen.fill( Button.black )

        # set the clock FPS for app
        clock = pygame.time.Clock()

        # iterate over the pygame events
        for event in pygame.event.get():

            # user clicks the quit button on app window
            if event.type == QUIT:
                app_running = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                quit()

            # user presses a key on keyboard
            if event.type == KEYDOWN:

                if Button.selected != None:

                    # get the selected button
                    b = Button.selected

                    # user presses the return key
                    if event.key == K_RETURN:
                        month_ranking_return = None
                        #if this is the button for the second query
                        if "Rank" in b.name:
                            rank = str(re.findall('(\S+)&',b.text))[2:-2]
                            month = str(re.findall('&(\S+)',b.text))[2:-2]
                        #if the return button is clicked
                        elif"return" in b.name:
                            refresh_button = Button("                                    ",(10, 50))
                            screen.blit(refresh_button.font,refresh_button.rect)
                            starting_screen()
                            break
                        connection = connect_postgres( db_name )
                        month_ranking_return = return_ranking_records(connection)
                        Button.selected = None
                        print(month_ranking_return)
                    else:
                        # get the key pressed
                        key_press = pygame.key.get_pressed()

                        # iterate over the keypresses
                        for keys in range(255):
                            if key_press[keys]:
                                if keys == 8: # backspace
                                    b.text = b.text[:-1]
                                else:
                                    # convert key to unicode string
                                    b.text += event.unicode
                                    print ("KEYPRESS:", event.unicode)

                    # append the button text to button font object
                    b.font = font.render(b.name + " " + b.text, True, Button.white, Button.black)

            # check for mouse button down events
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                print ("\nMOUSE CLICK:", event)

                # iterate over the button registry list
                for b in Button.registry:

                    # check if the mouse click collided with button
                    if b.rect.collidepoint(event.pos) == 1:
                        # store button object under selected attr
                        Button.selected = b

        # iterate over the button registry list
        for b in Button.registry:

            # blit the button's font to screen
            screen.blit(b.font, b.rect)

            # check if the button has been clicked by user
            if Button.selected == b:

                # blit an outline around button if selected
                rect_pos = (b.rect.x-5, b.rect.y-5, b.rect.width+1000, b.rect.height+10)
                pygame.draw.rect(screen, Button.white, rect_pos, 3) # width 3 pixels
        
        #Blit hint message to guide the query
        if rank == None:
            blit_text = "Please type in your query (sample format:1&4)."
            blit_text2 ="The first number is rank and the second is month (2-11)."
            blit_text1 = "And please press enter to start your query :)"
            conn_msg = font.render(blit_text, True, Button.green, Button.black)
            c_msg=font.render(blit_text2, True, Button.green, Button.black)
            msg = font.render(blit_text1,True,Button.green,Button.black)
            screen.blit(conn_msg, (10, 150))
            screen.blit(c_msg,(10,200))
            screen.blit(msg,(10,250))
        else:
            #If the connection is valid but output is None
            if connection != None and rank!=None and month!=None and (month_ranking_return == None or len(month_ranking_return)==0):
                blit_text = "The PostgreSQL table does not have the record in this month."
                color = Button.red
                # blit the message to the pygame screen
                conn_msg = font.render(blit_text, True, color, Button.black)
                screen.blit(conn_msg, (66, 180))
            #Invalid connection
            elif connection == None:
                blit_text = "PostgreSQL connection is invalid."
                color = Button.red
                # blit the message to the pygame screen
                conn_msg = font.render(blit_text, True, color, Button.black)
                screen.blit(conn_msg, (10, 300))
            if month_ranking_return != None:

                # enumerate the list of tuple rows
                for num, row in enumerate(month_ranking_return):

                    # blit the table data to Pygame window
                    blit_text = (str(row).split("'")[1]+" | Monthly increase rate: "+str(row).split("'")[3]).encode("utf-8", "ignore")
                    table_font = font.render(blit_text, True, Button.light_blue, Button.black)
                    screen.blit(table_font, (150, 130 + int(num*50)))
        # set the clock FPS for application
        clock.tick(20)
        # use the flip() method to display text on surface
        pygame.display.flip()
        pygame.display.update()


#Define a function for the thrid query (Get the first 8 coutries with an daily inrease rate higher than worldwide)    
def Query_3():
    #Set the global variables
    global date_input
    date_input = None
    global country_return
    global worldwide_return
    pygame.display.set_mode((1000, 1000))

    # change the caption/title for the Pygame app
    pygame.display.set_caption("2020 DST2 Final Project ", "2020 DST2 Final Project ")

    # create a pygame resizable screen
    screen = pygame.display.set_mode(
    (display_width,display_height),
    HWSURFACE | DOUBLEBUF| RESIZABLE
)
    
    try:
        font = pygame.font.SysFont('Arial', 20)
    except Exception as err:
        print ("pygame.font ERROR:", err)
        font = pygame.font.SysFont('Calibri', 20)
        
    date_button = Button("Date:", (10, 50))
    return_button = Button("Back: click here and press return",(350,650))
    
    connection = None

    # begin the pygame loop

    app_running = True
    while app_running == True:

        # reset the screen
        screen.fill( Button.black )

        # set the clock FPS for app
        clock = pygame.time.Clock()

        # iterate over the pygame events
        for event in pygame.event.get():

            # user clicks the quit button on app window
            if event.type == QUIT:
                app_running = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                quit()

            # user presses a key on keyboard
            if event.type == KEYDOWN:

                if Button.selected != None:

                    # get the selected button
                    b = Button.selected

                    # user presses the return key
                    if event.key == K_RETURN:
                        country_return = None
                        #The button for query 3 is clicked
                        if "Date" in b.name:
                            date_input = b.text
                        #User clicks the return button
                        elif"return" in b.name:
                            #Refresh button to avoid message duplication
                            refresh_button = Button("                                    ",(10, 50))
                            screen.blit(refresh_button.font,refresh_button.rect)
                            starting_screen()
                            break
                        connection = connect_postgres( db_name )
                        country_return = return_country_records( connection )
                        worldwide_return = return_worldwide(connection)
                        Button.selected = None
                        print(worldwide_return)
                        print(country_return)
                        
                    else:
                        # get the key pressed
                        key_press = pygame.key.get_pressed()

                        # iterate over the keypresses
                        for keys in range(255):
                            if key_press[keys]:
                                if keys == 8: # backspace
                                    b.text = b.text[:-1]
                                else:
                                    # convert key to unicode string
                                    b.text += event.unicode
                                    print ("KEYPRESS:", event.unicode)

                    # append the button text to button font object
                    b.font = font.render(b.name + " " + b.text, True, Button.white, Button.black)

            # check for mouse button down events
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                print ("\nMOUSE CLICK:", event)

                # iterate over the button registry list
                for b in Button.registry:

                    # check if the mouse click collided with button
                    if b.rect.collidepoint(event.pos) == 1:
                        # store button object under selected attr
                        Button.selected = b

        # iterate over the button registry list
        for b in Button.registry:

            # blit the button's font to screen
            screen.blit(b.font, b.rect)

            # check if the button has been clicked by user
            if Button.selected == b:

                # blit an outline around button if selected
                rect_pos = (b.rect.x-5, b.rect.y-5, b.rect.width+1000, b.rect.height+10)
                pygame.draw.rect(screen, Button.white, rect_pos, 3) # width 3 pixels
        #Set the hint message to guide the user
        if date_input == None:
            blit_text = "Please type in your query (sample format:2020-03-13)."
            blit_text1 = "And please press enter to start your query :)"
            conn_msg = font.render(blit_text, True, Button.green, Button.black)
            msg = font.render(blit_text1,True,Button.green,Button.black)
            screen.blit(conn_msg, (10, 150))
            screen.blit(msg,(10,200))
        else:
            #If the connection is valid but there is no output
            if connection != None and date_input!=None and (country_return == None or len(country_return)==0) and len(worldwide_return)==0:
                blit_text = "The PostgreSQL table does not have the record on this day."
                color = Button.red
                # blit the message to the pygame screen
                conn_msg = font.render(blit_text, True, color, Button.black)
                screen.blit(conn_msg, (66, 180))
            #Invalide connenction
            elif connection == None:
                blit_text = "PostgreSQL connection is invalid."
                color = Button.red
                # blit the message to the pygame screen
                conn_msg = font.render(blit_text, True, color, Button.black)
                screen.blit(conn_msg, (10, 300))
            if country_return != None and len(country_return)!=0:
                blit_text0 = ("Worldwide increase rate: "+str(worldwide_return).split("'")[1]).encode("utf-8","ignore")
                table_font0 = font.render(blit_text0,True, Button.light_blue, Button.black)
                screen.blit(table_font0, (160, 120))

                # enumerate the list of tuple rows
                for num, row in enumerate(country_return):

                    # blit the table data to Pygame window
                    blit_text = (str(num+1)+": "+str(row).split("'")[1]+" | Increase rate: "+str(row).split("'")[3]).encode("utf-8", "ignore")
                    table_font = font.render(blit_text, True, Button.light_blue, Button.black)
                    screen.blit(table_font, (160, 170 + int(num*50) ))
        # set the clock FPS for application
        clock.tick(20)
        # use the flip() method to display text on surface
        pygame.display.flip()
        pygame.display.update()

#Set the displaying screen
screen = pygame.display.set_mode((display_width, display_height))
#load the image
bg = pygame.image.load(bg_location)
#Set the font style and size
font = pygame.font.SysFont('Arial', 20)
#Begin with the start screen
starting_screen()