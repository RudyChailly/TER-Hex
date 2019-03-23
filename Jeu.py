import json

from tkinter import*
from tkinter.messagebox import *
from tkinter.filedialog import *

import time

from Grille import *

from Constante import *

from Sommet import *

from Graphe import *

class Jeu:
    def __init__(self):
        
        self.taille = None
        self.joueurs = {} #Stocke la configuration (IA ou joueur) de chacun des joueurs

        self.menu()

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
        Graphe(LIBRE,B_HAUT_BLEU|B_GAUCHE_ROUGE).ajoutSommet(self.matriceSommets[0][0])
        Graphe(LIBRE,B_HAUT_BLEU|B_DROIT_ROUGE).ajoutSommet(self.matriceSommets[0][self.taille-1])
        Graphe(LIBRE,B_BAS_BLEU|B_GAUCHE_ROUGE).ajoutSommet(self.matriceSommets[self.taille-1][0])
        Graphe(LIBRE,B_BAS_BLEU|B_DROIT_ROUGE).ajoutSommet(self.matriceSommets[self.taille-1][self.taille-1])
        
        for i in range(self.taille):
            if i == 0:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_HAUT_BLEU).ajoutSommet(self.matriceSommets[i][j])
            elif i == self.taille-1:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_BAS_BLEU).ajoutSommet(self.matriceSommets[i][j])
            else:
                Graphe(LIBRE,B_GAUCHE_ROUGE).ajoutSommet(self.matriceSommets[i][0])
                Graphe(LIBRE,B_DROIT_ROUGE).ajoutSommet(self.matriceSommets[i][self.taille-1])
        
        #on va ajouter tous les voisins de tous les sommets
        for x in range(self.taille):
            for y in range(self.taille):
                if x != 0:
                    self.matriceSommets[x][y].ajoutVoisin(self.matriceSommets[x-1][y])
                if y != 0:
                    self.matriceSommets[x][y].ajoutVoisin(self.matriceSommets[x][y-1])
                    if x != self.taille-1:
                        self.matriceSommets[x][y].ajoutVoisin(self.matriceSommets[x+1][y-1])
                if x != self.taille-1:
                    self.matriceSommets[x][y].ajoutVoisin(self.matriceSommets[x+1][y])
                if y != self.taille-1:
                    if x != 0:
                        self.matriceSommets[x][y].ajoutVoisin(self.matriceSommets[x-1][y+1])
                    self.matriceSommets[x][y].ajoutVoisin(self.matriceSommets[x][y+1])
        
        self.grille = Grille(Point(10,30),self.taille,40,self.matriceSommets)
        self.tourActuel = ROUGE
        self.canvas = 0;
        self.fenetre = 0;
        self.commencer()

    # afficher le menu de configuration de la partie
    def menu(self):
        fenetreMenu = Tk(className='configuration')
        fenetreMenu.resizable(width=False, height=False)
        fenetreMenu.geometry('320x200+700+300')

        FrameTaille = Frame(fenetreMenu,pady=10,padx=10)
        texteTaille = Label(FrameTaille, text="Taille : ", font="Arial 15")
        texteTaille.pack(side='left')
        taille = Spinbox(FrameTaille,from_=2, to=11,font="Arial 15",width=15)
        taille.pack(side='right')
        FrameTaille.pack()
            
        FrameJoueur = Frame(fenetreMenu,pady=10)
        Frame1 = Frame(FrameJoueur)
        choix1 = [("Joueur","Joueur"),("IA","IA")]

        texteJoueur1 = Label(Frame1,text="Joueur 1 : ",fg=COULEUR_ROUGE, font="Arial 15")
        texteJoueur1.pack(side='left')

        choix1 = [("Joueur",0),("IA",1)]
        var1 = StringVar()
        for text, val in choix1 :
            rb = Radiobutton(Frame1, text=text, variable=var1, value=val, font="Arial 15")
            rb.pack(side='right')
        Frame1.pack()

        Frame2 = Frame(FrameJoueur, pady=10)
        texteJoueur2 = Label(Frame2,text="Joueur 2 : ", fg=COULEUR_BLEU,font="Arial 15")
        texteJoueur2.pack(side='left')

        choix2 = [("Joueur",0),("IA",1)]
        var2 = StringVar()
        for text, val in choix2:
            rb2 = Radiobutton(Frame2, text=text, variable=var2, value=val, font="Arial 15")
            rb2.pack(side='right')
        Frame2.pack()
        FrameJoueur.pack()

        b = Button(fenetreMenu,text="Jouer",command=lambda: self.verifier(fenetreMenu,taille.get(),var1.get(),var2.get()))
        b.pack()

        fenetreMenu.mainloop()

    # verifier que les parametres saisis via le menu sont corrects
    def verifier(self,fenetre,taille,J1,J2):
        # verifier que la taille saisie est un entier
        if (taille.isdigit()):
            if (not (int(taille) >= 2 and int(taille) <= 11)):
                showerror('Taille de grille incorrecte','Veuillez selectionner une taille de grille comprise entre 2 et 11.')
                return False
        else:
            showerror('Taille de grille incorrecte','Veuillez selectionner une taille de grille comprise entre 2 et 11.')
            return False
        if (J1 != '0' and J1 != '1'):
            showerror('Joueur 1 non selectionné','Veuillez selectionner entre IA et Joueur.')
            return False
        if (J2 != '0' and J2 != '1'):
            showerror('Joueur 2 non selectionné','Veuillez selectionner entre IA et Joueur.')
            return False
        self.taille = int(taille)
        self.joueurs[ROUGE] = int(J1)
        self.joueurs[BLEU] = int(J2) 
        fenetre.destroy()

    # commencer une partie
    def commencer(self):

        self.fenetre = Tk(className="Jeu de Hex")
        self.fenetre.resizable(width=False, height=False)
        self.canvas = Canvas(self.fenetre, width=self.grille.taille*100, height=self.grille.taille*67 + 30, background='#ddd')

        self.grille.tracer(self.canvas)
        self.canvas.bind("<Button-1>",self.jouer)    
        self.canvas.pack()
        self.fenetre.after(1000,self.jouerIA)
        self.fenetre.mainloop()
        
    # retourner le code correspondant au plateau actuel
    def code(self):
        code = list()
        for x in range(len(self.matriceSommets)):
            for y in range(len(self.matriceSommets[x])):
                code.append(self.matriceSommets[x][y].couleur)
        code = ''.join(map(str,code))
        return code

    def jouer(self,event):
        if (self.joueurs[self.tourActuel] == 0):
            p = Point(event.x,event.y)
            hexagone = self.grille.trouver(p)
            if((hexagone is not None) and (hexagone.choixHex == False)) :
                hexagone.sommet.jouer(self.tourActuel)
                self.grille.placer(self.tourActuel,hexagone,self.canvas)

                if (self.tourActuel == ROUGE):
                    self.tourActuel = BLEU
                else:
                    self.tourActuel = ROUGE

                hexagone.choixHex = True

                if (self.joueurs[self.tourActuel] == 1): #Si le prochain tour est un IA, le lancer
                    self.fenetre.after(1000,self.jouerIA)

    def jouerIA(self):
        if (self.joueurs[self.tourActuel] == 1):
            s = self.plateaux[self.code()]["s"]
            if (s is not None):
                s = int(s)
                hexagone = self.grille.matriceHexagones[s//self.taille][s%self.taille]
                hexagone.sommet.jouer(self.tourActuel)
                self.grille.placer(self.tourActuel,hexagone,self.canvas)

                if (self.tourActuel == ROUGE):
                    self.tourActuel = BLEU
                else:
                    self.tourActuel = ROUGE

                hexagone.choixHex = True

                if (self.joueurs[self.tourActuel] == 1): #Si le prochain tour est un IA, le lancer
                    self.fenetre.after(1000,self.jouerIA)

                return s

Jeu()