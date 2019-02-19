from Constante import *

from Graphe import *

#un Pion est decrit par ses coordonnes X et Y dans une matrice
class Sommet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.couleur = LIBRE
        self.graphe = None
        self.listeVoisin = []
        
    def addToGraph(self, graph):
        self.graphe = graph
        self.couleur = graph.couleur
        
    def ajVoisin(self, voisin):
        self.listeVoisin.append(voisin)
        
    def jouer(self,couleur):
        if self.graphe == None:
            Graphe(couleur,B_NO).ajouter(self)
        elif self.graphe.couleur == LIBRE:
            self.graphe.couleur = couleur
            self.couleur = couleur
        for i in range(len(self.listeVoisin)):
            if self.listeVoisin[i].couleur == couleur and self.listeVoisin[i].graphe != self.graphe:
                self.listeVoisin[i].graphe.fusion(self.graphe)