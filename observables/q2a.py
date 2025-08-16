import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from pathlib import Path

try:
    df = pd.read_csv(Path("../results/q2a_result.csv"))
except FileNotFoundError:
    print("El archivo de resultados no fue encontrado. Asegúrate de haber ejecutado la simulación.")
else:
    df.columns = [c.lower().strip() for c in df.columns]
    df["status_effect"] = df["status_effect"].astype(str).str.lower().str.strip().replace({"": "none"})
    df["pokeball_type"] = df["pokeball_type"].astype(str).str.strip()
    df["success"] = df["success"].astype(bool)
    pokemon_name = df["pokemon_name"].iloc[0].title()

    known_order = ["burn", "freeze", "none", "paralysis", "poison", "sleep"]
    status_order = [s for s in known_order if s in set(df["status_effect"])]
    hue_order = sorted(df["pokeball_type"].unique())

    # Compute per-group mean and binomial SE
    stats = (
        df.groupby(["status_effect", "pokeball_type"], as_index=False)["success"]
          .agg(n="size", mean="mean")
    )
    stats["se"] = np.sqrt(stats["mean"] * (1.0 - stats["mean"]) / stats["n"])
    stats["mean_pct"] = stats["mean"] * 100.0
    stats["se_pct"] = stats["se"] * 100.0

    # Weights so hist bars show the MEAN (%) per (status, ball)
    # N per (status, ball) for each row
    n_group = df.groupby(["status_effect", "pokeball_type"]).transform("size")
    df = df.join(n_group.rename("n_group"))
    df["weight_pct"] = df["success"].astype(int) * (100.0 / df["n_group"])

    # Numeric x for discrete histogram bins
    cats = pd.Categorical(df["status_effect"], categories=status_order, ordered=True)
    df["status_code"] = cats.codes

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(
        data=df,
        x="status_code",
        hue="pokeball_type",
        hue_order=hue_order,
        weights="weight_pct",
        multiple="dodge",
        bins=len(status_order),
        discrete=True,
        shrink=0.85,
        stat="count",
        ax=ax
    )

    # Add error bars
    for i, status in enumerate(status_order):
        for j, ball in enumerate(hue_order):
            subset = stats[(stats["status_effect"] == status) & (stats["pokeball_type"] == ball)]
            if not subset.empty:
                x = i + (j - (len(hue_order) - 1) / 2) * 0.85 / len(hue_order)
                ax.errorbar(
                    x=x,
                    y=subset["mean_pct"].values[0],
                    yerr=subset["se_pct"].values[0],
                    fmt='none',
                    ecolor='black',
                    capsize=3,
                    linewidth=1
                )

    sns.move_legend(ax, "upper right", bbox_to_anchor=(1.18, 1),
                    title="Pokeball Type", frameon=True)

    ax.set_xticks(np.arange(len(status_order)))
    ax.set_xticklabels([s.title() for s in status_order], rotation=0)
    ax.yaxis.set_major_formatter(PercentFormatter(100))
    ax.set_xlabel("Status effect", fontsize=15, labelpad=15)
    ax.set_ylabel("Mean success (%)", fontsize=15, labelpad=15)
    ax.set_title(f"Capture Rate by Status Effect\n- {pokemon_name} -",
                   fontsize=16, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.99])
    fig.savefig(f"../results/{pokemon_name}_capture_by_status_mean.png", dpi=200, bbox_inches="tight")
    plt.show()
    print(f"Saved: {pokemon_name}_capture_by_status_mean.png")

    # Heatmap showing pokeball types, status effects, and mean success
    plt.figure(figsize=(10, 6))

    heatmap_data = stats.pivot_table(
        values="mean_pct",
        index="status_effect",
        columns="pokeball_type"
    )

    heatmap_data = heatmap_data.reindex(status_order)
    ax = sns.heatmap(
        heatmap_data,
        annot=True,
        cmap="PuBuGn",
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={'label': 'Mean Success (%)'}
    )

    current_y_labels = ax.get_yticklabels()
    ax.set_yticklabels([label.get_text().title() for label in current_y_labels])
    current_x_labels = ax.get_xticklabels()
    ax.set_xticklabels([label.get_text().title() for label in current_x_labels])

    plt.title(f"Capture Rate by Status Effect\n- {pokemon_name} -",
              fontsize=16, fontweight='bold', pad=20)

    plt.xlabel("Pokeball Type", fontsize=14, labelpad=15)
    plt.ylabel("Status Effect", fontsize=14, labelpad=15)
    plt.tight_layout()
    plt.savefig(f"../results/{pokemon_name}_capture_heatmap.png",
                dpi=200, bbox_inches="tight")
    plt.show()
    print(f"Saved: {pokemon_name}_capture_heatmap.png")
