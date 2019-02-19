from Constante import *
# un Graphe possède des sommets d'une même couleur qui sont reliés sur le plateau
class Graphe:
    # pour initialiser le graphe il faut sa couleur, son "bord" 1 bleu haut,2 rouge gauche, 4 bleu bas et 8 rouge droite (pour permettre des opérations bit à bit)
    def __init__(self,couleur,bord):
        self.sommets = []
        self.couleur = couleur
        self.bord = bord

    # ajoute un sommet au graphe
    def ajouter(self,sommet):
        sommet.addToGraph(self)
        self.sommets.append(sommet)
        
    # récupère tous les sommets d'un autre graphe
    def fusion(self,graphe):
        if graphe.couleur != self.couleur:
            return 0
        self.bord = self.bord | graphe.bord
        
        while(len(graphe.sommets) != 0):
            self.ajouter(graphe.sommets.pop())
        
        if self.couleur == BLEU:
            if (self.bord & (B_HAUT_BLEU | B_BAS_BLEU)) == B_HAUT_BLEU + B_BAS_BLEU:
                print("Le joueur bleu a gagné!");
        elif self.couleur == ROUGE:
            if (self.bord & (B_GAUCHE_ROUGE | B_DROIT_ROUGE)) == B_GAUCHE_ROUGE + B_DROIT_ROUGE:
                print("Le joueur rouge a gagné!");
            