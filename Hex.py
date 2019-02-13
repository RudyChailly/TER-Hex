from tkinter import*
from math import*

N = 11

#un Point est decrit par ses coordonnes X et Y
class Point:
	def __init__(self,x,y):
		self.x = x;
		self.y = y;

	def distance(self,p):
		return sqrt(pow((self.x - p.x),2) + pow((self.y - p.y),2))

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

		self.centre = Point((points[0].x+points[3].x)/2,(points[0].y+points[3].y)/2)

	# tracer l'Hexagone sur le canvas
	def tracer(self,canvas):
		self.trace = canvas.create_polygon(self.points[0].x,self.points[0].y, self.points[1].x,self.points[1].y, self.points[2].x,self.points[2].y,self.points[3].x,self.points[3].y, self.points[4].x,self.points[4].y, self.points[5].x,self.points[5].y,fill= "white", outline='black')
		canvas.create_oval(self.centre.x-25,self.centre.y-25,self.centre.x+25,self.centre.y+25,fill='',outline='',activefill='#ddd')

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
			canvas.create_line(self.hexagones[0][i].points[0].x, self.hexagones[0][i].points[0].y, self.hexagones[0][i].points[5].x, self.hexagones[0][i].points[5].y, width=5, fill="#005dff")
			canvas.create_line(self.hexagones[0][i].points[4].x, self.hexagones[0][i].points[4].y, self.hexagones[0][i].points[5].x, self.hexagones[0][i].points[5].y, width=5, fill="#005dff")

			canvas.create_line(self.hexagones[-1][i].points[2].x, self.hexagones[-1][i].points[2].y, self.hexagones[-1][i].points[3].x, self.hexagones[-1][i].points[3].y, width=5, fill="#005dff")
			canvas.create_line(self.hexagones[-1][i].points[1].x, self.hexagones[-1][i].points[1].y, self.hexagones[-1][i].points[2].x, self.hexagones[-1][i].points[2].y, width=5, fill="#005dff")

			#Red
			canvas.create_line(self.hexagones[i][0].points[0].x, self.hexagones[i][0].points[0].y, self.hexagones[i][0].points[1].x, self.hexagones[i][0].points[1].y, width=5, fill="#dd0000")
			canvas.create_line(self.hexagones[i][0].points[1].x, self.hexagones[i][0].points[1].y, self.hexagones[i][0].points[2].x, self.hexagones[i][0].points[2].y, width=5, fill="#dd0000")

			canvas.create_line(self.hexagones[i][-1].points[5].x, self.hexagones[i][-1].points[5].y, self.hexagones[i][-1].points[4].x, self.hexagones[i][-1].points[4].y, width=5, fill="#dd0000")
			canvas.create_line(self.hexagones[i][-1].points[4].x, self.hexagones[i][-1].points[4].y, self.hexagones[i][-1].points[3].x, self.hexagones[i][-1].points[3].y, width=5, fill="#dd0000")

		canvas.create_line((self.hexagones[0][-1].points[4].x + self.hexagones[0][-1].points[5].x)/2, (self.hexagones[0][-1].points[4].y + self.hexagones[0][-1].points[5].y)/2, self.hexagones[0][-1].points[4].x, self.hexagones[0][-1].points[4].y, width=5, fill="#dd0000")
		canvas.create_line((self.hexagones[-1][0].points[1].x + self.hexagones[-1][0].points[2].x)/2, (self.hexagones[-1][0].points[1].y + self.hexagones[-1][0].points[2].y)/2, self.hexagones[-1][0].points[2].x, self.hexagones[-1][0].points[2].y, width=5, fill="#005dff")

	# trouver l'hexagone correspondant à l'aide la distance entre le centre d'un hexagone et la zone cliquee
	def trouver(self,p):
		i, j =0, 0
		distMin = self.hexagones[0][0].centre.distance(p)
		for a in range(N):
			for b in range(N):
				if (self.hexagones[a][b].centre.distance(p) < distMin):
					i,j = a,b
					distMin = self.hexagones[a][b].centre.distance(p)
		return self.hexagones[i][j]

	# placer un pion d'une certaine couleur sur l'hexagone passe en parametre
	def placer(self,couleur,hexagone,canvas):
		p = hexagone.centre
		canvas.create_oval(p.x-25, p.y-25, p.x+25, p.y+25, fill=couleur,outline='')

class Jeu:
	def __init__(self,grille):
		self.grille = grille
		self.tourActuel = 0

	# commencer une partie
	def commencer(self):
		global canvas
		self.grille.tracer(canvas)
		canvas.bind("<Button-1>",self.jouer)	
		canvas.pack()

	# placer un pion
	def jouer(self,event):
		p = Point(event.x,event.y)
		global canvas
		hexagone = self.grille.trouver(p)
		# Red
		if (self.tourActuel == 0):
			self.grille.placer("#dd0000",hexagone,canvas)
			self.tourActuel = 1
		# Blue
		else:
			self.grille.placer("#005dff",hexagone,canvas)
			self.tourActuel = 0

class Main:
	def __init__(self):
		fenetre = Tk(className="Jeu de Hex")
		fenetre.resizable(width=False, height=False)
		global canvas
		canvas = Canvas(fenetre, width=1080, height=750, background='#ddd')

		global jeu
		jeu = Jeu(Grille(Point(10,30),11,40))
		jeu.commencer()

		fenetre.mainloop()


Main()