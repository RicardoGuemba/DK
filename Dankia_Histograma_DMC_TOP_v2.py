import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados
file_path = "/Users/ricardohausguembarovski/Desktop/rah.csv"
df = pd.read_csv(file_path)

# Pré-processamento dos dados
df['Tempo de Indexação'] = pd.to_datetime(df['Tempo de Indexação'])
df.set_index('Tempo de Indexação', inplace=True)

# Solicitar o código do produto
codigo_produto = int(input("Digite o código do produto: "))

# Filtrar os dados apenas para o produto informado
produto_df = df[df['Cód. Produto'] == codigo_produto]

# Filtrar os dados apenas para o intervalo de tempo entre 6 e 12 horas
periodo_manha_df = produto_df.between_time('6:00', '12:00')

# Calcular todos os totais de produtos demandados nos períodos da manhã
totais_manha = periodo_manha_df.resample('6H').sum()

# Verificar se existem dados disponíveis
if not totais_manha.empty:
    # Calcular a quantidade total de intervalos de 6 horas
    total_intervalos = len(totais_manha)

    # Calcular a quantidade máxima de produtos totalizada no período
    quantidade_maxima = totais_manha['Quantidade'].max()

    # Calcular a média das quantidades de produtos demandados
    media_quantidades = periodo_manha_df['Quantidade'].mean()

    # Calcular o desvio padrão das quantidades de produtos demandados
    desvio_padrao = periodo_manha_df['Quantidade'].std()

    # Calcular a probabilidade de ocorrer a quantidade máxima consecutiva
    frequencia_maximo = (totais_manha['Quantidade'] == quantidade_maxima).sum()
    probabilidade_maximo_consecutivo = frequencia_maximo / total_intervalos

    # Calcular o terceiro quartil como a soma das quantidades acima do percentil 75
    quantidades_ordenadas = sorted(periodo_manha_df['Quantidade'])
    indice_quartil_75 = int(0.75 * len(quantidades_ordenadas))
    terceiro_quartil = sum(quantidades_ordenadas[indice_quartil_75:]) / total_intervalos

    # Calcular a probabilidade da quantidade ser maior que o terceiro quartil
    frequencia_terceiro_quartil = (periodo_manha_df['Quantidade'] > terceiro_quartil).sum()
    probabilidade_terceiro_quartil = frequencia_terceiro_quartil / total_intervalos

    # Encontrar o intervalo com maior frequência demandada
    frequencia_histograma, intervalos_histograma = np.histogram(totais_manha['Quantidade'], bins='auto')
    indice_maior_frequencia = np.argmax(frequencia_histograma)
    demanda_maior_frequencia = frequencia_histograma[indice_maior_frequencia]

    # Calcular a probabilidade de ocorrer a demanda mais frequente
    probabilidade_demanda_mais_frequente = (demanda_maior_frequencia / total_intervalos) * 100

    # Calcular a demanda relacionada ao maior intervalo do histograma
    demanda_relacionada = (demanda_maior_frequencia / total_intervalos)

    # Apresentar os resultados
    print("Quantidade de intervalos considerados:", total_intervalos)
    print("Quantidade máxima de produtos totalizada no período:", quantidade_maxima)
    print("Média das quantidades de produtos demandados:", media_quantidades)
    print("Desvio Padrão das quantidades de produtos:", desvio_padrao)
    print("Probabilidade de ocorrer a quantidade máxima consecutiva:", "{:.2f}%".format(probabilidade_maximo_consecutivo * 100))
    print("Probabilidade da quantidade ser maior que o terceiro quartil:", "{:.2f}%".format(probabilidade_terceiro_quartil * 100))
    print("Demanda relacionada à maior probabilidade de ocorrer (un):", demanda_relacionada)
    print("Probabilidade de Ocorrer a Demanda mais Frequente (%):", "{:.2f}%".format(probabilidade_demanda_mais_frequente))

    # Plotar a série temporal
    plt.figure(figsize=(12, 6))
    plt.plot(periodo_manha_df.index, periodo_manha_df['Quantidade'], color='blue')
    plt.title('Série Temporal de Quantidade de Produtos (Períodos da Manhã)')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de Produtos')
    plt.grid(True)
    plt.show()

    # Plotar o histograma
    plt.figure(figsize=(10, 6))
    # Especificar os limites dos bins para incluir todos os valores de demanda
    bin_edges = np.arange(0, totais_manha['Quantidade'].max() + 2, 1)
    plt.hist(totais_manha['Quantidade'], bins=bin_edges, color='skyblue', edgecolor='black', density=False)
    plt.title('Histograma de Frequência - Intervalo de 6 Horas (Períodos da Manhã)')
    plt.xlabel('Quantidade Total de Produtos (Manhã)')
    plt.ylabel('Frequência')

    # Calcular o valor médio de cada intervalo e exibi-lo como rótulo no gráfico
    for i in range(len(frequencia_histograma)):
        valor_medio = (intervalos_histograma[i] + intervalos_histograma[i+1]) / 2
        plt.text(valor_medio, frequencia_histograma[i] + 0.5, str(frequencia_histograma[i]), ha='center')

    # Exibir o valor máximo no histograma
    plt.axvline(x=quantidade_maxima, color='red', linestyle='--', linewidth=1)

    plt.grid(False)
    plt.show()
else:
    print("Não há dados disponíveis para análise.")
