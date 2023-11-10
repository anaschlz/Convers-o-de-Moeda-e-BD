import requests
import sqlite3
from datetime import datetime

class CambioManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.conn = sqlite3.connect('historico_cambio.db')
        self.cursor = self.conn.cursor()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_cambio (
                data_hora DATETIME,
                valor_em_dolares REAL,
                valor_em_euros REAL
            )
        ''')
        self.conn.commit()

    def obter_taxas_de_cambio(self):
        url = f'https://api.hgbrasil.com/finance?key={self.api_key}'
        response = requests.get(url)
        data = response.json()
        return data

    def converter_moeda(self, valor_em_reais, taxas_de_cambio):
        dolar = taxas_de_cambio['results']['currencies']['USD']['buy']
        euro = taxas_de_cambio['results']['currencies']['EUR']['buy']
        valor_em_dolares = valor_em_reais / dolar
        valor_em_euros = valor_em_reais / euro
        return valor_em_dolares, valor_em_euros

    def salvar_no_banco_de_dados(self, data_hora, valor_em_dolares, valor_em_euros):
        self.cursor.execute('INSERT INTO historico_cambio VALUES (?, ?, ?)', (data_hora, valor_em_dolares, valor_em_euros))
        self.conn.commit()

    def buscar_dados_no_banco(self):
        self.cursor.execute('SELECT * FROM historico_cambio')
        dados = self.cursor.fetchall()

        if dados:
            for registro in dados:
                data_hora, valor_em_dolares, valor_em_euros = registro
                print(f'Data/Hora: {data_hora}, Valor em Dólares (USD): {valor_em_dolares:.2f}, Valor em Euros (EUR): {valor_em_euros:.2f}')
        else:
            print("Nenhum dado encontrado no banco de dados.")

if __name__ == "__main__":
    api_key = "a11f3a19"
    cambio_manager = CambioManager(api_key)

    valor_em_reais = float(input("Digite o valor em reais (R$): "))

    taxas_de_cambio = cambio_manager.obter_taxas_de_cambio()
    valor_em_dolares, valor_em_euros = cambio_manager.converter_moeda(valor_em_reais, taxas_de_cambio)

    print(f"Valor em Dólares (USD): {valor_em_dolares:.2f}")
    print(f"Valor em Euros (EUR): {valor_em_euros:.2f}")

    data_hora = datetime.now()
    cambio_manager.salvar_no_banco_de_dados(data_hora, valor_em_dolares, valor_em_euros)


    cambio_manager.buscar_dados_no_banco()


    cambio_manager.conn.close()
