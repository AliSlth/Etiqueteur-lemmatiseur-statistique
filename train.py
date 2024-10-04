# Script écrit par Alissa Slth

import os
import shelve
from tqdm import tqdm

def train(training_files_dir, stats_files_dir):
    """
    Traite les fichiers d'entraînement CONLL pour extraire des statistiques
    sur les bigrammes, trigrammes, lemmes, et formes.
    Les résultats sont stockés dans des shelves.
    
    Args:
        training_files_dir (str): Chemin du répertoire contenant les fichiers d'entraînement.
        stats_files_dir (str): Chemin du répertoire pour stocker les statistiques.

    Returns:
        int: Le nombre total de tokens traités.
    """
    token_count = 0  # Initialisation du compteur de tokens

    for file_name in os.listdir(training_files_dir):
        if file_name.endswith(".conll"): #Traitement des fichiers conll
            file_path = os.path.join(training_files_dir, file_name)


            # Ouverture et lecture des fichiers
            with open(file_path, "r", encoding="utf-8") as conll_file:
                lines = conll_file.readlines()
                
            # Initialisation des dictionnaires de fréquences
            bigram_freq = {}
            trigram_freq = {}
            lem_freq = {}
            form_lem_freq = {}
            lem_form_freq = {}
            form_lem_form_freq = {}
            form_x_form_freq = {}
            form_freq = {}
            phrase_courante = []  # Liste pour stocker tous les tokens de la phrase

            for current_line in tqdm(lines, desc=f"Traitement des lignes dans {file_name}"):
                if current_line[0].isdigit():  # Ligne commençant par un chiffre
                    token_count += 1  
                    line_part = current_line.split("\t")  # On extrait la ligne
                    forme = line_part[1]  # Forme
                    lemme = line_part[2]  # Lemma
                    pos_tag = line_part[3]  # POS tag

                    # Vérifier que la forme et le POS tag sont valides
                    if forme and pos_tag and pos_tag != "_":
                        # Créer une liste contenant ces éléments
                        token = [forme, lemme, pos_tag]
                        phrase_courante.append(token)  # Ajoute le token à la phrase courante

                else:  # Si current_line est une ligne vide == nouvelle phrase, traiter la phrase courante 
                    if current_line == "\n":
                        # Ajouter deux tokens vides <EOS> en début et fin de phrase
                        phrase_courante.insert(0, ['<EOS>', '<EOS>', '<EOS>'])
                        phrase_courante.append(['<EOS>', '<EOS>', '<EOS>'])
                        print("Traitement de la phrase en cours :", phrase_courante)
                        
                        # Parcourir les tokens de chaque phrase courante
                        for i in range(0, len(phrase_courante) - 1):
                            current_form = phrase_courante[i][0]  # Forme
                            lem = phrase_courante[i][1]  # Lemme
                            current_upos = phrase_courante[i][2]  # POS tag
                            previous_form = phrase_courante[i - 1][0]  # Forme précédente
                            prev_lem = phrase_courante[i - 1][1]  # Lemme précédent
                            previous_upos = phrase_courante[i - 1][2]  # POS tag précédent

                            # BIGRAMME
                            if current_upos and previous_upos and current_upos != "<EOS>" and previous_upos != "<EOS>":
                                bigram = f"{previous_upos}_{current_upos}"
                                if bigram in bigram_freq:
                                    bigram_freq[bigram] += 1
                                else:
                                    bigram_freq[bigram] = 1  

                            # LEMME
                            if lem != "<EOS>":
                                if lem in lem_freq:
                                    lem_freq[lem] += 1
                                else:
                                    lem_freq[lem] = 1
                                    
                            # FORM
                            if current_form != "<EOS>":
                                if current_form in form_freq:
                                    form_freq[current_form] += 1
                                else:
                                    form_freq[current_form] = 1

                            # FORM_LEM et LEM_FORM
                            if lem != "<EOS>" and current_form != "":
                                form_lem_key = f"{previous_form}_{lem}"
                                if form_lem_key in form_lem_freq:
                                    form_lem_freq[form_lem_key] += 1
                                else:
                                    form_lem_freq[form_lem_key] = 1

                                lem_form_key = f"{lem}_{previous_form}"
                                if lem_form_key in lem_form_freq:
                                    lem_form_freq[lem_form_key] += 1
                                else:
                                    lem_form_freq[lem_form_key] = 1


                            if i > 2:

                                previous_previous_form = phrase_courante[i - 2][0]  # Forme précédente précédente
                                previous_previous_upos = phrase_courante[i - 2][2]  # POS tag précédent précédent

                                # TRIGRAMME
                                if previous_previous_upos and previous_upos and previous_previous_upos != "<EOS>" and previous_upos != "<EOS>" and current_upos != "<EOS>":
                                    trigram = f"{previous_previous_upos}_{previous_upos}_{current_upos}"
                                    if trigram in trigram_freq:
                                        trigram_freq[trigram] += 1
                                    else:
                                        trigram_freq[trigram] = 1
                        
                                # FORME_LEMME_FORME
                                form_lem_form = f"{previous_previous_form}_{prev_lem}_{current_form}"
                                if form_lem_form in form_lem_form_freq:
                                    form_lem_form_freq[form_lem_form] += 1
                                else:
                                    form_lem_form_freq[form_lem_form] = 1

                                # FORME_X_FORME
                                form_x_form = f"{previous_previous_form}_{current_form}"
                                if form_x_form in form_x_form_freq:
                                    form_x_form_freq[form_x_form] += 1
                                else:
                                    form_x_form_freq[form_x_form] = 1


                        # Réinitialisation de la phrase courante après traitement
                        phrase_courante = []

            # Écriture dans les shelves
            with shelve.open(os.path.join(stats_files_dir, "bigram")) as bigram_shelve:
                bigram_shelve.update(bigram_freq)

            with shelve.open(os.path.join(stats_files_dir, "trigram")) as trigram_shelve:
                trigram_shelve.update(trigram_freq)

            with shelve.open(os.path.join(stats_files_dir, "lem")) as lem_shelve:
                lem_shelve.update(lem_freq)

            with shelve.open(os.path.join(stats_files_dir, "form_lem")) as form_lem_shelve:
                form_lem_shelve.update(form_lem_freq)

            with shelve.open(os.path.join(stats_files_dir, "lem_form")) as lem_form_shelve:
                lem_form_shelve.update(lem_form_freq)

            with shelve.open(os.path.join(stats_files_dir, "form_x_form")) as form_x_form_shelve:
                form_x_form_shelve.update(form_x_form_freq)

            with shelve.open(os.path.join(stats_files_dir, "form_lem_form")) as form_lem_form_shelve:
                form_lem_form_shelve.update(form_lem_form_freq)

            with shelve.open(os.path.join(stats_files_dir, "form")) as form_shelve:
                form_shelve.update(form_freq)

    return token_count

# Appel de la fonction
training_files_dir = "training/input_files"
stats_files_dir = "training/stats_files"
result = train(training_files_dir, stats_files_dir)
print("Nombre de tokens traités :", result)
