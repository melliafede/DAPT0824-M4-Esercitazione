import re

import pandas as pd

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
preposizioni_semplici = ['di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra']
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
    'gli', 'ne', 'si'
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

exclude_words = (articoli_indeterminativi + articoli_determinativi + preposizioni_semplici + preposizioni_articolate
                 + congiunzioni_coordinanti + pronomi_indefiniti + pronomi_personali + pronomi_possessivi
                 + pronomi_relativi + pronomi_dimostrativi + pronomi_interrogativi_esclamativi)

token_values = []
for index, row in df.iterrows():
    tokens = re.findall(r'\b\w+\b', row["Canzone"])
    filtered_tokens = [t for t in tokens if t.lower() not in exclude_words]
    token_values.append(filtered_tokens)

df["Tematiche"] = token_values

print(df.loc[:, ["anno", "Canzone", "Tematiche"]])

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

df.to_excel("output.xlsx", index=False)
