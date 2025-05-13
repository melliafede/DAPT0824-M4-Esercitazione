import pandas as pd
import re
from collections import Counter

file_path = "dati-classifica-sanremo-1951-2023.xlsx"
df = pd.read_excel(io=file_path)
df = df.set_index("Unnamed: 0")
df.index.name = None

''' Filtro il dataset dal 2005 al 2023'''
df = df[(df["anno"] >= 2005) & (df["anno"] <= 2023)]

''' Creo una lista di tokens per capire quali sono le parole ed in seguito le tematiche più ricorrenti
nei titoli delle canzoni di Sanremo '''
non_words_list = ["non", "dei", "tra", "gli", "una", "che", "mio", "mia", "del", "per", "quando", "più", "come", "mai",
                  "sei", "con", "così", "noi", "qui", "nel"]

pattern = r'\b(?!' + '|'.join(non_words_list) + r'\b)\w{3,}\b'
print(pattern)
all_tokens = []
for canzone in df["Canzone"]:
    for word in re.findall(pattern, canzone, re.IGNORECASE):
        all_tokens.append(word)

print(Counter(all_tokens))
unique_tokens = [item[0] for item in Counter(all_tokens).most_common()]

tokens_list = []
for canzone in df["Canzone"]:
    tokens_list.append(re.findall(pattern=r'\b\w{3,}\b', string=canzone))

df["Tokens"] = tokens_list
print(df.loc[:, ("Canzone", "Tokens", "anno")])

''' Pulizia della colonna Posizione'''
df["Posizione"] = df["Posizione"].astype(str)

positions = []
for posizione in df["Posizione"]:
    numbers_list = re.findall(r'(?<!\w)\d+', posizione)
    if len(numbers_list) > 0:
        positions.append(int(numbers_list[0]))
    else:
        positions.append(99)  # posizione non presente

df["Posizione"] = positions
print(df.loc[:, ("Canzone", "Tokens", "Posizione")])

''' Filtro per top 5 classificati di ogni anno '''
df = df[df["Posizione"] <= 5]
print(df.loc[:, ["Canzone", "Posizione", "anno"]])

for index, row in df.iterrows():
    print(f"{row["Canzone"]} | {row["Posizione"]} | {row["anno"]}")
    """ Mancano alcuni dati sulle posizioni """

for token in unique_tokens:
    match_count = df["Canzone"].str.contains(rf'\b{token}\b', case=False).sum()
    percentage = (match_count / df.shape[0]) * 100
    if percentage > 1:
        print(f"{token} appears in {percentage:.2f}% of top 5 songs")
