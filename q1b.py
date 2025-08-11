import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --- 1. Cargar y Preparar los Datos ---
try:
    df = pd.read_csv('results/q1a_pokeball_avg_effectiveness.csv')
except FileNotFoundError:
    print("El archivo de resultados no fue encontrado. Asegúrate de haber ejecutado la simulación de la pregunta 1a.")
else:
    
    # 1. Calculamos la probabilidad de éxito de cada combinación (Pokemon, Pokebola)
    prob_df = df.groupby(['pokemon_name', 'pokeball_type'])['success'].mean().reset_index()
    num_runs = df[df['pokeball_type'] == prob_df['pokeball_type'].iloc[0]]['run'].count()

    # 2. Normalización: 
    # calculamos la efectividad de la pokebola base (Pokeball) para cada Pokémon.
    base_effectiveness = prob_df[prob_df['pokeball_type'] == 'pokeball'] \
                            .set_index('pokemon_name')['success']
    
    # agregamos el dato anterior al DataFrame de probabilidades
    prob_df['base_success'] = prob_df['pokemon_name'].map(base_effectiveness)

    # Calculamos el Ratio de Efectividad.
    prob_df['effectiveness_ratio'] = (prob_df['success'] / prob_df['base_success']).fillna(1)

    # Sacamos las filas de la pokebola base
    special_balls_df = prob_df[prob_df['pokeball_type'] != 'pokeball']
    print(f"\nEfectividad normalizada de Pokebolas:\n{special_balls_df[['pokemon_name', 'pokeball_type', 'effectiveness_ratio', 'success', 'base_success']]}")

    # 3. Graficamos los resultados:
    plt.figure(figsize=(14, 8))
    sns.barplot(
        x='pokemon_name',
        y='effectiveness_ratio',
        hue='pokeball_type',
        data=special_balls_df,
    )

    plt.axhline(y=1, color='gray', linestyle='--', linewidth=2, label='Efectividad de PokeBall Base') # Añadimos una línea de referencia en y=1.
    plt.xlabel('Pokémon', fontweight='bold', fontsize=12)
    plt.ylabel('Ratio de Efectividad (Mejora vs. PokeBall)', fontweight='bold', fontsize=12)
    plt.title(f"Efectividad Normalizada de Pokebolas por Pokémon (N={num_runs}):", fontsize=18, fontweight='bold')
    plt.legend(title='Tipo de Pokebola')
    
    plt.show()