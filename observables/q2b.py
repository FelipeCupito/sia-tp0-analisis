import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from pathlib import Path
import numpy as np

try:
    df = pd.read_csv(Path("../results/q2b_hp_effect.csv"))
except FileNotFoundError:
    print("Results file not found. Make sure you've run the simulation first.")
    exit()

df.columns = [c.lower().strip() for c in df.columns]
df["pokeball_type"] = df["pokeball_type"].astype(str).str.strip().str.capitalize()
df["pokemon_name"] = df["pokemon_name"].str.capitalize()

group_cols = ["pokemon_name", "pokeball_type", "hp_percentage"]
if "level" in df.columns:
    group_cols.append("level")

grouped = df.groupby(group_cols)["capture_rate"]
summary = grouped.agg(['mean', 'count', 'std']).reset_index()
summary["capture_rate_std"] = summary["std"] / np.sqrt(summary["count"])
summary = summary.rename(columns={"mean": "capture_rate"})

# debug
print("Standard Error Statistics:")
print(f"Min: {summary['capture_rate_std'].min()}")
print(f"Max: {summary['capture_rate_std'].max()}")
print(f"Mean: {summary['capture_rate_std'].mean()}")

pokemon_names = summary["pokemon_name"].unique()
palette = sns.color_palette("tab10", n_colors=summary["pokeball_type"].nunique())
pokeball_types = summary["pokeball_type"].unique()
color_map = dict(zip(pokeball_types, palette))

for pokemon_name in pokemon_names:
    df_pokemon = summary[summary["pokemon_name"] == pokemon_name]
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")

    g = sns.lineplot(
        data=df_pokemon,
        x="hp_percentage",
        y="capture_rate",
        hue="pokeball_type",
        style="pokeball_type",
        markers=True,
        dashes=False,
        linewidth=2.5,
        markersize=8,
        palette=color_map,
        errorbar=None
    )

    for pokeball_type, group in df_pokemon.groupby("pokeball_type"):
        plt.errorbar(
            group["hp_percentage"],
            group["capture_rate"],
            yerr=group["capture_rate_std"],
            fmt='none',
            capsize=5,
            elinewidth=2.0,
            label=None,
            color=color_map[pokeball_type],
            alpha=0.8,
            zorder=20
        )

    g.set_xlabel("HP %", fontsize=17, labelpad=15)
    g.set_ylabel("Capture Rate", fontsize=17, labelpad=15)
    g.set_title("Effect of HP % on Capture Rate", fontsize=16, fontweight='bold', pad=30, loc='center')
    g.xaxis.set_major_formatter(PercentFormatter(1.0))
    g.yaxis.set_major_formatter(PercentFormatter(1.0))

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title="Pokeball Type", bbox_to_anchor=(1, 1), loc="upper right", fontsize=15)
    pokemon_level = df_pokemon["level"].iloc[0] if "level" in df_pokemon.columns and not df_pokemon["level"].empty else "Unknown"
    pokemon_info = f"{pokemon_name} (Level {pokemon_level})"
    plt.figtext(0.5, 0.94, pokemon_info, fontsize=15, ha="center", va="top", bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    output_path = f"../results/{pokemon_name}_{pokemon_level}_hp_effect.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.show()
    print(f"Saved: {output_path}")