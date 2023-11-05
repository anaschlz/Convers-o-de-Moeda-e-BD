import requests
import sqlite3
from datetime import datetime

# Chave de acesso à API da HG Brasil
api_key = "a11f3a19"

# Função para obter as taxas de câmbio da API
def obter_taxas_de_cambio():
    url = f'https://api.hgbrasil.com/finance?key={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

# Função para converter o valor em reais para dólares e euros
def converter_moeda(valor_em_reais, taxas_de_cambio):
    dolar = taxas_de_cambio['results']['currencies']['USD']['buy']
    euro = taxas_de_cambio['results']['currencies']['EUR']['buy']
    valor_em_dolares = valor_em_reais / dolar
    valor_em_euros = valor_em_reais / euro
    return valor_em_dolares, valor_em_euros

# Função para salvar as informações no banco de dados
def salvar_no_banco_de_dados(data_hora, valor_em_dolares, valor_em_euros):
    conn = sqlite3.connect('historico_cambio.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_cambio (
            data_hora DATETIME,
            valor_em_dolares REAL,
            valor_em_euros REAL
        )
    ''')

    cursor.execute('INSERT INTO historico_cambio VALUES (?, ?, ?)', (data_hora, valor_em_dolares, valor_em_euros))
    conn.commit()
    conn.close()

# Solicita o valor em reais ao usuário
valor_em_reais = float(input("Digite o valor em reais (R$): "))

# Obtém as taxas de câmbio da API
taxas_de_cambio = obter_taxas_de_cambio()

# Converte o valor para dólares e euros
valor_em_dolares, valor_em_euros = converter_moeda(valor_em_reais, taxas_de_cambio)

# Exibe os resultados
print(f"Valor em Dólares (USD): {valor_em_dolares:.2f}")
print(f"Valor em Euros (EUR): {valor_em_euros:.2f}")

# Salva as informações no banco de dados
data_hora = datetime.now()
salvar_no_banco_de_dados(data_hora, valor_em_dolares, valor_em_euros)


# Função para buscar e exibir os dados do banco de dados
def buscar_dados_no_banco():
    conn = sqlite3.connect('historico_cambio.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM historico_cambio')
    dados = cursor.fetchall()

    conn.close()

    if dados:
        for registro in dados:
            data_hora, valor_em_dolares, valor_em_euros = registro
            print(f'Data/Hora: {data_hora}, Valor em Dólares (USD): {valor_em_dolares:.2f}, Valor em Euros (EUR): {valor_em_euros:.2f}')
    else:
        print("Nenhum dado encontrado no banco de dados.")

# Chame a função para buscar e exibir os dados
buscar_dados_no_banco()