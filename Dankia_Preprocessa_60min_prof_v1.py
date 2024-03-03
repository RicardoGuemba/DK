import pandas as pd
from datetime import timedelta

# Passo 1: Leia o arquivo ra1 e crie um DataFrame com todos os dados
file_path = "/Users/ricardohausguembarovski/Desktop/ra.xlsx"
df = pd.read_excel(file_path)

# Passo 2: Converta as datas para o formato datetime e arredonde até o minuto mais próximo, excluindo os segundos
df['Data Hora'] = pd.to_datetime(df['Data Hora'], format='%d/%m/%y %H:%M:%S').dt.floor('min')

# Passo 3: Identifique a menor e a maior data existente nos dados da coluna Data Hora
min_date = df['Data Hora'].min()
max_date = df['Data Hora'].max()

# Passo 4: Verifique os dados das colunas Dispensário, Gaveta, Cód. Produto e conte quantos produtos distintos pertencentes respectivamente a um Dispensário e a uma Gaveta.
num_unique_dispensaries = df['Dispensário'].nunique()
num_unique_drawers = df['Gaveta'].nunique()
num_unique_products = df['Cód. Produto'].nunique()

# Passo 5: Para cada uma das combinações de dados iguais das colunas: Dispensário, Gaveta, Cód. Produto, conte quantos N produtos distintos existem e atribua esta quantidade a variável N.
num_products_per_combination = df.groupby(['Dispensário', 'Gaveta', 'Cód. Produto']).size()

# Passo 6: Crie N Séries Temporais padronizando intervalos de 60 minutos em 60 minutos desde a menor data verificada até a maior data verificada.
interval = 60  # minutos
num_intervals = int(((max_date - min_date).total_seconds() + 1) / (60 * interval))  # +1 para garantir que o último intervalo inclua a última data
time_series_index = pd.date_range(start=min_date, periods=num_intervals, freq=f'{interval}T')

# Passo 7: Para cada uma das séries temporais, totalize as quantidades contidas no intervalo de 60 minutos verificando os dados da coluna Qtde.
time_series_data = []
for idx, group in df.groupby(['Dispensário', 'Gaveta', 'Cód. Produto']):
    dispensary, drawer, product_code = idx
    quantities = []
    index_times = []
    for start_time in time_series_index:
        end_time = start_time + timedelta(minutes=interval)
        quantity = group[(group['Data Hora'] >= start_time) & (group['Data Hora'] < end_time)]['Qtde'].sum()
        quantities.append(quantity)
        index_times.append(start_time + timedelta(minutes=interval / 2))  # Tempo mediano do intervalo
    time_series_data.append({'Dispensário': [dispensary] * num_intervals,
                             'Gaveta': [drawer] * num_intervals,
                             'Cód. Produto': [product_code] * num_intervals,
                             'Tempo de Indexação': index_times,
                             'Quantidade': quantities})

# Concatenar os DataFrames das séries temporais
new_df = pd.concat([pd.DataFrame(d) for d in time_series_data], ignore_index=True)

# Indexação por set_index
new_df.set_index(['Dispensário', 'Gaveta', 'Cód. Produto', 'Tempo de Indexação'], inplace=True)

# Passo 8: Salve o DataFrame em um arquivo CSV
output_file_path = "/Users/ricardohausguembarovski/Desktop/st_60min_profi.csv"
new_df.to_csv(output_file_path)

# Passo 9: Apresentar informações adicionais
print("Data de início da série temporal:", min_date)
print("Data de fim da série temporal:", max_date)
print("Quantidade de séries temporais:", len(time_series_data))
print("Quantidade de intervalos:", num_intervals)
