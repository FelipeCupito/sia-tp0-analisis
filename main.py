import json
import sys
import pandas as pd
from src.pokemon import PokemonFactory, StatusEffect
from src.catching import attempt_catch
import os
import math
from itertools import product

EPS = 1e-9

def _to_list(value):
    """
    Expand a JSON field that may be:
      - a single value
      - {"set": [...]}
      - {"range": {"start": x, "end": y, "step": s}}
      - {"linspace": {"start": x, "end": y, "num": n}}
    Returns a Python list of concrete values.
    """
    if not isinstance(value, dict):
        return [value]  # single value (backward compatible)

    if "set" in value:
        return list(value["set"])

    if "range" in value:
        r = value["range"]
        start, end, step = float(r["start"]), float(r["end"]), float(r["step"])
        out = []
        v = start
        # include end (with tolerance) to avoid floating point drift
        while v <= end + EPS:
            out.append(round(v, 10))
            v += step
        return out

    if "linspace" in value:
        ls = value["linspace"]
        start, end, num = float(ls["start"]), float(ls["end"]), int(ls["num"])
        if num <= 1:
            return [start]
        step = (end - start) / (num - 1)
        return [round(start + i * step, 10) for i in range(num)]

    raise ValueError(f"Unsupported collection spec: {value}")

def expand_pokemon_config(pkm):
    """
    Given a single pokemon config possibly containing sets/ranges,
    return a list of concrete configs (Cartesian product).
    Always returns concrete primitives for level/hp_percentage/status_effect.
    """
    name = pkm["name"]
    levels = _to_list(pkm.get("level", 50))
    hp_values = _to_list(pkm.get("hp_percentage", 1.0))
    statuses = _to_list(pkm.get("status_effect", "none"))

    expanded = []
    for lvl, hp, st in product(levels, hp_values, statuses):
        expanded.append({
            "name": name,
            "level": int(lvl),
            "hp_percentage": float(hp),
            "status_effect": str(st)
        })
    return expanded


def main():
    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print(f"Error: El archivo de configuración '{config_path}' no fue encontrado.")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    num_runs = config["simulation_params"].get("num_runs", 100)
    noise = config["simulation_params"].get("noise", 0.0)

    pokeball_types = config["pokeball_params"].get("types", ["pokeball"])

    output_file = config.get("output_file", "results.csv")
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Iniciando simulación. Se realizarán {num_runs} corridas por cada configuración.")
    print(f"Los resultados se guardarán en: {output_file}")

    factory = PokemonFactory("pokemon.json")
    all_results = []

    for pkmn_cfg in config["pokemon_configs"]:
        for concrete in expand_pokemon_config(pkmn_cfg):
            pokemon_name = concrete["name"]
            level = concrete["level"]
            hp_percentage = concrete["hp_percentage"]

            status_str = str(concrete.get("status_effect", "none")).upper()
            status_effect = StatusEffect[status_str]

            print(f"\nProcesando {pokemon_name.capitalize()} "
                  f"(Lvl: {level}, HP: {hp_percentage * 100:.0f}%, Estado: {status_effect.name})...")

            pokemon = factory.create(pokemon_name, level, status_effect, hp_percentage)
            for ball in pokeball_types:
                print(f"  Usando {ball.capitalize()}...")
                for run in range(num_runs):
                    success, capture_rate = attempt_catch(pokemon, ball, noise)
                    all_results.append({
                        "run": run + 1,
                        "pokemon_name": pokemon_name,
                        "level": level,
                        "hp_percentage": hp_percentage,
                        "status_effect": status_effect.name,
                        "pokeball_type": ball,
                        "noise": noise,
                        "success": bool(success),
                        "capture_rate": capture_rate,
                        "base_catch_rate": pokemon.catch_rate,
                        "weight": pokemon.weight,
                        "speed": pokemon.stats.speed
                    })

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