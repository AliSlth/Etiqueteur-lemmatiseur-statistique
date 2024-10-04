import shelve

def probabilite_max(output_p_lemme, output_p_categorie, output_probabilite_max):
    with shelve.open(output_p_lemme) as file1, shelve.open(output_p_categorie) as file2, shelve.open(output_probabilite_max, 'c') as output_file:
        keys_1 = file1.keys()
        keys_2 = file2.keys()
        
        for key_1 in keys_1:
            if key_1 in keys_2: 
                value_key_1, value_key_2 = file1[key_1], file2[key_1]
                probability_max = value_key_1 * value_key_2
                output_file[key_1] = probability_max

probabilite_max(output_p_lemme, output_p_categorie, output_probabilite_max)
