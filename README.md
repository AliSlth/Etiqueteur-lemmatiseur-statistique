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

Pour la conversion des étiquettes, il y a eu deux approches différentes:

À partir du dictionnaire de formes fléchies "dico-utf8.xls"

    pos_upos/scripts/mix_dico.py

Les résultats sont dans `pos_upos/output_files/... `

## 2. train() Lecture du fichier conll et dictionnaires

 `training/scripts/train.py`
Les dictionnaires shelves de sortie sont dans le dossier `training/stats_files`

### Description
Cette fonction parcourt le fichier conll dans le répertoire training_files_dir et alimente les dictionnaires shelve (chemin des fichiers obtenus en sortie : “data/stats_files/…”).
Le comptage des fréquences d'occurrences des bigrammes et trigrammes se base sur un parcours des lignes commençant par un chiffre (pour cibler les lignes qui contiennent des informations linguistiques) et la vérification des lignes précédentes (ex. pour les bigrammes : extraire l’étiquette upos précédente et la concaténer avec l’étiquette upos de la ligne actuelle avec “_”, ce qui donne un bigramme qui ressemble à DET_NOUN).


### Listes de variables

`bigram_freq `fréquence d'occurrence des suites de 2 étiquettes UPOS

`trigram_freq `fréquence d'occurrence des suites de 3 étiquettes UPOS

`lem_freq `fréquence d'occurrence des lemmes

`form_lem_freq `fréquence d'occurrence suites form+lem

`lem_form_freq `fréquence d'occurrence des suites lem + form

`form_lem_form_freq `fréquence d'occurrence des suites form+lem+form

`form_x_form_freq `fréquence d'occurrence des suites form+...+form

+`form_freq `fréquence d'occurrence des formes (fréquence utilisée plus tard pour la partie 3.5 du calcul des probabilités pour une suite non rencontrée)

### Remarques / Améliorations: 

Puisque nous avons pris en compte les lignes commençant par un chiffre, il fallait faire attention à ne pas prendre les trigrammes entre les différentes phrases pour garder un contexte cohérent. (voir #trigramme)
`Pour gérer les débuts et fins de phrases, vous pouvez utiliser une marque du type <EOS> ou une marque de padding : les débuts et fins de phrases sont aussi des contextes informatifs.`
Comme chaque dictionnaire a été créée l’un après l’autre, le code est parfois répétitif et manque d’optimisation
Il aurait fallu traiter les cas où les données sont sur plusieurs lignes : le corpus d’entraînement contient ex: le cas de “des” qui est séparé sur deux lignes en “de” puis “les” (ex: ligne 33 dans training/input_files/fr_gsd-ud-train.conll”

## 3. Calculs de probabilités p(lem_cat/ context) -> Xinyi et Alissa

### 3.1 p(lemi/context) -> Xinyi et Alissa

Au départ, la création des dictionnaires de fréquences était répartie comme suit : Alissa s'est occupée de bigram_freq, trigram_freq et lem_freq, lem_form_freq et form_lem_freq tandis que Xinyi a travaillé sur form_lem_form_freq et form_x_form_freq. Cependant, nous avons rencontré des difficultés lors de la fusion de nos codes générant les dictionnaires. Lorsque nous avons tenté d'assembler les deux parties pour calculer les probabilités, nous avons rencontré d'autres problèmes de sortie de données, aboutissant à des fichiers vides.

Nous avons donc 2 versions du calcul de la probabilité pour p_lemme: 

3.1.1  Version 1 -> Alissa

Après avoir exécuté le script `training/scripts/train.py`, exécuter `training/scripts/calcul_p/proba_lem_1/calcul_p_lem_1.py`

3.1.2 Version 2 -> Xinyi

Après avoir exécuté le script `training/scripts/train.py`, exécuter `training/scripts/calcul_p/proba_lem_2/calcul_p_lem_2.py`
Les fichiers en entrée de la fonction (dictionnaires form_lem_form_2 et form_x_form_2 ont été générés par la fonction `training/scripts/proba_lem_2/calcul_p_lem_2.py`.

Le fichier de sortie se trouve dans `training/output_files/p_lemme`

### 3.1 p(cat i/context) -> Xinyi

Exécuter le script `training/scripts/calcul_p/calcul_p_cat.py`
Le fichier en sortie se trouve dans `training/output_files/p_categorie`

### 3.3 Écriture au format csv

Pour avoir une vision globale des données, nous avons écrit les données dans un fichier csv.

Exécuter `training/scripts/calcul_p/write_proba_csv.py`
Les fichiers csv se trouvent dans `training/output_files/…`

### 3.4 Calcul argmax (Xinyi)

Le script se trouve ici : `training/scripts/calcul_p/calcul_argmax.py`
Nous avons rencontré un problème où le fichier shelve `training/output_files/p_max`  est vide.

### 3.5 Probabilités pour une suite non rencontrée (Alissa)
Le code calcule les probabilités des bigrammes formi-1 lemi et lemi formi+1.

Exécuter `training/scripts/calcul_p/calcul_p_bigram.py`
Le résultat est stocké sous shelve dans `training/output_files/p_form_lem` et `training/output files/p_lem_form`

Le script permettant le calcul de la moyenne des probabilités n'a pas encore été implémenté.

## 4. Création du dictionnaire -> Lin

Même si deux dictionnaires ont été crées à la première étape (1. conversion des étiquettes) il n'a été utilisé pour cet tâche le `dico-utf8-UPOS`

Exécuter le script dans `create_dic/scripts/create_dic.py`

Le fichier de sortie se trouve dans `create_dic/output_files/dico_utf8_UPOS.shelve`


## 5. tag() : Lemmatisation et étiquetage -> Lin

Un début de code a été écrit : 

Étiquetage et la lemmatisation du fichier en entrée `tag/input_files/fr_sequoia-ud-test-TAG.conllu` et le résultat dans le fichier `tag/output_files/output-tag-test.conllu`. 

Exécuter le script dans `tag/scripts/tag.py`

La fonction n'est pas complète : nous avons tenté d'écrire un pseudo-code (Xinyi)

## 6. Evaluation -> Lin et Xinyi

Nous n'avons pas de données à tester mais un script python pour l'évaluation de la catégorie a été écrit en amont.

Voici le chemin d'accès `evaluation\scripts\evalu-categorie.py`

Un pseudo code a été écrit pour l'évaluation des lemmes (Xinyi)
