import shelve
from tqdm import tqdm

def p_form_lem(form_freq, form_lem_freq, output_shelve):
    with shelve.open(form_freq) as file1, shelve.open(form_lem_freq) as file2, shelve.open(output_shelve, 'c') as output_file:
        form_freq_values = list(file1.values())[0]
        form_lem_freq_values = list(file2.values())[0]

        for key, value in tqdm (form_lem_freq_values.items(), desc="Calcul des probabilités", unit=" entries"):
            form_lem = key.split("_")
            elt1 = form_lem[0]
            elt2 = form_lem[1]
            search_key = elt1
            suite = elt1 + "_" + elt2

            if search_key in form_freq_values:
                freq_occurrence = form_freq_values[search_key]
                p_form_lem = value / freq_occurrence
                output_file[suite] = p_form_lem
    
form_freq = "training/stats_files/form"
form_lem_freq = "training/stats_files/form_lem"
output_shelve = "training/output_files/p_form_lem"

p_form_lem(form_freq, form_lem_freq, output_shelve)


def p_lem_form(lem_freq, lem_form_freq, output_shelve):
    with shelve.open(lem_freq) as file1, shelve.open(lem_form_freq) as file2, shelve.open(output_shelve, 'c') as output_file:
        lem_freq_values = list(file1.values())[0]
        lem_form_freq_values = list(file2.values())[0]

        for key, value in tqdm (lem_form_freq_values.items(), desc="Calcul des probabilités", unit=" entries"):
            form_lem = key.split("_")
            elt1 = form_lem[0]
            elt2 = form_lem[1]
            search_key = elt1
            suite = elt1 + "_" + elt2

            if search_key in lem_freq_values:
                freq_occurrence = lem_freq_values[search_key]
                p_form_lem = value / freq_occurrence
                output_file[suite] = p_form_lem

lem_freq = "training/stats_files/lem"
lem_form_freq = "training/stats_files/lem_form"
output_shelve = "training/output_files/p_lem_form"
p_lem_form(lem_freq, lem_form_freq, output_shelve)


