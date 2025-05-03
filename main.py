import pandas as pd

file_path = "dati-classifica-sanremo-1951-2023.xlsx"
df = pd.read_excel(io=file_path)
df = df.set_index("Unnamed: 0")
df.index.name = None

print(df.head(10))

df.to_excel("output.xlsx", index= False)