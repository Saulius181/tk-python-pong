#!/usr/bin/env python

__author__ = "Saulius Bartkus"
__copyright__ = "Copyright 2017"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Saulius Bartkus"
__email__ = "saulius181@yahoo.com"
__status__ = "Production"

from tkinter import *
import random
import time
import math
from shapely.geometry import Polygon, Point, box

FRAME_RATE = 10 # 100 frames per second 
HEIGHT = 310
WIDTH = 565

class game_controller(object):
	def new_game(self):
		if self.canvas.data["play"] is None:
			rand_pos = random.randint(50,250)
			self.ball = self.canvas.create_oval(200, rand_pos, 220, rand_pos+20, outline='black', fill="black")
			
			self.canvas.data["ReactTime"] = self.var.get()
			
			self.angle = random.uniform(0.5, math.pi - 0.5)
			
			self.canvas.data["Dir"] = {'x': math.sin(self.angle) * random.choice([-1, 1]), 'y': math.cos(self.angle) * random.choice([-1, 1])}
			self.canvas.data["Speed"] = 3
			self.canvas.data["xTurn"], self.canvas.data["yTurn"] = False, False
			self.canvas.data["play"] = True
			self.root.after(FRAME_RATE, self.moveit)
		elif self.canvas.data["play"] == True:
			self.canvas.data["play"] = False
			self.root.after(FRAME_RATE, self.new_game)
		else:
			self.root.after(FRAME_RATE, self.new_game)
		
	def quit(self):
		self.root.destroy()		
	
	def ai(self):
		if (self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2 < (self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2:
			if ((self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2) <= 60:	
				if ((self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2) - self.canvas.data["ReactTime"] <= 60:
					self.canvas.coords(self.rect2, 410, 10, 430, 110)
				else:
					self.canvas.move(self.rect2, 0, -self.canvas.data["ReactTime"])
			elif ((self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2) - ((self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2) < -self.canvas.data["ReactTime"]:
				self.canvas.move(self.rect2, 0, -self.canvas.data["ReactTime"])
			else:
				self.canvas.move(self.rect2, 0, (((self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2) - ((self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2)))
					
		elif (self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2 > (self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2:
			if ((self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2) >= 250:	
				if ((self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2) + self.canvas.data["ReactTime"] >= 250:
					self.canvas.coords(self.rect2, 410, 200, 430, 300)
				else:
					self.canvas.move(self.rect2, 0, self.canvas.data["ReactTime"])	
			elif ((self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2) - ((self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2) > self.canvas.data["ReactTime"]:
				self.canvas.move(self.rect2, 0, self.canvas.data["ReactTime"])	
			else:
				self.canvas.move(self.rect2, 0, (((self.canvas.coords(self.ball)[1] + self.canvas.coords(self.ball)[3]) / 2) - ((self.canvas.coords(self.rect2)[1] + self.canvas.coords(self.rect2)[3]) / 2)))	
	
	def win_lose(self):
		if self.canvas.coords(self.ball)[0] < 0 and self.canvas.data["Dir"]['x'] < 0:
			self.canvas.data["play"] = False
			print("Player lose")
			
		elif self.canvas.coords(self.ball)[2] > 450 and self.canvas.data["Dir"]['x'] > 0:
			self.canvas.data["play"] = False
			print("Player win")	
	
	def moveit(self):
		self.ai()
		self.win_lose()	

		self.canvas.data["coordRange"] = []
		for i in range(1, self.canvas.data["Speed"]+1):
			self.canvas.data["coordRange"].append([	self.canvas.coords(self.ball)[0] + (self.canvas.data["Dir"]['x'] * i), 
													self.canvas.coords(self.ball)[1] + (self.canvas.data["Dir"]['y'] * i), 
													self.canvas.coords(self.ball)[2] + (self.canvas.data["Dir"]['x'] * i), 
													self.canvas.coords(self.ball)[3] + (self.canvas.data["Dir"]['y'] * i)   ])
		
		for i in self.canvas.data["coordRange"]:
			if i[0] > 40 and i[1] > 10 and i[2] < 410 and i[3] < 300:
				continue
			elif box( self.canvas.coords(self.rect1)[0], self.canvas.coords(self.rect1)[1],self.canvas.coords(self.rect1)[2],self.canvas.coords(self.rect1)[3] ).intersects(Point( self.canvas.coords(self.ball)[0] + 10, self.canvas.coords(self.ball)[1] + 10 ).buffer(10)) and self.canvas.data["Dir"]['x'] < 0:
				if self.canvas.coords(self.rect1)[1] <  i[3] and self.canvas.coords(self.rect1)[3] > i[1]:
			
					if self.canvas.data["Dir"]['y'] > 0:
						self.angle = random.uniform(math.pi/2, math.pi - 0.5)
					else:
						self.angle = random.uniform(0.5, math.pi/2)
					
					self.canvas.data["Dir"] = {'x': math.sin(self.angle), 'y': -math.cos(self.angle)}
	
					self.canvas.data["Speed"] += 1
					self.canvas.data["xTurn"] = True
					break
			elif box( self.canvas.coords(self.rect2)[0], self.canvas.coords(self.rect2)[1],self.canvas.coords(self.rect2)[2],self.canvas.coords(self.rect2)[3] ).intersects(Point( self.canvas.coords(self.ball)[0] + 10, self.canvas.coords(self.ball)[1] + 10 ).buffer(10)) and self.canvas.data["Dir"]['x'] > 0:
				if self.canvas.coords(self.rect2)[1] <  i[3] and self.canvas.coords(self.rect2)[3] > i[1]:
					
					if self.canvas.data["Dir"]['y'] > 0:
						self.angle = random.uniform(math.pi + 0.5, math.pi * 1.5)
					else:
						self.angle = random.uniform(math.pi * 1.5, math.pi * 2 - 0.5)
					
					self.canvas.data["Dir"] = {'x': math.sin(self.angle), 'y': -math.cos(self.angle)}
					
					self.canvas.data["Speed"] += 1
					self.canvas.data["xTurn"] = True
					break

			elif i[1] < 10 and self.canvas.data["Dir"]['y'] < 0:
				self.canvas.data["Dir"]['y'] *= -1
				self.canvas.data["yTurn"] = True
				break
			elif i[3] > 300 and self.canvas.data["Dir"]['y'] > 0:
				self.canvas.data["Dir"]['y'] *= -1
				self.canvas.data["yTurn"] = True
				break
		self.canvas.move(self.ball, self.canvas.data["Dir"]['x'] * self.canvas.data["Speed"], self.canvas.data["Dir"]['y'] * self.canvas.data["Speed"])
		
		if self.canvas.data["play"]:
			self.root.after(FRAME_RATE, self.moveit)
		else:
			self.canvas.delete(self.ball)
			self.canvas.data["play"] = None
			
		
	def mouseMoved(self, event):
		if self.canvas.data["play"]:
			if event.y <= 60:
				self.canvas.coords(self.rect1, 20, 10, 40, 110)
			elif event.y >= 250:
				self.canvas.coords(self.rect1, 20, 200, 40, 300)
			else:
				self.canvas.coords(self.rect1, 20, event.y-50, 40, event.y+50)
	
	def create_menu(self):
		self.radioArray = []
		self.var = IntVar()
		
		self.button1 = Button(self.canvas, text = "New game", anchor = W, command = self.new_game)
		self.button1.place(x=460,y=25)
		self.button2 = Button(self.canvas, text = "Quit", anchor = W, command = self.quit)
		self.button2.place(x=530,y=25)
		self.label = Label(self.canvas, text="Difficulty:")
		self.label.place(x=460,y=60)
		
		for i in range(1,11):
			self.radioArray.append(Radiobutton(self.canvas, text=i, variable=self.var, value=i))
		for i in range(10):	
			self.radioArray[i].place(x=460,y=80 + i*20)
		self.radioArray[0].select()
		
	def __init__(self, root):
		self.root = root
		self.canvas = Canvas(root, width=565, height=310)

		self.canvas.pack()
		self.canvas.bind("<Motion>", self.mouseMoved)
		self.canvas.data = { }
		self.canvas.data["play"] = None
		
		self.create_menu()
		
		self.rect1 = self.canvas.create_rectangle(20, 100, 40, 200, outline='black', fill="black")
		self.rect2 = self.canvas.create_rectangle(410, 100, 430, 200, outline='black', fill="black")
		
if __name__ == "__main__":
	root = Tk()
	root.title("Pong Tk")
	root.resizable(0,0)
	game = game_controller(root);
	root.mainloop()
