import shelve

def calculate_p_categorie(shelve_trigram, shelve_bigram, output_p_categorie):
    output_shelve = shelve.open(output_p_categorie, writeback=True)
    
    with shelve.open(shelve_trigram) as file1, shelve.open(shelve_bigram) as file2:  
        dict_trigram = file1['trigram_freq']
        dict_bigram = file2['bigram_freq']

    for key_tr, value_tr in dict_trigram.items():
        elements_tr = key_tr.split('_')
        cat_tr_1 = elements_tr[2]
        cat_tr_2 = elements_tr[1]    
        search_key = cat_tr_2 + '_' + cat_tr_1
           
        if search_key in dict_bigram: 
            value_tr, value_bi = dict_trigram[key_tr], dict_bigram[search_key]
            p_cat = value_tr / value_bi if value_bi != 0 else 0 
            output_shelve[f"{key_tr}----{search_key}"] = p_cat          

calculate_p_categorie(shelve_trigram, shelve_bigram, output_p_categorie)
