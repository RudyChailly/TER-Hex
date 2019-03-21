import json

from tkinter import*

from Grille import *

from Constante import *

from Sommet import *

from Graphe import *

class Jeu:
    def __init__(self):
        n = 0
        while (n < 2 or n > 11):
            n = int(input("Entrer la dimension de la grille (entre 3 et 11) : "))
            
        self.taille = n
        
        self.plateaux = {}
        with open("./plateaux/P"+str(self.taille)+".txt") as json_file:
            self.plateaux =  json.load(json_file)

        #matrice de sommets utilisée dans les graphes et taille n*n
        self.matriceSommets = []
        
        for i in range(self.taille):
            self.matriceSommets.append([])
            
        #on ajoute nos sommets
        for i in range(self.taille):
            for j in range(self.taille):
                self.matriceSommets[i].append(Sommet(i,j))
                
        #ici on ajoute pour tous les sommets qui touchent un bord dans un graphe avec son bord
        Graphe(LIBRE,B_HAUT_BLEU|B_GAUCHE_ROUGE).ajouter(self.matriceSommets[0][0])
        Graphe(LIBRE,B_HAUT_BLEU|B_DROIT_ROUGE).ajouter(self.matriceSommets[0][self.taille-1])
        Graphe(LIBRE,B_BAS_BLEU|B_GAUCHE_ROUGE).ajouter(self.matriceSommets[self.taille-1][0])
        Graphe(LIBRE,B_BAS_BLEU|B_DROIT_ROUGE).ajouter(self.matriceSommets[self.taille-1][self.taille-1])
        
        for i in range(self.taille):
            if i == 0:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_HAUT_BLEU).ajouter(self.matriceSommets[i][j])
            elif i == self.taille-1:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_BAS_BLEU).ajouter(self.matriceSommets[i][j])
            else:
                Graphe(LIBRE,B_GAUCHE_ROUGE).ajouter(self.matriceSommets[i][0])
                Graphe(LIBRE,B_DROIT_ROUGE).ajouter(self.matriceSommets[i][self.taille-1])
        
        #on va ajouter tous les voisins de tous les sommets
        for x in range(self.taille):
            for y in range(self.taille):
                if x != 0:
                    self.matriceSommets[x][y].ajVoisin(self.matriceSommets[x-1][y])
                if y != 0:
                    self.matriceSommets[x][y].ajVoisin(self.matriceSommets[x][y-1])
                    if x != self.taille-1:
                        self.matriceSommets[x][y].ajVoisin(self.matriceSommets[x+1][y-1])
                if x != self.taille-1:
                    self.matriceSommets[x][y].ajVoisin(self.matriceSommets[x+1][y])
                if y != self.taille-1:
                    if x != 0:
                        self.matriceSommets[x][y].ajVoisin(self.matriceSommets[x-1][y+1])
                    self.matriceSommets[x][y].ajVoisin(self.matriceSommets[x][y+1])
        
        self.grille = Grille(Point(10,30),self.taille,40,self.matriceSommets)
        self.tourActuel = ROUGE
        self.canvas = 0;

    def code(self):
        code = list()
        for x in range(len(self.matriceSommets)):
            for y in range(len(self.matriceSommets[x])):
                code.append(self.matriceSommets[x][y].couleur)
        
        code = ''.join(map(str,code))
        return code

    # commencer une partie
    def commencer(self):

        fenetre = Tk(className="Jeu de Hex")
        fenetre.resizable(width=False, height=False)
        self.canvas = Canvas(fenetre, width=self.grille.taille*100, height=self.grille.taille*67 + 30, background='#ddd')

        self.grille.tracer(self.canvas)
        self.canvas.bind("<Button-1>",self.jouer)    
        self.canvas.pack()
        self.jouerIA()
        fenetre.mainloop()
        

    # placer un pion
    def jouer(self,event):
        p = Point(event.x,event.y)
        hexagone = self.grille.trouver(p)
        if((hexagone is not None) and (hexagone.choixHex == False)) :
            # Red = IA
            if (self.tourActuel == ROUGE):
                hexagone.sommet.jouer(ROUGE)
                self.grille.placer(ROUGE,hexagone,self.canvas)
                self.tourActuel = BLEU
            # Blue
            else:
                hexagone.sommet.jouer(BLEU)
                self.grille.placer(BLEU,hexagone,self.canvas)
                self.tourActuel = ROUGE
                self.jouerIA()
            hexagone.choixHex = True

    # placer un pion
    def jouer2(self,hexagone):
        if((hexagone is not None) and (hexagone.choixHex == False)) :
            # Red = IA
            if (self.tourActuel == ROUGE):
                hexagone.sommet.jouer(ROUGE)
                self.grille.placer(ROUGE,hexagone,self.canvas)
                self.tourActuel = BLEU
            # Blue
            else:
                hexagone.sommet.jouer(BLEU)
                self.grille.placer(BLEU,hexagone,self.canvas)
                self.tourActuel = ROUGE
                self.jouerIA()
            hexagone.choixHex = True

    def jouerIA(self):
        for p in self.plateaux[self.code()]["s"]:
            if (self.plateaux[self.plateaux[self.code()]["s"][p]]["g"] == ROUGE):
                self.jouer2(self.grille.matriceHexagones[int(p)//self.taille][int(p)%self.taille])
                return p

Jeu().commencer()