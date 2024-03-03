Codigo para simular abatecimentos e sinalizar os momentos de abastecimentos
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import math

# Carregar o arquivo CSV
df = pd.read_csv('/Users/ricardohausguembarovski/Desktop/rah.csv')

# Solicitar o código do produto ao usuário
codigo_produto = input("Por favor, insira o código do produto: ")

# Filtrar o dataframe para incluir apenas o produto especificado
df_produto = df[df['Cód. Produto'] == int(codigo_produto)]

# Converter a coluna 'Tempo de Indexação' para o tipo datetime
df_produto['Tempo de Indexação'] = pd.to_datetime(df_produto['Tempo de Indexação'])

# Agrupar os dados por período de 6 horas e somar as quantidades
df_grouped = df_produto.resample('6H', on='Tempo de Indexação').sum().reset_index()

# Calcular a demanda acumulada
df_grouped['Demanda Acumulada'] = df_grouped['Quantidade'].cumsum()

# Identificar o maior valor de demanda totalizado num dos períodos
DMC = df_grouped['Quantidade'].max()

# Calcular a quantidade mínima (Qmin) e a quantidade máxima (Qmax)
Qmin = math.ceil(DMC * (180 / 360))  # Arredondar para o inteiro maior mais próximo
Qmax = int(DMC * 1)

# Calcular a quantidade de abastecimento
abastecimentos = 0
abastecimento_points = []
for i in range(1, len(df_grouped)):
    if df_grouped.iloc[i]['Demanda Acumulada'] >= Qmin:
        abastecimentos += 1
        df_grouped['Demanda Acumulada'][i:] -= Qmax
        abastecimento_points.append(df_grouped.iloc[i]['Tempo de Indexação'])

# Criar a figura e os eixos
fig, ax = plt.subplots(figsize=(10, 6))

# Definir os limites dos eixos x e y
ax.set_xlim(df_grouped['Tempo de Indexação'].min(), df_grouped['Tempo de Indexação'].max())
ax.set_ylim(0, df_grouped['Quantidade'].max())

# Inicializar a linha do gráfico
linha, = ax.plot([], [], lw=2)

# Inicializar as linhas de abastecimento
linhas_abastecimento = []


# Função de inicialização da animação
def init():
    linha.set_data([], [])
    return linha,


# Função de animação
def animate(frame):
    dados_frame = df_grouped.iloc[:frame + 1]  # Selecionar dados até o quadro atual
    linha.set_data(dados_frame['Tempo de Indexação'], dados_frame['Quantidade'])

    # Adicionar as linhas verticais nos momentos de abastecimento
    if frame < abastecimentos:
        if not linhas_abastecimento:
            linhas_abastecimento.append(
                ax.axvline(x=dados_frame.iloc[frame].loc['Tempo de Indexação'], color='r', linestyle='--', linewidth=1))
        else:
            linhas_abastecimento[0].set_xdata(dados_frame.iloc[frame].loc['Tempo de Indexação'])

    # Adicionar marcadores nos pontos de abastecimento
    for point in abastecimento_points[:frame]:
        ax.plot(point, df_grouped[df_grouped['Tempo de Indexação'] == point]['Quantidade'], marker='o', markersize=5,
                color='red')

    return linha,


# Calcular o número total de quadros na animação
num_frames = len(df_grouped)

# Criar a animação
ani = FuncAnimation(fig, animate, frames=num_frames, init_func=init, blit=True,
                    interval=1000)  # Intervalo em milissegundos (1 segundo)

plt.xlabel('Tempo')
plt.ylabel('Quantidade')
plt.title(f'Demanda do Produto {codigo_produto} ao Longo do Tempo')
plt.xticks(rotation=45)
plt.tight_layout()

# Exibir informações adicionais
plt.text(0.01, 0.9, f'DMC: {DMC}\nQmin: {Qmin}\nQmax: {Qmax}\nAbastecimentos: {abastecimentos}',
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')

plt.show()
