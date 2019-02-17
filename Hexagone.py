from tkinter import*

from Point import *

# un Hexagone est decrit par les coordonnes de ses 6 points et son centre
class Hexagone:
        # creer un Hexagone a partir d'un seul point et de la longueur des cotes
        def __init__(self,p,longueur):
                
                """
                  ___5___
                 /       \
                0        4
                |        |
                1        3
                \___2___/
                """
                
                points = [p]
                points.append(Point(points[0].x,points[0].y+longueur)) # |
                points.append(Point(points[1].x+longueur*cos(120), points[1].y+longueur*sin(120)))
                points.append(Point(points[2].x+longueur*cos(120), points[2].y-longueur*sin(120)))
                points.append(Point(points[3].x, points[3].y-longueur)) # | 
                points.append(Point(points[4].x-longueur*cos(120), points[4].y-longueur*sin(120)))
                
                self.choixHex = False
                self.points = points;
                self.centre = Point((points[0].x+points[3].x)/2,(points[0].y+points[3].y)/2)

        # tracer l'Hexagone sur le canvas
        def tracer(self,canvas):
                self.trace = self.points[0].tracerHexagone(self.points[1],self.points[2],self.points[3],self.points[4],self.points[5],canvas)
                self.centre.tracerCercle(25,'',canvas,'#ddd')