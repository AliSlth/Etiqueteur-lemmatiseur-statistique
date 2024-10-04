import pandas as pd
import shelve

def create_dic(csv_file_path, shelve_file_path):
    """
    Crée un dictionnaire à partir d'un fichier CSV et le sauvegarde dans un fichier shelve.

    Sortie:
        csv_file_path (str): Chemin du fichier CSV à traiter.
        shelve_file_path (str): Chemin du fichier shelve où stocker le dictionnaire.
    """
    # Lecture du fichier CSV
    df = pd.read_csv(csv_file_path)

    dico = {} 

    for index, row in df.iterrows():
        key = row[0]  # La première colonne correspond à la clé
        value = (row[1], row[2])  # Les deuxième et troisième colonnes sont les valeurs (tuple)

        if key in dico:
            if value not in dico[key]:
                dico[key].append(value)
        else:
            dico[key] = [value]

    with shelve.open(shelve_file_path) as db:
        db.update(dico)

# Exemple d'appel de la fonction
create_dic('create_dic/output_file/dico-utf8-UPOS.csv', 'create_dic/output_file/dico_utf8_UPOS.shelve')
