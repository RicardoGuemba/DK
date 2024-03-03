import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Ler o arquivo series_temporais.csv
file_path = "/Users/ricardohausguembarovski/Desktop/plot_st.csv"
df = pd.read_csv(file_path)


# Função para plotar os gráficos da série temporal com as previsões dos próximos 24 intervalos
def plot_with_forecast(df, product_code):
    # Filtrar os dados para o produto específico
    df_product = df[df['Cód. Produto'] == product_code]

    # Converter a coluna Tempo de Indexação para datetime
    df_product['Tempo de Indexação'] = pd.to_datetime(df_product['Tempo de Indexação'])

    # Definir a coluna Tempo de Indexação como índice
    df_product.set_index('Tempo de Indexação', inplace=True)

    # Plotar a série temporal
    plt.figure(figsize=(10, 6))
    plt.plot(df_product.index, df_product['Quantidade'],
             label=f'Dispensário: {df_product["Dispensário"].iloc[0]} / Gaveta: {df_product["Gaveta"].iloc[0]} / Produto: {product_code}',
             color='blue')

    # Ajustar o modelo ARIMA
    arima_model = ARIMA(df_product['Quantidade'], order=(
    6, 1, 1))  # Assumindo uma ordem de (5,1,0), você pode ajustar esses valores conforme necessário
    arima_result = arima_model.fit()

    # Prever os próximos 24 intervalos
    forecast_values = arima_result.forecast(steps=24)

    # Construir índice para os intervalos previstos
    forecast_index = pd.date_range(start=df_product.index[-1], periods=25, freq='30T')[1:]

    # Plotar as previsões
    plt.plot(forecast_index, forecast_values, label='Previsão', color='red')

    plt.legend(loc='upper left')
    plt.title('Série Temporal com Previsões dos Próximos 24 Intervalos')
    plt.xlabel('Tempo de Indexação')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


# Solicitar o código do produto ao usuário
product_code_input = input("Digite o código do produto: ")

# Plotar os gráficos para o produto especificado
plot_with_forecast(df, int(product_code_input))
