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

# Initialiser un tableau à 2 dimensions avec la valeur val
def initializeTab(n, tab, val):
	for i in range(n):
		tab.append([])
		for j in range(n):
			tab[i].append(val);

# Ecrire le contenu du tableau tab dans le fichier fd
def writeTab(tab, fd, couleur):
	fd.write(str(couleur)+" - ")
	for x in tab:
		for y in x:
			fd.write(str(y) + " ");
	fd.write("\n");

# Creer le tableau voisin initial avec pour chaque sommet, la liste des autres sommets adjacents
def voisins(n):
	voisins = []
	for i in range(n):
		voisins.append([])
		for j in range(n):
			voisins[i].append([])

	for i in range(n):
		for j in range(n):
			if (i-1 >= 0) and (j+1 < n):
				voisins[i][j].append((i-1)*n+j)
				voisins[i][j].append(i*n+(j+1))
				voisins[i][j].append((i-1)*n+(j+1))
			elif(i-1 >= 0):
				voisins[i][j].append((i-1)*n+j)
			elif(j+1 < n):
				voisins[i][j].append(i*n+(j+1))

			if (i+1 < n) and (j-1 >= 0):
				voisins[i][j].append((i+1)*n+j)
				voisins[i][j].append(i*n+(j-1))
				voisins[i][j].append((i+1)*n+(j-1))
			elif(i+1 < n):
				voisins[i][j].append((i+1)*n+j)
			elif(j-1 >= 0):
				voisins[i][j].append(i*n+(j-1))

	return voisins

# Determiner, a partir d'un tableau composante, si le joueur couleur a gagne en jouant le sommet i
def victoire(tab,i,voisin,couleur,composantes):
	n = len(tab)
	for indice in (voisin[i//n][i%n]):
		if (tab[indice//n][indice%n] == couleur):
			# La composante d'un bord du plateau est prioritaire sur les autres
			if ((composantes[i//n][i%n] != couleur*1000+1) and (composantes[i//n][i%n] != couleur*1000+2)):
				composantes[i//n][i%n] = composantes[indice//n][indice%n]
			else:
				# Si un sommet 1 a un voisin de composante 1001 (Bord Gauche) et un voisin de composante 1002 (Bord Droit)			
				# Si un sommet 2 a un voisin de composante 2001 (Bord Haut) et un voisin de composante 2002 (Bord Bas)	
				if ((composantes[i//n][i%n] == couleur*1000+1) and (composantes[indice//n][indice%n] == couleur*1000+2)) or ((composantes[indice//n][indice%n] == couleur*1000+1) and (composantes[i//n][i%n] == couleur*1000+2)):
					return couleur
	return 0

def genPlateaux(n, fd):
	#Chaque valeur du tab va passer respectivement par les 3 états suivant LIBRE -> BLEU -> ROUGE
	tab = [];
	initializeTab(n, tab, 0);

	fini=0;#Nombre de plateaux existants
	i=0; #indice
	taille = n*n #Taille totale de la matrice
	nbSommets = [taille, 0, 0]; #tab des nombres de sommets [ROUGE, BLEU, LIBRE]

	composantes = [];
	initializeTab(n, composantes, 0);

	voisin = voisins(n)
	couleurGagnante = 0; # Stock la couleur gagnante, s'il y en a une, du plateau actuel	

	while (tab[0][0] <= BLEU) :
		if(i<taille):
			if(tab[i//n][i%n]>2):
				tab[i//n][i%n]=0;
				nbSommets[BLEU] -= 1

				i-=1;
				tab[i//n][i%n]+=1;

				if (tab[i//n][i%n] == 1): 
					nbSommets[ROUGE] +=1
					if (i%n==0):
						composantes[i//n][i%n] = 1001
					elif (i%n==n-1):
						composantes[i//n][i%n] = 1002
					else:
						composantes[i//n][i%n] = 1
				elif (tab[i//n][i%n] == 2): 
					nbSommets[ROUGE]-=1
					nbSommets[BLEU]+=1
					if (i < n):
						composantes[i//n][i%n] = 2001
					elif (i/n > n-1):
						composantes[i//n][i%n] = 2002
					else:
						composantes[i//n][i%n] = 2

				couleurGagnante = victoire(tab,i,voisin,tab[i//n][i%n],composantes)

			else:
				i+=1;
		else:
			if couleurGagnante and (abs(nbSommets[ROUGE] - nbSommets[BLEU]) <= 1):
				writeTab(tab, fd, couleurGagnante);
				fini+=1;

			i-=1;
			tab[i//n][i%n]+=1;

			if (tab[i//n][i%n] == 1): 
				nbSommets[ROUGE]+=1
				composantes[i//n][i%n] = 1002
			elif (tab[i//n][i%n] == 2): 
				nbSommets[ROUGE]-=1
				nbSommets[BLEU]+=1
				composantes[i//n][i%n] = 2002
			couleurGagnante = victoire(tab,i,voisin,tab[i//n][i%n],composantes)

	return fini;


#-----------------------------MAIN-----------------------------#
taille = int(input('Dimension de la grille : (entre 3 et 15) : '));
fd = genFile(taille);
fini = genPlateaux(taille, fd);
print("Il y a "+ str(fini)+" plateaux de taille "+str(taille));