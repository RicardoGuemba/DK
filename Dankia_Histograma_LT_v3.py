import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Carregar os dados da planilha
file_path = "/Users/ricardohausguembarovski/Desktop/his_aba.xlsx"
df = pd.read_excel(file_path)

# Calcular o tempo de abastecimento em minutos
df['Últ. Abast. (min)'] = pd.to_timedelta(df['Últ. Abast. (hh:mm:ss)']).dt.total_seconds() / 60

# Remover outliers
Q1 = df['Últ. Abast. (min)'].quantile(0.25)
Q3 = df['Últ. Abast. (min)'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_filtered = df[(df['Últ. Abast. (min)'] >= lower_bound) & (df['Últ. Abast. (min)'] <= upper_bound)]

# Calcular intervalo para os bins
bin_width = 30
min_value = int(df_filtered['Últ. Abast. (min)'].min() // bin_width * bin_width)
max_value = int(np.ceil(df_filtered['Últ. Abast. (min)'].max() / bin_width) * bin_width)

# Criar os bins para o histograma
bins = np.arange(min_value, max_value + bin_width, bin_width)

# Criar o histograma com distribuição normal
plt.hist(df_filtered['Últ. Abast. (min)'], bins=bins, density=False, alpha=0.6, color='g', edgecolor='black')

# Adicionar linha de melhor ajuste
mu, sigma = df_filtered['Últ. Abast. (min)'].mean(), df_filtered['Últ. Abast. (min)'].std()
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, sigma)
plt.plot(x, p * len(df_filtered['Últ. Abast. (min)']) * bin_width, 'k', linewidth=2)

# Adicionar linhas verticais para os quartis
plt.axvline(Q1, color='r', linestyle='--', label='1º Quartil')
plt.axvline(Q3, color='b', linestyle='--', label='3º Quartil')

plt.title('Histograma com Distribuição Normal (Intervalos de 30 minutos, Outliers Removidos)')
plt.xlabel('Tempo de Abastecimento (min)')
plt.ylabel('Frequência Absoluta')
plt.legend()
plt.grid(True)
plt.show()

# Calcular estatísticas
tempo_medio = round(df_filtered['Últ. Abast. (min)'].mean(), 2)
tempo_maximo = round(df_filtered['Últ. Abast. (min)'].max(), 2)
tempo_minimo = round(df_filtered['Últ. Abast. (min)'].min(), 2)
desvio_padrao = round(df_filtered['Últ. Abast. (min)'].std(), 2)
probabilidade_maior_tempo = round((df_filtered['Últ. Abast. (min)'] == df_filtered['Últ. Abast. (min)'].max()).mean() * 100, 2)
probabilidade_maior_terceiro_quartil = round((df_filtered['Últ. Abast. (min)'] > df_filtered['Últ. Abast. (min)'].quantile(0.75)).mean() * 100, 2)

# Exibir estatísticas
print("Tempo Médio de Abastecimento (min):", tempo_medio)
print("Tempo Máximo (min):", tempo_maximo)
print("Tempo Mínimo (min):", tempo_minimo)
print("Desvio Padrão:", desvio_padrao)
print("Probabilidade do Tempo de Abastecimento ser o Maior Tempo (%):", probabilidade_maior_tempo)
print("Probabilidade do Tempo ser Maior que o terceiro quartil Tempo (%):", probabilidade_maior_terceiro_quartil)
