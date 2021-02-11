# Room Assignment Problem

L'objectif est d'assigner une chambre à chaque étudiant, en tenant compte des préférences de chambre et de voisins de chambre. Chaque étudiant donne 3 voeux de chambre et 3 préférences de voisins.

Le problème est modélisé par un problème *d'optimisation linéaire* et résolu avec [l'algorithme hongrois](https://fr.wikipedia.org/wiki/Algorithme_hongrois).

Le résultat de l'affectation est ajouté au fichier CSV initial dans la colonne *Rooms* et stocké par défaut dans le fichier *result.csv* pour préserver le fichier CSV d'entrée.

Le fichier *debug.log* contient les traces de l'exécution du programme, à savoir les *dataframes* générées en entrée et en sortie, la matrice d'adjacence et la matrice des coûts. 

## Utilisation

Pour afficher les options possibles:
```bash
[~/room-assignment]$ python3 src/solution.py --help
```

Pour tester le programme avec options:
```bash
[~/room-assignment]$ python3 src/solution.py tests/data.csv tests/result.csv
```

Le fichier d'entrée est recherché par défaut dans le répertoire courant sous le nom de *data.csv*. Le fichier de sortie généré par défaut se trouve aussi dans le répertoire courant sous le nom de *result.csv*:
```bash
[~/room-assignment]$ python3 src/solution.py
```

Pour exécuter les tests:
```bash
[~/room-assignment]$ nosetests3 -v
```

## Possibilités d'extension

Il est possible d'effectuer un plus grand nombre de choix de chambre ou de voisin sans modifier l'algorithme. Seule la fonction de lecture du fichier CSV est à modifier. 

Il est aussi possible de n'effectuer aucun choix. Une chambre est tout de même assignée par l'algorithme du moment que le nom de l'étudiant est renseigné.

Il est possible de modifier le dictionnaire des chambres voisines afin de mieux représenter l'agencement des chambres.