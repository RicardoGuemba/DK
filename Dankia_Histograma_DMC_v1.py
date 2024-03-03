import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados
file_path = "/Users/ricardohausguembarovski/Desktop/ra.csv"
df = pd.read_csv(file_path)

# Pré-processamento dos dados
df['Tempo de Indexação'] = pd.to_datetime(df['Tempo de Indexação'])
df.set_index('Tempo de Indexação', inplace=True)
codigo_produto = int(input("Digite o código do produto: "))
produto_df = df[df['Cód. Produto'] == codigo_produto]
interval_df = produto_df.resample('1H').sum()
demand_series = interval_df['Quantidade'].fillna(method='ffill')

# Ajustar a série temporal para agrupar os dados em intervalos de 8 horas e somar as quantidades de produtos
intervalos_8h = demand_series.resample('8H').sum()

# Selecionar apenas os dados do período da manhã (das 7h às 12h)
periodo_manha = intervalos_8h.between_time('07:00', '12:00')

# Criar o histograma de frequência
plt.figure(figsize=(10, 6))
periodo_manha.hist(bins=10, color='skyblue', edgecolor='black')
plt.title('Histograma de Frequência - Período da Manhã (7h às 12h)')
plt.xlabel('Quantidade de Produtos')
plt.ylabel('Frequência')
plt.grid(False)
plt.show()
