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

    plt.figure()
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

    #Heavy ball analysis
    # First, calculate success rates for each pokemon and ball type
    success_rates = df.groupby(['pokemon_name', 'pokeball_type'])['success'].mean().reset_index()
    # Pivot to get Heavy Ball and Pokéball success rates side by side
    pivoted = success_rates.pivot(index='pokemon_name', columns='pokeball_type', values='success').reset_index()
    # Calculate the ratio (Heavy Ball success / Pokéball success)
    pivoted['success_ratio'] = pivoted['heavyball'] / pivoted['pokeball']
    # Get weight for each pokemon (assuming it's fixed per pokemon)
    weights = df.drop_duplicates('pokemon_name')[['pokemon_name', 'weight']]

    # Merge the data
    plot_data = pd.merge(pivoted[['pokemon_name', 'success_ratio']], weights, on='pokemon_name')
    # Sort by weight for better visualization (optional)
    plot_data = plot_data.sort_values('weight')

    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=(12, 6))
    # Bar plot for success ratio on primary axis
    sns.barplot(data=plot_data, x='pokemon_name', y='success_ratio', 
                color='blue', alpha=0.7, ax=ax1)
    ax1.set_title('Pokémon Capture Success Ratio (Heavy Ball/Poké Ball) and Weight')
    ax1.set_xlabel('Pokémon')
    ax1.set_ylabel('Success Ratio (Heavy/Poké)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.axhline(1, linestyle='--', color='black', label='Pokeball reference')

    # Create secondary axis
    ax2 = ax1.twinx()
    # Line plot for weight on secondary axis
    sns.lineplot(data=plot_data, x='pokemon_name', y='weight', 
                color='red', marker='o', ax=ax2, linewidth=2.5)
    ax2.set_ylabel('Weight', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Rotate x-labels
    plt.xticks(rotation=45)
    # Add legend
    ax1.legend()
    ax2.legend(['Weight'], loc='upper right')
    plt.tight_layout()
    plt.show()

    prob_df = df.groupby(['pokemon_name', 'pokeball_type'])['success'].mean().reset_index()
    print(f"\nValores absolutos:\n{prob_df[['pokemon_name', 'pokeball_type', 'success']]}")

    #Fast ball analysis
    # Pivot to get Fast Ball and Pokéball success rates side by side
    pivoted = success_rates.pivot(index='pokemon_name', columns='pokeball_type', values='success').reset_index()
    # Calculate the ratio (Heavy Ball success / Pokéball success)
    pivoted['success_ratio'] = pivoted['fastball'] / pivoted['pokeball']
    # Get weight for each pokemon (assuming it's fixed per pokemon)
    weights = df.drop_duplicates('pokemon_name')[['pokemon_name', 'speed']]

    # Merge the data
    plot_data = pd.merge(pivoted[['pokemon_name', 'success_ratio']], weights, on='pokemon_name')
    # Sort by weight for better visualization (optional)
    plot_data = plot_data.sort_values('speed')

    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=(12, 6))
    # Bar plot for success ratio on primary axis
    sns.barplot(data=plot_data, x='pokemon_name', y='success_ratio', 
                color='blue', alpha=0.7, ax=ax1)
    ax1.set_title('Pokémon Capture Success Ratio (Fast Ball/Poké Ball) and Speed')
    ax1.set_xlabel('Pokémon')
    ax1.set_ylabel('Success Ratio (Fast/Poké)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.axhline(1, linestyle='--', color='black', label='Pokeball reference')

    # Create secondary axis
    ax2 = ax1.twinx()
    # Line plot for weight on secondary axis
    sns.lineplot(data=plot_data, x='pokemon_name', y='speed', 
                color='red', marker='o', ax=ax2, linewidth=2.5)
    ax2.set_ylabel('Speed', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Rotate x-labels
    plt.xticks(rotation=45)
    # Add legend
    ax1.legend()
    ax2.legend(['Speed'], loc='upper right')
    plt.tight_layout()
    plt.show()
