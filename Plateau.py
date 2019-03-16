from math import *;

import os

LIBRE = 0
ROUGE = 1
BLEU = 2

# Recuperer le fichier et, s'il n'existe pas, le creer
def genFile(n):
	path = "./plateaux"
	filename = "P"+str(n)+".txt";
	if not os.path.exists(path):
		os.makedirs(path);
	fd = open(os.path.join(path, filename), "w");
	return fd;

def voisins(n):
	# voisins[n*n] : Bord Bleu Haut
	# voisins[n*n+1] : Bord Bleu Bas
	# voisins[n*n+2] : Bord Rouge Gauche
	# voisins[n*n+3] : Bord Rouge Droite
	voisins = []
	for i in range(n*n+4):
		voisins.append([])

	for i in range(n):
		voisins[n*n].append(i) #Bord Bleu Haut 
		voisins[i].append(n*n)

		voisins[n*n+1].append(n*n-1-i) #Bord Bleu Bas
		voisins[n*n-1-i].append(n*n+1)

		voisins[n*n+2].append(i*n) #Bord Rouge Gauche
		voisins[i*n].append(n*n+2)

		voisins[n*n+3].append((n*n-1)-(i*n)) #Bord Rouge Droite
		voisins[(n*n-1)-(i*n)].append(n*n+3)

		for j in range(n):
			if (i-1 >= 0) and (j+1 < n):
				voisins[i*n+j].append((i-1)*n+j)
				voisins[i*n+j].append(i*n+(j+1))
				voisins[i*n+j].append((i-1)*n+(j+1))
			elif(i-1 >= 0):
				voisins[i*n+j].append((i-1)*n+j)
			elif(j+1 < n):
				voisins[i*n+j].append(i*n+(j+1))

			if (i+1 < n) and (j-1 >= 0):
				voisins[i*n+j].append((i+1)*n+j)
				voisins[i*n+j].append(i*n+(j-1))
				voisins[i*n+j].append((i+1)*n+(j-1))
			elif(i+1 < n):
				voisins[i*n+j].append((i+1)*n+j)
			elif(j-1 >= 0):
				voisins[i*n+j].append(i*n+(j-1))

	return voisins

class Plateau():
	
	def __init__(self,code,tour):
		self.code = code
		self.tour = tour
		self.gagnant = self.victoire()
		self.transitions = {}
		if (self.gagnant == 0): #Si le plateau n'est pas déjà gagnant
			self.calculTransitions()

	def __str__(self):
		return self.code+" "+str(self.gagnant)+" "+str(self.transitions)+"\n"

	def calculTransitions(self):
		global plateaux
		for i in range(len(self.code)):
			if (self.code[i] == '0'):
				codeP = list(self.code) #Transforme le code du plateau en une liste de caractères
				codeP[i] = str(self.tour) #Change un caractere de ce code, correspond au pion joue
				codeP = "".join(codeP) #Re-transforme le nouveau code obtenu en chaine de caractere
				self.transitions[i+1] = codeP #Ajoute le plateau à la liste de transitions
				if (not(codeP in plateaux)):
					plateaux[codeP] = Plateau(codeP,(self.tour%2)+1)

	# Parcours en profondeur d'un bord à l'autre
	def victoire(self):
		global voisins
		n = int(sqrt(len(self.code)))
		
		AT = []
		dejaVus = []
		for i in range(n*n+4):
			dejaVus.append(0)

		#Si Bleu : on ajoute le Bord Bleu Haut (n*n)
		#Sinon : on ajoute le Bord Rouge Gauche (n*n+2)
		bord = n*n+((self.tour-1)*2)
		AT.append(bord)
		dejaVus[bord] = 1
		while(len(AT) != 0):
			x = AT[-1]
			nbVoisins = 0
			for i in (voisins[x]):
				if (i < n*n):
					if (self.code[i] == str(self.tour%2+1) and dejaVus[i] == 0):
						y = i
						nbVoisins += 1
				else:
					if (i == bord+1):
						self.gagnant = self.tour%2+1
						return self.tour%2+1
					
			if (nbVoisins == 0):
				AT.pop()
			else:
				dejaVus[y] = 1
				AT.append(y)
		return 0

	def ecrireFichier(self,fd):
		fd.write(self.__str__())

N = int(input("Taille de la grille:"))
voisins = voisins(N) #On calcule la liste des voisins (sommets adjacents, qu'importe la couleur) de chacun des sommets

format = "%0"+str(N*N)+"d" #Permet de forcer l'affichage d'un nombre en (N*N) chiffres

#On crée la liste globale des plateaux qu'on initialise avec le plateau vide.
plateaux = {}
plateaux[format % 0] = Plateau(format % 0,ROUGE) 

fd = genFile(N)

for i in plateaux:
	plateaux[i].ecrireFichier(fd)