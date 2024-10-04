import pandas as pd

def process_dictionary(excel_file_path, output_csv_path):
    """
    Traite un fichier Excel contenant un dictionnaire de mots avec leurs catégories et sauvegarde le résultat dans un fichier CSV

    Entrée:
        excel_file_path (str): Chemin vers le fichier Excel à traiter
        output_csv_path (str): Chemin vers le fichier CSV de sortie
    """
    # Chargement du fichier excel dans un dataframe
    df = pd.read_excel(excel_file_path)

    second_column = df.columns[1]  # Extraction des lemmes
    third_column = df.columns[2]  # Extraction des catégories

    # Dictionnaire de remplacement des catégories
    replace_dict = {
        'Nom:': 'NOUN',
        'Ver:': 'VERB',
        'Pre': 'ADP',
        'Adj:': 'ADJ',
        'Abr': 'X',
        'Ono': 'X',
        'Int': 'INTJ',
        'Det': 'DET',
        'Pct': 'PUNCT',
        'Pro': 'PROUN',
        'QPr:': 'PRON',
        'Adv': 'ADV'
    }

    # Parcours avec remplacement des items
    for key, value in replace_dict.items():
        df.loc[df[third_column].str.contains(key, na=False), third_column] = value

    # Ajout du traitement pour les conjonctions
    conjunctions = ['mais', 'ou', 'et', 'donc', 'or', 'ni', 'car']
    df.loc[df[second_column].isin(conjunctions) & (df[third_column] == 'Con'), third_column] = 'CCONJ'

    # Remplacement de nom de catégorie
    df.loc[df[third_column].str.contains('Con', na=False), third_column] = 'SCONJ'
    df.loc[df[third_column].str.contains('Nom', na=False), third_column] = 'NOUN'

    # Renommage des colonnes
    df.columns = ['forme', 'lemme', 'catégorie']

    # Sauvegarde dans un fichier CSV
    df.to_csv(output_csv_path, index=False)

# Exemple d'appel de la fonction avec les chemins appropriés
process_dictionary('pos_upos/input_files/dico-utf8.xlsx', 'pos_upos/output_files/dico-utf8-UPOS.csv')
