#!/usr/bin/env python

__author__ = "Saulius Bartkus"
__copyright__ = "Copyright 2017"

__license__ = "GPL"
__version__ = "1.0.2"
__maintainer__ = "Saulius Bartkus"
__email__ = "saulius181@yahoo.com"
__status__ = "Production"

from tkinter import *
import random
import time
import math
from shapely.geometry import Polygon, Point, box
import winsound

FRAME_RATE = 10 # 100 frames per second 
#HEIGHT = 310
#WIDTH = 565

class game_controller(object):
	def set_score(self, var):
		if var == "ai":
			self.canvas.data["AiScore"] += 1
			self.canvas.itemconfig(self.aiScore, text=self.canvas.data["AiScore"])
			winsound.PlaySound("ping_pong_8bit_peeeeeep.wav", winsound.SND_ALIAS|winsound.SND_ASYNC)
			if self.canvas.data["AiScore"] >= self.currentScoreVar:
				print("Player lose")
			else:
				self.set_ball()
				self.set_ball_dir()
				self.set_diff()
				self.canvas.data["play"] = True
				self.roundWin = None
				self.root.after(2000, self.moveit)		
				
		elif var == "player":
			self.canvas.data["PlayerScore"] += 1
			self.canvas.itemconfig(self.playerScore, text=self.canvas.data["PlayerScore"])
			winsound.PlaySound("ping_pong_8bit_peeeeeep.wav", winsound.SND_ALIAS|winsound.SND_ASYNC)
			if self.canvas.data["PlayerScore"] >= self.currentScoreVar:
				print("Player win")
			else:
				self.set_ball()
				self.set_ball_dir()
				self.set_diff()
				self.canvas.data["play"] = True
				self.roundWin = None
				
				self.root.after(2000, self.moveit)	
		elif self.roundWin == None:
			pass
				
	def set_ball(self):
		rand_pos = random.randint(50,250)
		self.ball = self.canvas.create_oval(235, rand_pos, 255, rand_pos+20, outline='white', fill="white")		
	
	def set_diff(self):
		if self.currentBallSpeedVar == "Random":
			self.canvas.data["Speed"] = random.choice(range(3,10))
		elif self.currentBallSpeedVar == "Slow":
			self.canvas.data["Speed"] = 3
		elif self.currentBallSpeedVar == "Medium":
			self.canvas.data["Speed"] = 5
		elif self.currentBallSpeedVar == "Fast":
			self.canvas.data["Speed"] = 9	
	
	def set_ball_dir(self):
		if self.currentBallDirVar == "Random":
			self.canvas.data["Dir"] = {'x': math.sin(self.angle) * random.choice([-1, 1]), 'y': math.cos(self.angle) * random.choice([-1, 1])}
		elif self.currentBallDirVar == "Left":
			self.canvas.data["Dir"] = {'x': math.sin(self.angle) * -1, 'y': math.cos(self.angle) * random.choice([-1, 1])}
		elif self.currentBallDirVar == "Right":
			self.canvas.data["Dir"] = {'x': math.sin(self.angle), 'y': math.cos(self.angle) * random.choice([-1, 1])}		
	
	def new_game(self):
		if self.canvas.data["play"] is None:
	
			self.set_ball()
			self.roundWin = None
			
			self.canvas.data["PlayerScore"] = 0
			self.canvas.data["AiScore"] = 0
			
			self.currentScoreVar = self.scoreVar.get()
			
			self.canvas.itemconfig(self.playerScore, text=self.canvas.data["PlayerScore"])
			self.canvas.itemconfig(self.aiScore, text=self.canvas.data["AiScore"])
			
			difficultyVar = self.difficultyVar.get()
			if difficultyVar == "Random":
				self.canvas.data["ReactTime"] = random.choice(range(3,10))
			elif difficultyVar == "Slow":
				self.canvas.data["ReactTime"] = 3
			elif difficultyVar == "Medium":
				self.canvas.data["ReactTime"] = 5
			elif difficultyVar == "Fast":
				self.canvas.data["ReactTime"] = 9

			self.currentBallSpeedVar = self.ballSpeedVar.get()
			self.set_diff()

			self.angle = random.uniform(0.5, math.pi - 0.5)
			self.currentBallDirVar = self.ballDirVar.get()
			
			self.set_ball_dir()
				
			self.canvas.data["play"] = True
			self.root.after(2000, self.moveit)

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
			self.roundWin = "ai"
			
		elif self.canvas.coords(self.ball)[2] > 450 and self.canvas.data["Dir"]['x'] > 0:
			self.canvas.data["play"] = False
			self.roundWin = "player"
	
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
					
#					if i[0] < 30:
#						self.angle += math.pi
					
					self.canvas.data["Dir"] = {'x': math.sin(self.angle), 'y': -math.cos(self.angle)}
	
					self.canvas.data["Speed"] += 1
					
					winsound.PlaySound("ping_pong_8bit_beeep.wav", winsound.SND_ALIAS|winsound.SND_ASYNC)
					break
			elif box( self.canvas.coords(self.rect2)[0], self.canvas.coords(self.rect2)[1],self.canvas.coords(self.rect2)[2],self.canvas.coords(self.rect2)[3] ).intersects(Point( self.canvas.coords(self.ball)[0] + 10, self.canvas.coords(self.ball)[1] + 10 ).buffer(10)) and self.canvas.data["Dir"]['x'] > 0:
				if self.canvas.coords(self.rect2)[1] <  i[3] and self.canvas.coords(self.rect2)[3] > i[1]:
					
					if self.canvas.data["Dir"]['y'] > 0:
						self.angle = random.uniform(math.pi + 0.5, math.pi * 1.5)
					else:
						self.angle = random.uniform(math.pi * 1.5, math.pi * 2 - 0.5)
					
#					if i[2] > 420:
#						self.angle += math.pi
					
					self.canvas.data["Dir"] = {'x': math.sin(self.angle), 'y': -math.cos(self.angle)}
					
					self.canvas.data["Speed"] += 1
					
					winsound.PlaySound("ping_pong_8bit_beeep.wav", winsound.SND_ALIAS|winsound.SND_ASYNC)
					break

			elif i[1] < 10 and self.canvas.data["Dir"]['y'] < 0:
				self.canvas.data["Dir"]['y'] *= -1
				winsound.PlaySound("ping_pong_8bit_plop.wav", winsound.SND_ALIAS|winsound.SND_ASYNC)
				break
			elif i[3] > 300 and self.canvas.data["Dir"]['y'] > 0:
				self.canvas.data["Dir"]['y'] *= -1
				winsound.PlaySound("ping_pong_8bit_plop.wav", winsound.SND_ALIAS|winsound.SND_ASYNC)
				break
		self.canvas.move(self.ball, self.canvas.data["Dir"]['x'] * self.canvas.data["Speed"], self.canvas.data["Dir"]['y'] * self.canvas.data["Speed"])
		
		if self.canvas.data["play"]:
			self.root.after(FRAME_RATE, self.moveit)
		else:
			self.canvas.delete(self.ball)
			self.canvas.data["play"] = None
			self.set_score(self.roundWin)
			
	def mouseMoved(self, event):
		if self.canvas.data["play"]:
			if event.y <= 60:
				self.canvas.coords(self.rect1, 20, 10, 40, 110)
			elif event.y >= 250:
				self.canvas.coords(self.rect1, 20, 200, 40, 300)
			else:
				self.canvas.coords(self.rect1, 20, event.y-50, 40, event.y+50)
	
	def create_menu(self):
		self.difficultyVar = StringVar()
		self.difficultyVar.set("Slow")		
		
		self.scoreVar = IntVar() 
		self.scoreVar.set(10)
		
		self.ballSpeedVar = StringVar()
		self.ballSpeedVar.set("Slow")

		self.ballDirVar = StringVar()
		self.ballDirVar.set("Random")
		
		self.button1 = Button(self.canvas, text = "New game", anchor = W, command = self.new_game)
		self.button1.place(x=460,y=25)
		self.button2 = Button(self.canvas, text = "Quit", anchor = W, command = self.quit)
		self.button2.place(x=530,y=25)

		self.difficultyLabel = Label(self.canvas, text="AI reaction:")
		self.difficultyLabel.place(x=460,y=60)
		self.difficultyOption = OptionMenu(self.canvas, self.difficultyVar, "Random", "Slow", "Medium", "Fast")
		self.difficultyOption.place(x=460,y=80)

		self.scoreLabel = Label(self.canvas, text="Winning score:")
		self.scoreLabel.place(x=460,y=120)
		self.scoreOption = OptionMenu(self.canvas, self.scoreVar, 5,10,15,20,25,30,35,40)
		self.scoreOption.place(x=460,y=140)		
		
		self.ballSpeedLabel = Label(self.canvas, text="Init ball speed:")
		self.ballSpeedLabel.place(x=460,y=180)
		self.ballSpeedOption = OptionMenu(self.canvas, self.ballSpeedVar, "Random", "Slow", "Medium", "Fast")
		self.ballSpeedOption.place(x=460,y=200)			

		self.ballDirLabel = Label(self.canvas, text="Init ball dir:")
		self.ballDirLabel.place(x=460,y=240)
		self.ballDirOption = OptionMenu(self.canvas, self.ballDirVar, "Random", "Left", "Right")
		self.ballDirOption.place(x=460,y=260)		
		
	def __init__(self, root):
		self.root = root
		self.canvas = Canvas(root, width=565, height=310, bg="black")

		self.canvas.pack()
		self.canvas.bind("<Motion>", self.mouseMoved)
		self.canvas.data = { }
		self.canvas.data["play"] = None
		
		
		self.midLine = self.canvas.create_line(245, 0, 245, 310, fill="white", dash=(200, 255), width=2)
		
		self.playerScore = self.canvas.create_text(140, 100, text="0", font=("Lucida Console", 120), fill="white")
		self.aiScore = self.canvas.create_text(340, 100, text="0", font=("Lucida Console", 120), fill="white")
		
		self.create_menu()
		
		self.rect1 = self.canvas.create_rectangle(20, 100, 40, 200, outline='white', fill="white")
		self.rect2 = self.canvas.create_rectangle(410, 100, 430, 200, outline='white', fill="white")
		
if __name__ == "__main__":
	root = Tk()
	root.title("Pong Tk")
	root.resizable(0,0)
	game = game_controller(root);
	root.mainloop()
