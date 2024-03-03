import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
from sklearn.linear_model import LinearRegression

# Ler o arquivo series_temporais.csv
file_path = "/Users/ricardohausguembarovski/Desktop/plot_st.csv"
df = pd.read_csv(file_path)

# Função para plotar os gráficos da série temporal, tendência, sazonalidade e resíduo
def plot_decomposition(df, product_code):
    # Filtrar os dados para o produto específico
    df_product = df[df['Cód. Produto'] == product_code]

    # Converter a coluna Tempo de Indexação para datetime
    df_product['Tempo de Indexação'] = pd.to_datetime(df_product['Tempo de Indexação'])

    # Definir a coluna Tempo de Indexação como índice
    df_product.set_index('Tempo de Indexação', inplace=True)

    # Decompor a série temporal
    decomposition = seasonal_decompose(df_product['Quantidade'], model='additive', period=24)  # Período de 24 horas (assumindo que seja diário)

    # Ajustar uma linha de tendência linear aos dados
    trend_values = decomposition.trend
    x = np.arange(len(trend_values))
    y = trend_values.values
    nan_mask = ~np.isnan(y)
    model = LinearRegression().fit(x.reshape(-1, 1)[nan_mask], y.reshape(-1, 1)[nan_mask])
    trend_line_values = model.predict(np.arange(len(x)).reshape(-1, 1))

    # Calculando a quantidade de intervalos da série e o tempo de cada intervalo
    num_intervals = len(df_product)
    time_interval = (df_product.index[-1] - df_product.index[0]) / num_intervals

    # Plotar os gráficos
    plt.figure(figsize=(12, 15))

    # Série temporal
    plt.subplot(511)
    plt.plot(df_product.index, df_product['Quantidade'], label=f'Série Temporal - Produto {product_code}', color='blue')
    plt.legend(loc='upper left')
    plt.title('Série Temporal')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Tendência
    plt.subplot(512)
    plt.plot(df_product.index, trend_values, label='Tendência', color='green')
    plt.plot(df_product.index, trend_line_values, color='orange', linestyle='--', label='Linha Linear de Tendência')
    plt.legend(loc='upper left')
    plt.title('Tendência')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Sazonalidade
    plt.subplot(513)
    plt.plot(df_product.index, decomposition.seasonal, label='Sazonalidade', color='orange')
    plt.legend(loc='upper left')
    plt.title('Sazonalidade')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Resíduo
    plt.subplot(514)
    plt.plot(df_product.index, decomposition.resid, label='Resíduo', color='purple')
    plt.legend(loc='upper left')
    plt.title('Resíduo')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Estatísticas
    plt.subplot(515)
    plt.text(0.5, 0.5, f'Quantidade de Intervalos: {num_intervals}', fontsize=8, ha='center', va='center')
    plt.text(0.5, 0.4, f'Tempo de cada Intervalo: {time_interval}', fontsize=8, ha='center', va='center')
    plt.text(0.5, 0.3, f'Máximo: {df_product["Quantidade"].max()}', fontsize=8, ha='center', va='center')
    plt.text(0.5, 0.2, f'Mínimo: {df_product["Quantidade"].min()}', fontsize=8, ha='center', va='center')
    plt.text(0.5, 0.1, f'Média: {df_product["Quantidade"].mean()}', fontsize=8, ha='center', va='center')
    plt.text(0.5, 0.0, f'Desvio Padrão: {df_product["Quantidade"].std()}', fontsize=8, ha='center', va='center')
    plt.axis('off')
    plt.tight_layout()

    plt.show()

    # Terminar a execução do programa
    import sys
    sys.exit()

# Solicitar o código do produto ao usuário
product_code_input = input("Digite o código do produto: ")

# Plotar os gráficos para o produto especificado
plot_decomposition(df, int(product_code_input))
