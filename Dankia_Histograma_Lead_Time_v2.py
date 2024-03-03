import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Carregar os dados da planilha
file_path = "/Users/ricardohausguembarovski/Desktop/his_aba.xlsx"
df = pd.read_excel(file_path)

# Calcular o tempo de abastecimento em minutos
df['Últ. Abast. (min)'] = pd.to_timedelta(df['Últ. Abast. (hh:mm:ss)']).dt.total_seconds() / 60

# Calcular parâmetros da distribuição normal
mu, sigma = df['Últ. Abast. (min)'].mean(), df['Últ. Abast. (min)'].std()

# Criar o histograma com distribuição normal
bin_edges = np.linspace(df['Últ. Abast. (min)'].min(), df['Últ. Abast. (min)'].max(), 30)
plt.hist(df['Últ. Abast. (min)'], bins=bin_edges, density=False, alpha=0.6, color='g', edgecolor='black')

# Adicionar linha de melhor ajuste
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, sigma)
plt.plot(x, p * len(df['Últ. Abast. (min)']), 'k', linewidth=2)

plt.title('Histograma com Distribuição Normal (Valores Absolutos)')
plt.xlabel('Tempo de Abastecimento (min)')
plt.ylabel('Frequência Absoluta')
plt.grid(True)
plt.show()

# Calcular estatísticas
tempo_medio = round(df['Últ. Abast. (min)'].mean(), 2)
tempo_maximo = round(df['Últ. Abast. (min)'].max(), 2)
tempo_minimo = round(df['Últ. Abast. (min)'].min(), 2)
desvio_padrao = round(df['Últ. Abast. (min)'].std(), 2)
probabilidade_maior_tempo = round((df['Últ. Abast. (min)'] == df['Últ. Abast. (min)'].max()).mean() * 100, 2)
probabilidade_maior_terceiro_quartil = round((df['Últ. Abast. (min)'] > df['Últ. Abast. (min)'].quantile(0.75)).mean() * 100, 2)

# Exibir estatísticas
print("Tempo Médio de Abastecimento (min):", tempo_medio)
print("Tempo Máximo (min):", tempo_maximo)
print("Tempo Mínimo (min):", tempo_minimo)
print("Desvio Padrão:", desvio_padrao)
print("Probabilidade do Tempo de Abastecimento ser o Maior Tempo (%):", probabilidade_maior_tempo)
print("Probabilidade do Tempo ser Maior que o terceiro quartil Tempo (%):", probabilidade_maior_terceiro_quartil)
