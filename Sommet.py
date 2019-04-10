from Graphe import *

#un Sommet est decrit par ses coordonnes i et j dans une matrice
class Sommet:
    def __init__(self):
        self.couleur = LIBRE
        self.graphe = None
        self.listeVoisin = []
        
    # associer un Graphe a un Sommet  
    def setGraphe(self, graphe):
        self.graphe = graphe
        self.couleur = graphe.couleur
        
    # ajouter un Sommet a la liste de voisins  
    def ajoutVoisin(self, voisin):
        self.listeVoisin.append(voisin)
        
    # changer la couleur d'un Sommet et le fusioner avec les graphes voisins
    def jouer(self,couleur):
        if self.graphe == None:
            Graphe(couleur,B_NO).ajoutSommet(self)
        elif self.graphe.couleur == LIBRE:
            self.graphe.couleur = couleur
            self.couleur = couleur
        for i in range(len(self.listeVoisin)):
            if self.listeVoisin[i].couleur == couleur and self.listeVoisin[i].graphe != self.graphe:
                self.listeVoisin[i].graphe.fusion(self.graphe)