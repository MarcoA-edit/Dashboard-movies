import pandas as pd
import ast

def processar_json_ratings(arquivo_json, arquivo_saida):
    dados = pd.read_json(arquivo_json)
    
    if "Ratings" in dados.columns:
        dados = dados.dropna(subset=["Ratings"])

        ratings_expandido = pd.json_normalize(dados['Ratings'])
        ratings_expandido.columns = [f"Ratings_{col}" for col in ratings_expandido.columns]

        dados = dados.drop(columns=["Ratings"]).join(ratings_expandido)
    else:
        print("A coluna 'Ratings' não foi encontrada no JSON.")
        return

    colunas_ratings = [col for col in dados.columns if col.startswith('Ratings_')]
    if not colunas_ratings:
        print("Nenhuma coluna válida 'Ratings_*' foi encontrada após expansão.")
        return

    linhas_expandida = []

    for _, row in dados.iterrows():
        for col in colunas_ratings:
            try:
                rating_dict = ast.literal_eval(row[col]) if isinstance(row[col], str) else row[col]
                if isinstance(rating_dict, dict):
                    nova_linha = row.copy()
                    nova_linha["Ratings_Source"] = rating_dict.get("Source", "")
                    nova_linha["Ratings_Value"] = rating_dict.get("Value", "")
                    linhas_expandida.append(nova_linha)
            except (ValueError, SyntaxError, TypeError):
                continue

    if linhas_expandida:
        dados_expandidos = pd.DataFrame(linhas_expandida)

        fontes_desejadas = ["Internet Movie Database", "Rotten Tomatoes", "Metacritic"]
        dados_expandidos = dados_expandidos[dados_expandidos["Ratings_Source"].isin(fontes_desejadas)]

        dados_expandidos.to_csv(arquivo_saida, index=False, encoding='utf-8')
        print(f"Arquivo CSV final salvo como: {arquivo_saida}")
    else:
        print("Nenhuma linha válida encontrada com colunas 'Ratings'.")


arquivo_json = 'data.json' 
csv_final = 'add.csv'  

processar_json_ratings(arquivo_json, csv_final)
