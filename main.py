import re
import pandas as pd
from collections import Counter

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)

file_path = "dati-classifica-sanremo-1951-2023.xlsx"
df = pd.read_excel(io=file_path)
df = df.set_index("Unnamed: 0")
df.index.name = None

# print(df)
# exit()

file_path = "interpreti_sesso.txt"
interpreti_sesso_df = pd.read_csv(filepath_or_buffer=file_path, sep=";")
# print(interpreti_sesso_df)
# exit()

""" Aggiunta colonna sesso al dataframe """
df = pd.merge(df, interpreti_sesso_df, on="Interprete", how="left")
# print(df.loc[:, ["Interprete", "Sesso"]])
# exit()


# interpreti = list(df["Interprete"].unique())
# interpreti_df = pd.DataFrame(interpreti, columns=["Interprete"])
# print(interpreti_df)
# interpreti_df.to_csv("interpreti_unique.csv", index=False, encoding="utf-8")
# exit()

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
extra = [
    "è", "come", "sei", "se", "quando", "senza", "così", "grande", "no", "voglio",
    "solo", "ho", "bella", "ciao", "qui", "sono", "due"
]

exclude_words = (articoli_indeterminativi + articoli_determinativi + preposizioni_semplici + preposizioni_articolate
                 + congiunzioni_coordinanti + pronomi_indefiniti + pronomi_personali + pronomi_possessivi
                 + pronomi_relativi + pronomi_dimostrativi + pronomi_interrogativi_esclamativi
                 + avverbi_negazione + extra)

token_values = []
for index, row in df.iterrows():
    tokens = re.findall(r'\b\w+\b', row["Canzone"])
    tokens = [t.lower() for t in tokens]
    filtered_tokens = [t for t in tokens if t not in exclude_words]
    token_values.append(filtered_tokens)

df["Tematiche"] = token_values

print(df.loc[:, ["anno", "Canzone", "Tematiche"]])

grouped = df.groupby("anno")["Tematiche"].sum()
print("-" * 50)
print(grouped)
word_counts = grouped.apply(lambda words: Counter(words).most_common())
grouped.apply(lambda words: Counter(dict(Counter(words).most_common())))
print(word_counts)

all_tokens = df["Tematiche"].sum()
tokens_count = Counter(all_tokens)
print("-" * 50)
print(tokens_count)

words_df = pd.DataFrame(tokens_count.items(), columns=["Words", "Frequency"]).sort_values(by="Frequency",
                                                                                          ascending=False)
print(words_df)

""" Conversione posizione """
df["Posizione"] = df["Posizione"].astype(str)
pos_values = []
for index, row in df.iterrows():
    pos_value = re.findall(r'\b\d+', row["Posizione"])
    if len(pos_value) > 0:
        pos_values.append(int(pos_value[0]))
    else:
        pos_values.append(row["Posizione"])

df["Pos"] = pos_values

# print(df.loc[df["Interprete"] == "Alexia", ["anno", "Posizione", "Interprete"]])
# exit()

""" Filtro posizioni numeriche"""
pos_df = df[df["Pos"].apply(lambda x: isinstance(x, int))]

""" Canzoni vincenti """
winning_df = df.loc[df["Pos"] == 1]
flags_amore = []
for index, row in winning_df.iterrows():
    if "amore" in row["Tematiche"]:
        flags_amore.append("True")
    else:
        flags_amore.append("False")

winning_df["FlagAmore"] = flags_amore
print("-" * 50)
print(winning_df.shape[0])
print("-" * 50)
print(winning_df.loc[:, ["anno", "Canzone", "Tematiche", "Pos", "FlagAmore"]])

winning_words_list = winning_df["Tematiche"].sum()
print("-" * 50)
print("Winning words list")
print(Counter(winning_words_list))
print("-" * 50)

""" Top 3 """
top3_df = df.loc[(df["Pos"] == 1) | (df["Pos"] == 2) | (df["Pos"] == 3)]
flags_amore = []
for index, row in top3_df.iterrows():
    if "amore" in row["Tematiche"]:
        flags_amore.append("True")
    else:
        flags_amore.append("False")

top3_df["FlagAmore"] = flags_amore
print("-" * 50)
print(top3_df.shape[0])
print("-" * 50)
print(top3_df.loc[:, ["anno", "Canzone", "Tematiche", "Pos", "FlagAmore"]])

""" Conteggio numero titoli"""
numero_titoli = df.shape[0]
print(df)

""" Scrittura files """
pos_df.to_csv("pos_interpreti.csv", index=False, encoding="utf-8")
top3_df.to_csv("top3_titles.csv", index=False, encoding="utf-8")
winning_df.to_csv("winning_titles.csv", index=False, encoding="utf-8")
words_df.to_csv("words_count.csv", index=False, encoding="utf-8")
df.to_csv("output.csv", index=False, encoding="utf-8")
