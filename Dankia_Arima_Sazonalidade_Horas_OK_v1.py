import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from itertools import product
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression

# Carregar dados
file_path = "/Users/ricardohausguembarovski/Desktop/ra.csv"
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

# Verificar se a série temporal é estacionária usando o teste de Dickey-Fuller aumentado (ADF)
def adf_test(timeseries):
    result = adfuller(timeseries)
    print('Estatísticas ADF:', result[0])
    print('Valor-p:', result[1])
    print('Valores críticos:')
    for key, value in result[4].items():
        print('\t', key, ':', value)
    if result[1] > 0.05:
        print("A série temporal não é estacionária.")
        # Aplicar método para tornar a série estacionária, se necessário
    else:
        print("A série temporal é estacionária.")

adf_test(demand_series)

# Executar decomposição sazonal da série temporal
decomposition = seasonal_decompose(demand_series, model='additive', period=24)

# Extrair os componentes
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Ajustar uma linha de tendência linear aos dados de tendência
x = np.arange(len(trend))
y = trend.values
nan_mask = ~np.isnan(y)
if np.any(nan_mask):
    regression_model = LinearRegression().fit(x.reshape(-1, 1)[nan_mask], y.reshape(-1, 1)[nan_mask])
    trend_line_values = regression_model.predict(np.arange(len(x)).reshape(-1, 1))
else:
    trend_line_values = np.zeros_like(x)

# Plotar a série temporal e os componentes (tendência, sazonalidade e resíduo)
plt.figure(figsize=(12, 10))

# Série Temporal
plt.subplot(411)
plt.plot(demand_series.index, demand_series, label=f'Dispensário: {produto_df["Dispensário"].iloc[0]} / Gaveta: {produto_df["Gaveta"].iloc[0]} / Produto: {codigo_produto}', color='blue')
plt.xlabel('Dia e Hora')
plt.ylabel('Demanda')
plt.title(f'Série Temporal e Componentes para o Produto {codigo_produto}')
plt.legend()

# Tendência com a reta
plt.subplot(412)
plt.plot(trend.index, trend, label='Tendência', color='green')
plt.plot(trend.index, trend_line_values, color='orange', linestyle='--', label='Reta de Tendência')
plt.xlabel('Dia e Hora')
plt.ylabel('Tendência')
plt.legend()

# Sazonalidade
plt.subplot(413)
plt.plot(seasonal.index, seasonal, label='Sazonalidade', color='orange')
plt.xlabel('Dia e Hora')
plt.ylabel('Sazonalidade')
plt.legend()

# Resíduo
plt.subplot(414)
plt.plot(residual.index, residual, label='Resíduo', color='purple')
plt.xlabel('Dia e Hora')
plt.ylabel('Resíduo')
plt.legend()

plt.tight_layout()
plt.show()

# Suprimir avisos durante o processamento
warnings.filterwarnings("ignore")

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

# Ajustar o modelo ARIMA com os melhores parâmetros encontrados
model = ARIMA(demand_series, order=best_pdq)
model_fit = model.fit()

# Fazer previsões para os próximos 24 intervalos
forecast = model_fit.forecast(steps=24)

# Plotar a série temporal e a previsão
plt.figure(figsize=(10, 6))
plt.plot(demand_series, label='Série Temporal', color='blue')
plt.plot(interval_df.index[-1] + pd.to_timedelta(np.arange(1, 25), unit='H'), forecast, color='red', linestyle='--', label='Previsão')
plt.xlabel('Dia e Hora')
plt.ylabel('Demanda')
plt.title(f'Série Temporal e Previsão de Demanda para o Produto {codigo_produto}')
plt.legend()
plt.show()

# Apresentar os valores previstos de demanda
print("Valores previstos de demanda e respectivo dia e hora:")
for i, value in enumerate(forecast):
    forecast_time = interval_df.index[-1] + pd.to_timedelta(i + 1, unit='H')
    print(f"Dia {forecast_time.date()} Hora {forecast_time.hour}: {int(value)}")
