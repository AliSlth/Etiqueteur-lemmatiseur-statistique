# Etiqueteur-lemmatiseur-syntaxique
L’objectif de ce projet est de développer une série de fonctions Python permettant d'entrainer un étiquetteur lemmatiseur statistique.

Le projet est incomplet, il reste des fonctionnalités à développer.

## Étapes du développement de l'étiqueteur

1. Conversion des étiquettes 

2. train() : Lecture du fichier conll et dictionnaires

3. Calculs de probabilités

3. 1. p(lem i/context)

3. 2. p(cat i/context)

3. 3. Écriture au format csv

3. 4. Calcul argmax 

3. 5. Probabilités pour une suite non rencontrée

4. create_dic() : Création du dictionnaire 

5. tag() : Lemmatisation et étiquetage 

6. Evaluation
## Ressources

Corpus: 
* Entraînement: “fr_gsd-ud-train.conll” (https://universaldependencies.org/treebanks/fr_gsd/)

* Test: “fr_sequoia-ud-test-TAG.conll” (https://universaldependencies.org/treebanks/fr_sequoia/) 

* Dictionnaire de formes fléchies : “dico-utf8” `la ref est : http://abu.cnam.fr/DICO/mots-communs.html`


# Développement

Prérequis et installation : 
* import pandas as pd
* import openpyxl
* import tqdm 
* import csv
* import shelve
* import os

## 1. Conversion des étiquettes 

À partir du dictionnaire de formes fléchies "dico-utf8.xls"

    pos_upos/scripts/mix_dico.py

Les résultats sont dans `pos_upos/output_files/... `

## 2. train() Lecture du fichier conll et dictionnaires

 `training/scripts/train.py`
Les dictionnaires shelves de sortie sont dans le dossier `training/stats_files`

### Description
On regroupe toutes les lignes d'une phrase dans une liste, puis en les traitant ensemble. Lorsque la phrase est complète (ligne vide rencontrée), on ajoute les tokens de début et de fin de phrase <eos>. Ensuite, dans une seule boucle, le code calcule les bigrammes, trigrammes, et autres statistiques (lemmes, formes, etc.) en parcourant cette liste. 

### Listes de variables

`bigram_freq `fréquence d'occurrence des suites de 2 étiquettes UPOS

`trigram_freq `fréquence d'occurrence des suites de 3 étiquettes UPOS

`lem_freq `fréquence d'occurrence des lemmes

`form_lem_freq `fréquence d'occurrence suites form+lem

`lem_form_freq `fréquence d'occurrence des suites lem + form

`form_lem_form_freq `fréquence d'occurrence des suites form+lem+form

`form_x_form_freq `fréquence d'occurrence des suites form+...+form

+`form_freq `fréquence d'occurrence des formes (fréquence utilisée plus tard pour la partie 3.5 du calcul des probabilités pour une suite non rencontrée)

## 3. Calculs de probabilités p(lem_cat/ context) 

### 3.1 p(lemi/context)

Après avoir exécuté le script `training/scripts/train.py`, exécuter `training/scripts/calcul_p/proba_lem_1/calcul_p_lem_1.py`


