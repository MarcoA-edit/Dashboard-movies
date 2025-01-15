import pandas as pd

df1 = 'add.csv'
df2 = 'df_final.csv'

dados = pd.read_csv(df1)

colunas = [
    "Title", "Year", "Released", "Runtime", "Genre", "Director", "Writer",
    "Actors", "Plot", "Awards", "Poster", "Metascore", "imdbRating",
    "imdbVotes", "imdbID", "Type", "DVD", "BoxOffice", "Ratings_Source", "Ratings_Value"
]

if "Rotten Tomatoes" in dados["Ratings_Source"].values:
    dados_filtrados = dados[dados["Ratings_Source"] == "Rotten Tomatoes"]
else:
    dados_filtrados = dados[dados["Ratings_Source"] == "Internet Movie Database"]

dados_final = dados_filtrados[colunas]

df = pd.read_csv(df2)

saida = pd.concat([dados_final, df], ignore_index=True)

saida.to_csv(df2, index=False, encoding="utf-8")

print(f"Arquivo salvo como: {df2}")
