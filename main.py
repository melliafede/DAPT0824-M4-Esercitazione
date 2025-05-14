import re
import pandas as pd
from collections import Counter
from sentence_transformers import SentenceTransformer, util


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)

file_path = "dati-classifica-sanremo-1951-2023.xlsx"
df = pd.read_excel(io=file_path)
df = df.set_index("Unnamed: 0")
df.index.name = None

''' Generazione tokens '''
articoli_determinativi = ['il', 'lo', "la", 'i', 'gli', 'le', 'l']
articoli_indeterminativi = ['un', 'uno', 'una', 'un']
preposizioni_semplici = ['di', "d", 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra']
preposizioni_articolate = [
    'del', 'dello', 'della', 'dei', 'degli', 'delle',
    'al', 'allo', 'alla', 'ai', 'agli', 'alle',
    'dal', 'dallo', 'dalla', 'dai', 'dagli', 'dalle',
    'nel', 'nello', 'nella', 'nei', 'negli', 'nelle',
    'sul', 'sullo', 'sulla', 'sui', 'sugli', 'sulle',
    'col', 'coi'
]
congiunzioni_coordinanti = [
    'e', 'o', 'ma', 'però', 'bensì', 'anzi', 'infatti',
    'oppure', 'quindi', 'dunque', 'cioè', 'eppure', 'né', 'pure'
]

pronomi_personali = [
    'io', 'tu', 'lui', 'lei', 'noi', 'voi', 'loro',
    'mi', 'ti', 'ci', 'vi', 'lo', 'la', 'li', 'le',
    'gli', 'ne', 'si', "te", "me"
]

pronomi_possessivi = [
    'mio', 'mia', 'miei', 'mie',
    'tuo', 'tua', 'tuoi', 'tue',
    'suo', 'sua', 'suoi', 'sue',
    'nostro', 'nostra', 'nostri', 'nostre',
    'vostro', 'vostra', 'vostri', 'vostre',
    'loro'
]
pronomi_dimostrativi = [
    'questo', 'questa', 'questi', 'queste',
    'quello', 'quella', 'quelli', 'quelle',
    'ciò'
]
pronomi_relativi = [
    'che', 'cui', 'il quale', 'la quale', 'i quali', 'le quali'
]
pronomi_interrogativi_esclamativi = [
    'chi', 'che', 'cosa', 'quale', 'quanto', 'quanti', 'quanta', 'quante'
]
pronomi_indefiniti = [
    'qualcuno', 'qualcuna', 'qualcosa', 'chiunque', 'alcuni', 'alcune', 'alcuno', 'alcuna',
    'nessuno', 'nessuna', 'niente', 'nulla', 'tutti', 'tutte', 'tutto', 'ciascuno', 'ciascuna',
    'ognuno', 'ognuna', 'altro', 'altra', 'altri', 'altre'
]
avverbi_negazione = [
    "non", "mai", "più", "affatto", "mica", "neanche", "nemmeno", "neppure",
    "niente", "nulla", "alcunché", "nessuno"
]

exclude_words = (articoli_indeterminativi + articoli_determinativi + preposizioni_semplici + preposizioni_articolate
                 + congiunzioni_coordinanti + pronomi_indefiniti + pronomi_personali + pronomi_possessivi
                 + pronomi_relativi + pronomi_dimostrativi + pronomi_interrogativi_esclamativi
                 + avverbi_negazione)

token_values = []
for index, row in df.iterrows():
    tokens = re.findall(r'\b\w+\b', row["Canzone"])
    tokens = [t.lower() for t in tokens]
    filtered_tokens = [t for t in tokens if t not in exclude_words]
    token_values.append(filtered_tokens)

df["Tematiche"] = token_values

print(df.loc[:, ["anno", "Canzone", "Tematiche"]])

grouped = df.groupby("anno")["Tematiche"].sum()
print("-"*50)
print(grouped)
word_counts = grouped.apply(lambda words: Counter(words).most_common())
grouped.apply(lambda words: Counter(dict(Counter(words).most_common())))
print(word_counts)



all_tokens = df["Tematiche"].sum()
tokens_count = Counter(all_tokens)
print("-" * 50)
print(tokens_count)

words_df = pd.DataFrame(tokens_count.items(), columns=["Words", "Frequency"]).sort_values(by="Frequency", ascending=False)
print(words_df)

# """ Test with sentence transformer"""
# # Carica il modello multilingua
# model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
#
# # Definisci i temi e descrizioni rappresentative
# temi = {
#     "amore": "amore, cuore, emozione, affetto",
#     "musica": "musica, canzone, melodia, ritmo",
#     "libertà": "libertà, volare, sogno, volo",
#     "natura/tempo": "notte, giorno, cielo, tempo, natura",
#     "dolore/emozioni": "tristezza, pianto, dolore, lacrime",
#     "altro": "altri argomenti generici"
# }
#
# # Calcola gli embeddings dei temi
# temi_testi = list(temi.values())
# temi_labels = list(temi.keys())
# temi_embeddings = model.encode(temi_testi, convert_to_tensor=True)
#
# titoli = df["Canzone"].tolist()
# titoli_embeddings = model.encode(titoli, convert_to_tensor=True)
#
# # Assegna il tema più simile a ciascun titolo
# assegnazioni = []
# for i, titolo in enumerate(titoli):
#     sim_scores = util.cos_sim(titoli_embeddings[i], temi_embeddings)
#     best_idx = sim_scores.argmax()
#     assegnazioni.append(temi_labels[best_idx])
#
# # Aggiunge la colonna "Tema"
# df["Tema"] = assegnazioni
#
# print("-" * 50)
# print(df.loc[:, ["anno", "Canzone", "Tema"]])

""" Conversione posizione """
df["Posizione"] = df["Posizione"].astype(str)
pos_values = []
for index, row in df.iterrows():
    pos_value = re.findall(r'\d+', row["Posizione"])
    if len(pos_value) > 0:
        pos_values.append(int(pos_value[0]))
    else:
        pos_values.append(row["Posizione"])

df["Pos"] = pos_values

# print(df.loc[:, ["anno","Posizione", "Pos"]])

numero_titoli = df.shape[0]


words_df.to_csv("words_count.csv", index=False, encoding="utf-8")
df.to_csv("output.csv", index=False, encoding="utf-8")
