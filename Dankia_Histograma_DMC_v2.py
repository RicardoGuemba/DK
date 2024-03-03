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

# Ajustar a série temporal para agrupar os dados em intervalos de 6 horas e somar as quantidades de produtos
intervalos_6h = demand_series.resample('6H').sum()

# Criar o histograma de frequência
plt.figure(figsize=(10, 6))
bin_edges = np.arange(intervalos_6h.min(), intervalos_6h.max() + 4, 2)
plt.hist(intervalos_6h, bins=bin_edges, color='skyblue', edgecolor='black')
plt.title('Histograma de Frequência - Intervalo de 6 Horas')
plt.xlabel('Quantidade Total de Produtos')
plt.ylabel('Frequência')
plt.grid(False)
plt.xticks(np.arange(intervalos_6h.min(), intervalos_6h.max() + 2, 2))
plt.show()
