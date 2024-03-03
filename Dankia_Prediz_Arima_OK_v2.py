import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from itertools import product
import warnings
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_absolute_error

# Carregar dados
file_path = "/Users/ricardohausguembarovski/Desktop/plot_st.csv"
df = pd.read_csv(file_path)

# Converter a coluna 'Tempo de Indexação' para datetime e definir como índice
df['Tempo de Indexação'] = pd.to_datetime(df['Tempo de Indexação'])
df.set_index('Tempo de Indexação', inplace=True)

# Solicitar o código do produto
codigo_produto = int(input("Digite o código do produto: "))

# Filtrar os dados para o produto selecionado
produto_df = df[df['Cód. Produto'] == codigo_produto]

# Agrupar os dados por intervalo de tempo e calcular a quantidade total
interval_df = produto_df.resample('1H').sum()

# Criar a série temporal de demanda
demand_series = interval_df['Quantidade']

# Verificar se a série temporal é estacionária
def check_stationarity(timeseries):
    # Teste de Dickey-Fuller aumentado (ADF test)
    result = adfuller(timeseries)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))
    if result[1] > 0.05:
        print("A série temporal não é estacionária. Aplicando diferenciação...")
        # Aplicar diferenciação para tornar a série temporal estacionária
        differenced_series = timeseries.diff().dropna()
        return differenced_series
    else:
        print("A série temporal é estacionária.")
        return timeseries

# Definir a grade de parâmetros para busca em grade
p = d = q = range(0, 3)
pdq = list(product(p, d, q))

# Executar busca em grade para encontrar os melhores parâmetros
best_aic = np.inf
best_pdq = None
for param in pdq:
    try:
        model = ARIMA(demand_series, order=param)
        model_fit = model.fit()

        if model_fit.aic < best_aic:
            best_aic = model_fit.aic
            best_pdq = param
    except:
        continue

# Exibir os melhores parâmetros encontrados
print(f"Melhores parâmetros encontrados: ARIMA{best_pdq}")

# Ajustar o modelo ARIMA com os melhores parâmetros encontrados
model = ARIMA(demand_series, order=best_pdq)
model_fit = model.fit()

# Fazer previsões para os próximos 24 intervalos
forecast = model_fit.forecast(steps=24)

# Arredondar os valores previstos para o valor inteiro mais próximo
forecast_rounded = np.round(forecast)

# Plotar a série temporal e a previsão
plt.figure(figsize=(10, 6))
plt.plot(demand_series, label='Série Temporal')
plt.plot(interval_df.index[-1] + pd.to_timedelta(np.arange(1, 25), unit='H'), forecast_rounded, color='red', linestyle='--', label='Previsão')
plt.xlabel('Dia e Hora')
plt.ylabel('Demanda')
plt.title(f'Série Temporal e Previsão de Demanda para o Produto {codigo_produto}')
plt.legend()
plt.show()

# Calcular o erro médio absoluto
mae = mean_absolute_error(demand_series[-24:], forecast_rounded)
print(f"Erro Médio Absoluto: {mae}")

# Exibir estatísticas da série temporal
print("\nEstatísticas da Série Temporal:")
print(f"Máximo: {demand_series.max()}")
print(f"Mínimo: {demand_series.min()}")
print(f"Média: {demand_series.mean()}")
print(f"Desvio Padrão: {demand_series.std()}")
print(f"Tempo do Intervalo: 1 hora")
print(f"Número de Intervalos: {len(demand_series)}")

# Apresentar os valores previstos de demanda
print("\nValores previstos de demanda (arredondados para o valor inteiro mais próximo) e respectivo dia e hora:")
for i, value in enumerate(forecast_rounded):
    forecast_time = interval_df.index[-1] + pd.to_timedelta(i + 1, unit='H')
    print(f"Dia {forecast_time.date()} Hora {forecast_time.hour}: {int(value)}")
