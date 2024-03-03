import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.linear_model import LinearRegression

# Ler o arquivo series_temporais.csv
file_path = "/Users/ricardohausguembarovski/Desktop/plot_st.csv"
df = pd.read_csv(file_path)

# Função para plotar os gráficos da série temporal, tendência, sazonalidade, resíduo e previsão
def plot_decomposition_with_forecast(df, product_code):
    # Filtrar os dados para o produto específico
    df_product = df[df['Cód. Produto'] == product_code]

    # Converter a coluna Tempo de Indexação para datetime
    df_product['Tempo de Indexação'] = pd.to_datetime(df_product['Tempo de Indexação'])

    # Definir a coluna Tempo de Indexação como índice
    df_product.set_index('Tempo de Indexação', inplace=True)

    # Decompor a série temporal
    decomposition = seasonal_decompose(df_product['Quantidade'], model='additive', period=24*4)  # Período de 24 horas (assumindo que seja diário)

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

    # Define tamanho das fontes na plotagem
    rsaize = 5

    # Plotar os gráficos
    plt.figure(figsize=(12, 15))

    # Série temporal
    plt.subplot(611)
    plt.plot(df_product.index, df_product['Quantidade'], label=f'Dispensário: {df_product["Dispensário"].iloc[0]} / Gaveta: {df_product["Gaveta"].iloc[0]} / Produto: {product_code}', color='blue')
    plt.legend(loc='upper left')
    plt.title('Série Temporal')
    plt.xticks(rotation=30, fontsize=rsaize)
    plt.tight_layout()

    # Tendência
    plt.subplot(612)
    plt.plot(df_product.index, trend_values, label='Tendência', color='green')
    plt.plot(df_product.index, trend_line_values, color='orange', linestyle='--', label='Linha Linear de Tendência')
    plt.legend(loc='upper left')
    plt.title('Tendência')
    plt.xticks(rotation=30, fontsize=rsaize)
    plt.tight_layout()

    # Sazonalidade
    plt.subplot(613)
    plt.plot(decomposition.seasonal.index, decomposition.seasonal, label='Sazonalidade', color='orange')
    plt.legend(loc='upper left')
    plt.title('Sazonalidade')
    plt.xticks(rotation=30, fontsize=rsaize)
    plt.tight_layout()

    # Resíduo
    plt.subplot(614)
    plt.plot(df_product.index, decomposition.resid, label='Resíduo', color='purple')
    plt.legend(loc='upper left')
    plt.title('Resíduo')
    plt.xticks(rotation=30, fontsize=rsaize)
    plt.tight_layout()

    # Estatísticas
    plt.subplot(615)
    plt.text(0.25, 0.8, f'Quantidade de Intervalos: {num_intervals}\nTempo de cada Intervalo: {time_interval}', fontsize=8, ha='center')
    plt.text(0.75, 0.8, f'Máximo: {df_product["Quantidade"].max()}\nMínimo: {df_product["Quantidade"].min()}', fontsize=8, ha='center')
    plt.text(0.25, 0.5, f'Média: {df_product["Quantidade"].mean()}\nDesvio Padrão: {df_product["Quantidade"].std()}', fontsize=8, ha='center')
    plt.axis('off')
    plt.tight_layout()

    # Modelo ARIMA para previsão
    arima_model = ARIMA(df_product['Quantidade'], order=(5, 1, 0))  # Assumindo uma ordem de (5,1,0), você pode ajustar esses valores conforme necessário
    arima_result = arima_model.fit()

    # Previsão dos próximos 24 intervalos
    forecast_values = arima_result.forecast(steps=24)  # Prever os próximos 24 intervalos

    # Construir índice para os intervalos previstos
    forecast_index = pd.date_range(start=df_product.index[-1], periods=25, freq='30T')[1:]  # A partir do próximo intervalo de 30 minutos após o último da série

    # Plotar a previsão
    plt.subplot(616)
    plt.plot(forecast_index, forecast_values, label='Previsão', color='red')
    plt.legend(loc='upper left')
    plt.title('Previsão dos Próximos 24 Intervalos')
    plt.xticks(rotation=30, fontsize=rsaize)
    plt.tight_layout()

    # Exibir os valores previstos
    print("Valores previstos para os próximos 24 intervalos:")
    for i, value in enumerate(forecast_values):
        print(f"Intervalo {i + 1}: {value:.2f}")

    plt.show()

    # Terminar a execução do programa
    import sys
    sys.exit()

# Solicitar o código do produto ao usuário
product_code_input = input("Digite o código do produto: ")

# Plotar os gráficos para o produto especificado
plot_decomposition_with_forecast(df, int(product_code_input))
