from math import *;

import os
import json

LIBRE = 0
ROUGE = 1
BLEU = 2

voisins = []
plateaux = {}

# recuperer le fichier "./plateaux/{n}/{coups}.txt" ou, s'il n'existe pas, le creer
def genFichier(n,coups):
	path = "./plateaux/"+str(n)
	filename = str(coups)+".txt";
	if not os.path.exists(path):
		os.makedirs(path);	
	fd = open(os.path.join(path, filename), "w")
	return fd;

# ecrire le contenu dans le fichier fd 
def ecrireFichier(fd,contenu):
	fd.write(json.dumps(contenu))

# initialiser la variable globale voisins en fonction de la dimension n de la grille
def voisin(n):
	# voisins[n*n] : Bord Bleu Haut
	# voisins[n*n+1] : Bord Bleu Bas
	# voisins[n*n+2] : Bord Rouge Gauche
	# voisins[n*n+3] : Bord Rouge Droite
	global voisins
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

class ArbreCoups():
	
	def __init__(self,code,tour,nbTours):
		global plateaux
		plateaux[code] = self

		self.code = code
		self.tour = tour
		self.nbTours = nbTours
		self.gagnant = self.victoire()
		self.suivants = {}
		# si le Plateau n'est pas déjà gagnant
		if (self.gagnant == 0): 
			self.calculSuivants()
			self.gagnant = self.estGagnant()

	# calculer les Plateau accesibles en un coup depuis le 
	def calculSuivants(self):
		global plateaux
		for i in range(len(self.code)):
			if (self.code[i] == '0'):
				codeSuiv = list(self.code) #Transforme le code du plateau en une liste de caractères
				codeSuiv[i] = str(self.tour) #Change un caractere de ce code, correspond au pion joue
				codeSuiv = "".join(codeSuiv) #Re-transforme le nouveau code obtenu en chaine de caractere
				self.suivants[i] = codeSuiv #Ajoute le plateau à la liste de suivants
				if (not(codeSuiv in plateaux)):
					ArbreCoups(codeSuiv,(self.tour%2)+1,self.nbTours+1)

	# verifier si un joueur a relié les 2 bords d'une même couleur(Parcours en profondeur d'un bord à l'autre)
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

	# determiner pour quel joueur il existe une strategie gagnante sur ce plateau 
	#(le joueur a la possibilité de gagner dans plusieurs coups qu'importe ceux de l'adversaire)
	def estGagnant(self):
		global plateaux
		result = (self.tour == BLEU)
		if (self.tour == BLEU):
			for s in self.suivants:
				result = (result and (plateaux[self.suivants[s]].gagnant == ROUGE)) 
		else :
			for s in self.suivants:
				result = (result or (plateaux[self.suivants[s]].gagnant == ROUGE))
		if (result):
			return ROUGE
		else:
			return BLEU

	# retourner un coup qui permet au joueur d'etre dans une strategie gagnante
	def coupGagnant(self):
		global plateaux
		for s in self.suivants:
			if plateaux[self.suivants[s]].gagnant == self.gagnant:
				return s
		return None

	# retourner l'index correspondant au plateau
	def index(self):
		res = 0
		for i in range(len(self.code)):
			res = res + int(self.code[i])*pow(3,i)
		return int(res)

	# generer les fichiers differents json (un pour chaque nombre de coups)
	def json(self,tourCourant,n):
		global plateaux
		dictio = {}
		for i in plateaux:
			if ((len(plateaux[i].suivants) != 0) and (plateaux[i].nbTours == tourCourant)):
				dictio[str(plateaux[i].index())] = plateaux[i].coupGagnant()
		for tourTemp in range(tourCourant, n*n):
			writingTempDictio = {}
			for i in plateaux:
				if ((len(plateaux[i].suivants) != 0) and (plateaux[i].nbTours == tourTemp)):
					writingTempDictio[str(plateaux[i].index())] = plateaux[i].coupGagnant()
			if (not (os.path.isfile("./plateaux/"+str(n)+"/"+str(tourTemp)+".txt"))):
				ecrireFichier(genFichier(n,tourTemp),writingTempDictio)
			else:
				with open("./plateaux/"+str(n)+"/"+str(tourTemp)+".txt") as json_file:
					writingTempDictio.update(json.load(json_file))
					ecrireFichier(genFichier(n,tourTemp),writingTempDictio)
		return dictio

