import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


try:
    df = pd.read_csv('results/q1a_pokeball_avg_effectiveness.csv')
except FileNotFoundError:
    print("El archivo de resultados no fue encontrado. Asegúrate de haber ejecutado la simulación.")
else:
    # 1. Calcular la probabilidad de captura para cada combinación (Pokemon, Pokebola)
    prob_df = df.groupby(['pokemon_name', 'pokeball_type'])['success'].mean().reset_index()
    num_runs = df[df['pokeball_type'] == prob_df['pokeball_type'].iloc[0]]['run'].count()
    print(f"Probabilidades de captura calculadas:\n{prob_df}")

    # 2. Calcular el promedio y la desviación estándar POR POKEBOLA
    avg_effectiveness = prob_df.groupby('pokeball_type')['success'].mean()
    std_dev_effectiveness = prob_df.groupby('pokeball_type')['success'].std()
    print (f"\n\nPromedio de efectividad:\n{avg_effectiveness}")
    print (f"\n\nDesviación estándar de efectividad:\n{std_dev_effectiveness}")
    
    # 3. Calcular el Error Estandar de la muetrsa (SEM)
    n_pokemons = prob_df['pokemon_name'].nunique()
    sem_effectiveness = std_dev_effectiveness / np.sqrt(n_pokemons)
    print(f"\n\nError estándar de la muestra (SEM):\n{sem_effectiveness}")

    # 4. Ordenar los resultados para un gráfico más claro
    avg_effectiveness = avg_effectiveness.sort_values(ascending=False)
    std_dev_effectiveness = std_dev_effectiveness.reindex(avg_effectiveness.index)
    sem_effectiveness = sem_effectiveness.reindex(avg_effectiveness.index)

    # 4. Crear el Gráfico
    plt.figure(figsize=(12, 7))
    bars = plt.bar(
        avg_effectiveness.index,
        avg_effectiveness.values,
        yerr=sem_effectiveness.values,
        capsize=5,
    )
    

    # Añadir etiquetas, título y la nota sobre el N
    plt.xlabel('Tipo de Pokebola', fontweight='bold', fontsize=12)
    plt.ylabel('Probabilidad de Captura', fontweight='bold', fontsize=12)
    plt.title(f"Efectividad por Tipo de Pokebola (N={num_runs})", fontsize=18, fontweight='bold')
    plt.ylim(0, 1)

    # Mostrar el gráfico
    plt.show()