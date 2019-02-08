from tkinter import*
from math import*

#un Point est decrit par ses coordonnes X et Y
class Point:
	def __init__(self,x,y):
		self.x = x;
		self.y = y;

# un Hexagone est decrit par les coordonnes de ses 6 points
class Hexagone:
	# creer un Hexagone a partir d'un seul point et de la longueur des cotes
	def __init__(self,p,longueur):
		
		"""
		  ___5___
		 /       \
		0	     4
		|	     |
		1	     3
		\___2___/
		"""
		points = [p]
		points.append(Point(points[0].x,points[0].y+longueur)) # |
		points.append(Point(points[1].x+longueur*cos(120), points[1].y+longueur*sin(120))) # \
		points.append(Point(points[2].x+longueur*cos(120), points[2].y-longueur*sin(120))) # /
		points.append(Point(points[3].x, points[3].y-longueur)) # | 
		points.append(Point(points[4].x-longueur*cos(120), points[4].y-longueur*sin(120))) # \
		self.points = points;

	# tracer l'Hexagone sur le canvas
	def tracer(self,canvas):
		canvas.create_polygon(self.points[0].x,self.points[0].y, self.points[1].x,self.points[1].y, self.points[2].x,self.points[2].y,self.points[3].x,self.points[3].y, self.points[4].x,self.points[4].y, self.points[5].x,self.points[5].y,fill= "white", outline='black')


# une Grille est decrite par un ensemble de Hexagone
class Grille:
	# pour initialiser une Grille, nous lui donnons le point de départ p, les dimensions (n x n) et la longueur des cotes des Hexagone
	def __init__(self,p,n,longueur):
		self.hexagones = []
		for i in range(0,n):
			self.hexagones.append([])
		self.hexagones[0].append(Hexagone(p,longueur))
		for i in range(0,n):
			for j in range(1,n):
				self.hexagones[i].append(Hexagone(self.hexagones[i][j-1].points[4],longueur))
			if (i < n-1):
				self.hexagones[i+1].append(Hexagone(self.hexagones[i][0].points[2],longueur))

	# tracer tous les Hexagone qui composent la Grille ainsi que les lignes
	def tracer(self,canvas):
		for i in range(0,len(self.hexagones)):
			for j in range(0,len(self.hexagones[i])):
				self.hexagones[i][j].tracer(canvas)
		for i in range(0,len(self.hexagones)):
			#Blue
			canvas.create_line(self.hexagones[0][i].points[0].x, self.hexagones[0][i].points[0].y, self.hexagones[0][i].points[5].x, self.hexagones[0][i].points[5].y, width=5, fill="blue")
			canvas.create_line(self.hexagones[0][i].points[4].x, self.hexagones[0][i].points[4].y, self.hexagones[0][i].points[5].x, self.hexagones[0][i].points[5].y, width=5, fill="blue")

			canvas.create_line(self.hexagones[-1][i].points[2].x, self.hexagones[-1][i].points[2].y, self.hexagones[-1][i].points[3].x, self.hexagones[-1][i].points[3].y, width=5, fill="blue")
			canvas.create_line(self.hexagones[-1][i].points[1].x, self.hexagones[-1][i].points[1].y, self.hexagones[-1][i].points[2].x, self.hexagones[-1][i].points[2].y, width=5, fill="blue")

			#Red
			canvas.create_line(self.hexagones[i][0].points[0].x, self.hexagones[i][0].points[0].y, self.hexagones[i][0].points[1].x, self.hexagones[i][0].points[1].y, width=5, fill="red")
			canvas.create_line(self.hexagones[i][0].points[1].x, self.hexagones[i][0].points[1].y, self.hexagones[i][0].points[2].x, self.hexagones[i][0].points[2].y, width=5, fill="red")

			canvas.create_line(self.hexagones[i][-1].points[5].x, self.hexagones[i][-1].points[5].y, self.hexagones[i][-1].points[4].x, self.hexagones[i][-1].points[4].y, width=5, fill="red")
			canvas.create_line(self.hexagones[i][-1].points[4].x, self.hexagones[i][-1].points[4].y, self.hexagones[i][-1].points[3].x, self.hexagones[i][-1].points[3].y, width=5, fill="red")

		canvas.create_line((self.hexagones[0][-1].points[4].x + self.hexagones[0][-1].points[5].x)/2, (self.hexagones[0][-1].points[4].y + self.hexagones[0][-1].points[5].y)/2, self.hexagones[0][-1].points[4].x, self.hexagones[0][-1].points[4].y, width=5, fill="red")
		canvas.create_line((self.hexagones[-1][0].points[1].x + self.hexagones[-1][0].points[2].x)/2, (self.hexagones[-1][0].points[1].y + self.hexagones[-1][0].points[2].y)/2, self.hexagones[-1][0].points[2].x, self.hexagones[-1][0].points[2].y, width=5, fill="blue")

class Main:
	def __init__(self):
		fenetre = Tk(className="Jeu de Hex")
		fenetre.resizable(width=False, height=False)

		canvas = Canvas(fenetre, width=1080, height=750, background='#ddd')

		Gr = Grille(Point(10,30),11,40)
		Gr.tracer(canvas)

		canvas.pack()
		fenetre.mainloop()

Main()