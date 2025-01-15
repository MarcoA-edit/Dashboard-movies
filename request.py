import requests
import json
import pandas as pd

df = pd.read_csv('carga.csv')

def consultar_omdb(api_key, titulo, tipo="movie", ano=None):
    url = "http://www.omdbapi.com/"
    parametros = {
        "apikey": api_key,
        "t": titulo,
        "type": tipo,
    }
    if ano:
        parametros["y"] = ano
    
    try:
        resposta = requests.get(url, params=parametros)
        resposta.raise_for_status()
        dados = resposta.json()
        if dados.get("Response") == "True":
            return dados
        else:
            return {"Erro": dados.get("Error", "Erro desconhecido")}
    except requests.exceptions.RequestException as e:
        return {"Erro": str(e)}

def salvar_json(dados, nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"JSON salvo no arquivo: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

if __name__ == "__main__":
    api_key = "58a82d96"
    
    resultados = []

    for titulo in df['Filme']:
        print(f"Consultando o filme: {titulo}")
        resultado = consultar_omdb(api_key, titulo)
        
        if "Erro" in resultado:
            print(f"Erro ao consultar {titulo}: {resultado['Erro']}")
        else:
            resultados.append(resultado)

    salvar_json(resultados, "data.json")
