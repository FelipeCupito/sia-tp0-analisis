# TP0 SIA - Análisis de Datos con Configuración Modular

Este proyecto evalúa la función de captura de un Pokémon utilizando un sistema de configuración modular que permite ejecutar diferentes experimentos de forma sencilla y reproducible.

## Estructura del Proyecto

* **`src/`**: Contiene la lógica del simulador (`pokemon.py`, `pokeball.py`, `catching.py`).
* **`configs/`**: Directorio para guardar los archivos de configuración de cada experimento.
* **`main.py`**: El script principal que orquesta las simulaciones.
* **`pokemon.json`**: La base de datos con las estadísticas de los Pokémon.
* **`results/`**: Directorio donde se guardarán los archivos CSV con los resultados de las simulaciones.

## ¿Cómo funciona?

El flujo de trabajo se basa en 3 pasos:

1.  **Configurar**: Se crea un archivo `.json` en la carpeta `configs/` que describe el experimento a realizar.
2.  **Ejecutar**: Se corre `main.py` pasándole como argumento la ruta al archivo de configuración.
3.  **Analizar**: El script genera un archivo `.csv` con los datos crudos en la carpeta `results/`. Este archivo puede ser cargado fácilmente en un notebook de Colab o Jupyter para su análisis y visualización.

### El Archivo de Configuración (`config.json`)

El archivo de configuración tiene la siguiente estructura:

```json
{
  "simulation_params": {
    "num_runs": 100,
    "noise": 0.0
  },
  "pokemon_configs": [
    {
      "name": "snorlax",
      "level": 100,
      "hp_percentage": 1.0,
      "status_effect": "none"
    },
    {
      "name": "caterpie",
      "level": 5,
      "hp_percentage": 0.5,
      "status_effect": "sleep"
    }
  ],
  "pokeball_params": {
    "types": ["pokeball", "ultraball", "heavyball"]
  },
  "output_file": "results/mi_experimento.csv"
}
```

**Descripción de los campos:**

* `simulation_params`:
    * `num_runs` (entero): Cuántas veces se ejecutará la simulación `attempt_catch` para **cada** combinación de Pokémon y Pokebola.
    * `noise` (flotante): El nivel de ruido a aplicar en la función de captura (0.0 para un `capture_rate` determinista).

* `pokemon_configs` (lista de objetos):
    * Esta es una lista donde cada objeto define una configuración de un Pokémon a probar.
    * `name` (string): El nombre del Pokémon (debe existir en `pokemon.json`).
    * `level` (entero): El nivel del Pokémon (1-100).
    * `hp_percentage` (flotante): El porcentaje de vida (1.0 = 100%, 0.5 = 50%).
    * `status_effect` (string): El estado de salud. Valores posibles: `poison`, `burn`, `paralysis`, `sleep`, `freeze`, `none`.

* `pokeball_params`:
    * `types` (lista de strings): Una lista con los nombres de las pokebolas a utilizar en el experimento.

* `output_file` (string): La ruta y el nombre del archivo donde se guardarán los resultados. Se recomienda ponerlo dentro de la carpeta `results/`.

### Lógica de Ejecución

El script realizará un producto cartesiano: por **cada objeto** en `pokemon_configs`, probará **cada una** de las `pokeball_params.types`, y cada una de esas combinaciones la correrá `num_runs` veces.

### El Archivo de Salida (`.csv`)

El archivo CSV generado tendrá las siguientes columnas, permitiendo un análisis detallado:

* `run`: El número de la corrida (de 1 a `num_runs`).
* `pokemon_name`: Nombre del Pokémon.
* `level`: Nivel del Pokémon.
* `hp_percentage`: Porcentaje de vida.
* `status_effect`: Estado de salud aplicado.
* `pokeball_type`: Pokebola utilizada.
* `noise`: Nivel de ruido utilizado.
* `success`: `True` si la captura fue exitosa, `False` si no.
* `capture_rate`: La probabilidad de captura calculada en esa corrida.
* `base_catch_rate`: La tasa de captura base del Pokémon (útil para normalizar).
* `weight`: El peso del Pokémon (útil para analizar la HeavyBall).
* `speed`: La velocidad del Pokémon (útil para analizar la FastBall).

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en la carpeta del proyecto, instala las dependencias con:

```sh
pipenv install
```
ó si no se usa pipenv

```sh
pip3 install -r requirements.txt
```


## Ejecución

```sh
pipenv run python main.py configs/template.json
```
ó si no se usa pipenv

```sh
python3 main.py configs/template.json
```

