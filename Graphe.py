from Constante import *

# un Graphe possède des sommets d'une même couleur qui sont reliés sur le plateau
class Graphe: 

    gagnant = ""

    # creer un Graphe a partir d'une couleur et de son bord (1: Bleu Haut, 2: Rouge Gauche, 4: Bleu Bas, 8: Rouge Droite)
    def __init__(self,couleur,bord):
        self.sommets = []
        self.couleur = couleur
        self.bord = bord

    # ajouter un Sommet à un Graphe (definit aussi le Graphe du Sommet)
    def ajoutSommet(self,sommet):
        sommet.setGraphe(self)
        self.sommets.append(sommet)
        
    # recuperer tous les Sommet d'un autre Graphe
    def fusion(self,graphe):
        # si les 2 grpahes ne sont pas de la meme couleur, ils ne peuvent pas fusionner
        if graphe.couleur != self.couleur:
            return 0
            
        self.bord = self.bord | graphe.bord

        while(len(graphe.sommets) != 0):
            self.ajoutSommet(graphe.sommets.pop())

        # si la fusion des 2 graphes relie les 2 bords d'une couleur
        if self.couleur == BLEU:
            if (self.bord & (B_HAUT_BLEU | B_BAS_BLEU)) == B_HAUT_BLEU + B_BAS_BLEU:
                Graphe.gagnant = "BLEU"
        elif self.couleur == ROUGE:
            if (self.bord & (B_GAUCHE_ROUGE | B_DROIT_ROUGE)) == B_GAUCHE_ROUGE + B_DROIT_ROUGE:
                Graphe.gagnant = "ROUGE"

