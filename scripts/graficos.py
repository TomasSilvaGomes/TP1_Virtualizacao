import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =====================================================================
# Configurações Globais de Estilo (Visual Clean e Científico - IEEE)
# =====================================================================
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
        "axes.axisbelow": True,  # CORREÇÃO: "axes.axisbelow" em vez de "axes.set_axisbelow"
    }
)

# Dicionários de normalização para cores e nomes
CORES = ["#4A72B0", "#DD8452", "#55A868"]
NOMES_PLOT = ["Host Nativo", "KVM (Tipo 1)", "VirtualBox (Tipo 2)"]
ORDEM_ENV = ["host", "kvm", "virtualbox"]
ORDEM_ENV_PT = ["Host Nativo", "KVM (Tipo 1)", "VirtualBox (Tipo 2)"]


def plot_cpu_ram():
    """Gera o Gráfico de CPU e RAM a partir de cpu.csv e ram.csv"""
    print("A processar CPU e RAM...")

    try:
        # ATENÇÃO: Confirma se os teus ficheiros estão na pasta 'csvs/' ou na mesma pasta do script
        caminho_cpu = "csvs/cpu.csv" if os.path.exists("csvs/cpu.csv") else "cpu.csv"
        caminho_ram = "csvs/ram.csv" if os.path.exists("csvs/ram.csv") else "ram.csv"

        df_cpu = pd.read_csv(caminho_cpu).set_index("Environment").reindex(ORDEM_ENV_PT)
        df_ram = pd.read_csv(caminho_ram).set_index("Environment").reindex(ORDEM_ENV_PT)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

        # --- Gráfico CPU ---
        b1 = ax1.bar(
            ORDEM_ENV_PT,
            df_cpu["Mean"],
            color=CORES,
            width=0.55,
            edgecolor="black",
            linewidth=1,
        )
        ax1.set_title("Desempenho de Processador (SysBench)", fontweight="bold", pad=15)
        ax1.set_ylabel("Eventos por Segundo (events/s)", fontweight="bold")
        ax1.set_ylim(0, df_cpu["Mean"].max() * 1.15)

        for b in b1:
            h = b.get_height()
            ax1.text(
                b.get_x() + b.get_width() / 2,
                h + (df_cpu["Mean"].max() * 0.02),
                f"{h:.0f}",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=11,
            )

        # --- Gráfico RAM ---
        b2 = ax2.bar(
            ORDEM_ENV_PT,
            df_ram["Mean"],
            color=CORES,
            width=0.55,
            edgecolor="black",
            linewidth=1,
        )
        ax2.set_title("Desempenho de Memória RAM (SysBench)", fontweight="bold", pad=15)
        ax2.set_ylabel("Throughput (MiB/s)", fontweight="bold")
        ax2.set_ylim(0, df_ram["Mean"].max() * 1.15)

        for b in b2:
            h = b.get_height()
            ax2.text(
                b.get_x() + b.get_width() / 2,
                h + (df_ram["Mean"].max() * 0.02),
                f"{h:.0f}",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=11,
            )

        plt.tight_layout()
        plt.savefig("grafico_1_cpu_ram.png", bbox_inches="tight")
        plt.close()
    except Exception as e:
        print(f"Erro a processar CPU/RAM: {e}")


def plot_rede():
    """Gera o Gráfico de TCP e UDP a partir de rede_dados_brutos.csv"""
    print("A processar Rede (TCP e UDP)...")
    try:
        caminho_rede = (
            "csvs/rede_dados_brutos.csv"
            if os.path.exists("csvs/rede_dados_brutos.csv")
            else "rede_dados_brutos.csv"
        )
        # Pode ter o sufixo _2
        if not os.path.exists(caminho_rede) and os.path.exists(
            "rede_dados_brutos_2.csv"
        ):
            caminho_rede = "rede_dados_brutos_2.csv"

        df = pd.read_csv(caminho_rede)
        df_tcp = (
            df[df["protocol"] == "tcp"]
            .groupby("environment")["throughput_Gbit_s"]
            .mean()
            .reindex(ORDEM_ENV)
        )
        df_udp = (
            df[df["protocol"] == "udp"]
            .groupby("environment")["jitter_ms"]
            .mean()
            .reindex(ORDEM_ENV)
        )

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

        # --- Gráfico TCP ---
        b1 = ax1.bar(
            ORDEM_ENV_PT,
            df_tcp,
            color=CORES,
            width=0.55,
            edgecolor="black",
            linewidth=1,
        )
        ax1.set_title("Largura de Banda TCP (iPerf3)", fontweight="bold", pad=15)
        ax1.set_ylabel("Throughput (Gbit/s)", fontweight="bold")
        ax1.set_ylim(0, df_tcp.max() * 1.15)

        for b in b1:
            h = b.get_height()
            if pd.notna(h):
                ax1.text(
                    b.get_x() + b.get_width() / 2,
                    h + (df_tcp.max() * 0.02),
                    f"{h:.2f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=11,
                )

        # --- Gráfico UDP (Jitter) ---
        b2 = ax2.bar(
            ORDEM_ENV_PT,
            df_udp,
            color=CORES,
            width=0.55,
            edgecolor="black",
            linewidth=1,
        )
        ax2.set_title(
            "Variação de Atraso - Jitter UDP (iPerf3)", fontweight="bold", pad=15
        )
        ax2.set_ylabel("Jitter (ms)", fontweight="bold")
        ax2.set_ylim(0, df_udp.max() * 1.15)

        for b in b2:
            h = b.get_height()
            if pd.notna(h):
                ax2.text(
                    b.get_x() + b.get_width() / 2,
                    h + (df_udp.max() * 0.02),
                    f"{h:.3f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=11,
                )

        plt.tight_layout()
        plt.savefig("grafico_2_rede.png", bbox_inches="tight")
        plt.close()
    except Exception as e:
        print(f"Erro ao processar Rede: {e}")


def plot_iozone():
    """Gera o Gráfico de IOzone com Escala Logarítmica a partir do csv"""
    print("A processar IOzone (Armazenamento)...")
    try:
        caminho_io = (
            "csvs/iozone_dados_brutos.csv"
            if os.path.exists("csvs/iozone_dados_brutos.csv")
            else "iozone_dados_brutos.csv"
        )
        if not os.path.exists(caminho_io) and os.path.exists(
            "iozone_dados_brutos_2.csv"
        ):
            caminho_io = "iozone_dados_brutos_2.csv"

        df = pd.read_csv(caminho_io)
        cols = [
            "write_kB_s",
            "rewrite_kB_s",
            "read_kB_s",
            "reread_kB_s",
            "random_read_kB_s",
            "random_write_kB_s",
        ]
        labels = ["Write", "Re-write", "Read", "Re-read", "Random Read", "Random Write"]

        # Converter para MiB/s
        df_mean = df.groupby("environment")[cols].mean().reindex(ORDEM_ENV) / 1024.0

        x = np.arange(len(labels))
        width = 0.25

        fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

        for i, env in enumerate(ORDEM_ENV):
            valores = df_mean.loc[env].values
            pos = x + (i - 1) * width
            barras = ax.bar(
                pos,
                valores,
                width,
                label=NOMES_PLOT[i],
                color=CORES[i],
                edgecolor="black",
                linewidth=1,
            )

            for b in barras:
                h = b.get_height()
                if pd.notna(h) and h > 0:
                    # O 1.15 é um multiplicador devido à escala logarítmica para colocar o texto acima
                    ax.text(
                        b.get_x() + b.get_width() / 2,
                        h * 1.15,
                        f"{h:.0f}",
                        ha="center",
                        va="bottom",
                        fontsize=10,
                        rotation=90,
                    )

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontweight="bold", fontsize=12)
        ax.set_ylabel("Throughput (MiB/s)", fontweight="bold")
        ax.set_title(
            "Desempenho de Armazenamento (O_DIRECT)",
            fontweight="bold",
            pad=20,
        )

        # Escala logarítmica crucial devido à enorme discrepância (VirtualBox vs KVM)
        ax.set_yscale("log")
        ax.set_ylim(1, df_mean.max().max() * 6)

        # Legenda elegante colocada por baixo do gráfico (centralizada horizontalmente)
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=3,
            frameon=False,
            fontsize=12,
        )

        plt.subplots_adjust(bottom=0.2)  # Dá espaço para a legenda em baixo
        plt.savefig("grafico_3_iozone.png", bbox_inches="tight")
        plt.close()
    except Exception as e:
        print(f"Erro ao processar IOzone: {e}")


if __name__ == "__main__":
    plot_cpu_ram()
    plot_rede()
    plot_iozone()
    print("✅ Todos os gráficos foram gerados e guardados com sucesso!")
