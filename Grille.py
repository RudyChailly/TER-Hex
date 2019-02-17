from tkinter import*

from Hexagone import *

# une Grille est decrite par un ensemble de Hexagone
class Grille:
        # pour initialiser une Grille, nous lui donnons le point de départ p, les dimensions (n x n) et la longueur des cotes des Hexagone
        def __init__(self,p,n,longueur):
                self.taille = n
                self.hexagones = []

                for i in range(self.taille):
                        self.hexagones.append([])

                self.hexagones[0].append(Hexagone(p,longueur))

                for i in range(self.taille):
                        for j in range(1,self.taille):
                                self.hexagones[i].append(Hexagone(self.hexagones[i][j-1].points[4],longueur))
                        if (i < self.taille-1):
                                self.hexagones[i+1].append(Hexagone(self.hexagones[i][0].points[2],longueur))

        # tracer tous les Hexagone qui composent la Grille ainsi que les lignes
        def tracer(self,canvas):
                for i in range(self.taille):
                        for j in range(0,len(self.hexagones[i])):
                                self.hexagones[i][j].tracer(canvas)

                for i in range(self.taille):
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
                for i in range(self.taille):
                        for j in range(self.taille):
                                if (self.hexagones[i][j].centre.distance(p) <= 25):
                                        return self.hexagones[i][j]


        # placer un pion d'une certaine couleur sur l'hexagone passe en parametre
        def placer(self,couleur,hexagone,canvas):
                hexagone.centre.tracerCercle(25,couleur,canvas)