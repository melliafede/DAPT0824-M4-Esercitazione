import pandas as pd
import re
from collections import Counter

file_path = "dati-classifica-sanremo-1951-2023.xlsx"
df = pd.read_excel(io=file_path)
df = df.set_index("Unnamed: 0")
df.index.name = None

''' Filtro il dataset dal 2005 al 2023'''
df = df[(df["anno"] >= 2005) & (df["anno"] <= 2023)]

tokens_list = []
for canzone in df["Canzone"]:
    tokens_list.append(re.findall(r'\b\w{3,}\b', canzone))

df["Tokens"] = tokens_list

all_tokens = []
for token_list in df["Tokens"]:
    for token in token_list:
        all_tokens.append(token)
print(all_tokens)

print(Counter(all_tokens))


print(df.columns)
print(df.loc[:,["Canzone", "Tokens"]])

df["Posizione"] = df["Posizione"].astype(str)

ranking_list = []
for posizione in df["Posizione"]:
    positions = re.findall(r'\d+', posizione)
    if len(positions) > 0:
        ranking_list.append(positions[0])
    else:
        ranking_list.append(posizione)

df["Final ranking"] = ranking_list

df = df[df["Final ranking"] == "1"]

word_to_search = "amore"

match_count = df["Canzone"].str.contains(rf'\b{word_to_search}\b', case=False).sum()

percentage = (match_count / df.shape[0]) * 100
print(f"{word_to_search} appears in {percentage:.2f}% of winning songs")


