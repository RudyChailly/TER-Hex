from tkinter import*

from Grille import *

class Jeu:
        def __init__(self):
                n = 0
                while (n < 3 or n > 11):
                    n = int(input("Entrer la dimension de la grille (entre 3 et 11) : "))
                self.grille = Grille(Point(10,30),n,40)
                self.tourActuel = 0
                self.canvas = 0;

        # commencer une partie
        def commencer(self):
                fenetre = Tk(className="Jeu de Hex")
                fenetre.resizable(width=False, height=False)
                self.canvas = Canvas(fenetre, width=self.grille.taille*100, height=self.grille.taille*67 + 30, background='#ddd')

                self.grille.tracer(self.canvas)
                self.canvas.bind("<Button-1>",self.jouer)    
                self.canvas.pack()

                fenetre.mainloop()

        # placer un pion
        def jouer(self,event):
                p = Point(event.x,event.y)
                hexagone = self.grille.trouver(p)
                if((hexagone is not None) and (hexagone.choixHex == False)) :
                    # Red
                    if (self.tourActuel == 0):
                            self.grille.placer("#dd0000",hexagone,self.canvas)
                            self.tourActuel = 1
                    # Blue
                    else:
                            self.grille.placer("#005dff",hexagone,self.canvas)
                            self.tourActuel = 0
                    hexagone.choixHex = True

Jeu().commencer()