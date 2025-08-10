import json
import sys
import pandas as pd
from src.pokemon import PokemonFactory, StatusEffect
from src.catching import attempt_catch
import os

def main():
    # --- 1. Cargar Configuración ---
    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print(f"Error: El archivo de configuración '{config_path}' no fue encontrado.")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    # Parámetros de la simulación
    num_runs = config["simulation_params"].get("num_runs", 100)
    noise = config["simulation_params"].get("noise", 0.0)

    # Parámetros de las Pokebolas
    pokeball_types = config["pokeball_params"].get("types", ["pokeball"])

    # Archivo de salida
    output_file = config.get("output_file", "results.csv")
    
    # Asegurarse de que el directorio de salida exista
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Iniciando simulación. Se realizarán {num_runs} corridas por cada configuración.")
    print(f"Los resultados se guardarán en: {output_file}")

    # --- 2. Ejecutar Simulación ---
    factory = PokemonFactory("pokemon.json")
    all_results = []

    # Iterar sobre cada configuración de Pokémon definida en el JSON
    for pkmn_config in config["pokemon_configs"]:
        pokemon_name = pkmn_config["name"]
        level = pkmn_config["level"]
        hp_percentage = pkmn_config["hp_percentage"]
        
        # Convertir string de status a Enum de StatusEffect
        status_str = pkmn_config.get("status_effect", "none").upper()
        status_effect = StatusEffect[status_str]

        print(f"\nProcesando a {pokemon_name.capitalize()} (Lvl: {level}, HP: {hp_percentage*100}%, Estado: {status_effect.name})...")

        # Probar cada tipo de Pokebola con la configuración actual del Pokémon
        for ball in pokeball_types:
            print(f"  Usando {ball.capitalize()}...")
            for run in range(num_runs):
                # Crear la instancia del Pokémon para cada corrida
                pokemon = factory.create(pokemon_name, level, status_effect, hp_percentage)

                # Intentar la captura
                success, capture_rate = attempt_catch(pokemon, ball, noise)

                # Guardar el resultado
                all_results.append({
                    "run": run + 1,
                    "pokemon_name": pokemon_name,
                    "level": level,
                    "hp_percentage": hp_percentage,
                    "status_effect": status_effect.name,
                    "pokeball_type": ball,
                    "noise": noise,
                    "success": success,
                    "capture_rate": capture_rate,
                    "base_catch_rate": pokemon.catch_rate, # Dato útil para análisis
                    "weight": pokemon.weight, # Dato útil para análisis
                    "speed": pokemon.stats.speed # Dato útil para análisis
                })

    # --- 3. Guardar Resultados ---
    if not all_results:
        print("No se generaron resultados. Revisa tu archivo de configuración.")
        return
        
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(output_file, index=False)

    print(f"\n¡Simulación completada! Se guardaron {len(all_results)} registros en '{output_file}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <ruta_al_archivo_config.json>")
    else:
        main()