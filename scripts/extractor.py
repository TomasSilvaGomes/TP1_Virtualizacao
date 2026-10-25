import glob
import os
import re

import pandas as pd

PASTA_RESULTADOS = "resultados_virtualizacao2"


def extrair_dados():
    dados_rede, dados_iozone = [], []

    # Extrair os ficheiros do zip (KVM e VirtualBox)
    for ficheiro in glob.glob(f"{PASTA_RESULTADOS}/*.txt"):
        nome = os.path.basename(ficheiro).lower()
        if "host" in nome:
            env = "Host"
        elif "kvm" in nome:
            env = "KVM"
        elif "virtualbox" in nome:
            env = "VirtualBox"
        else:
            continue

        with open(ficheiro, "r", encoding="utf-8", errors="ignore") as f:
            texto = f.read()

        # Extração iPerf3 TCP
        if "tcp" in nome:
            matches = re.findall(r"([\d.]+)\s+([MG])bits/sec", texto)
            if matches:
                val, unit = matches[-1]
                val = float(val)
                if unit == "G":
                    val *= 1000
                dados_rede.append(
                    {"Ambiente": env, "Metrica": "TCP (Mbit/s)", "Valor": val}
                )

        # Extração iPerf3 UDP
        elif "udp" in nome:
            matches = re.findall(r"([\d.]+)\s+ms\s+\d+/\d+", texto)
            if matches:
                dados_rede.append(
                    {
                        "Ambiente": env,
                        "Metrica": "Jitter UDP (ms)",
                        "Valor": float(matches[-1]),
                    }
                )

        # Extração IOzone
        elif "iozone" in nome:
            padroes = {
                "Write": r"initial writers\s*=\s*([\d.]+)",
                "Re-write": r"rewriters\s*=\s*([\d.]+)",
                "Read": r"readers\s*=\s*([\d.]+)",
                "Re-read": r"re-readers\s*=\s*([\d.]+)",
                "Random Read": r"random readers\s*=\s*([\d.]+)",
                "Random Write": r"random writers\s*=\s*([\d.]+)",
            }
            for op, regex in padroes.items():
                m = re.search(regex, texto)
                if m:
                    dados_iozone.append(
                        {
                            "Ambiente": env,
                            "Operacao": op,
                            "Valor": float(m.group(1)) / 1024.0,
                        }
                    )

    # Injetar os 3 testes manuais do Host (Loopback) retirados do teu apontamento inicial
    for _ in range(3):
        dados_rede.append(
            {"Ambiente": "Host", "Metrica": "TCP (Mbit/s)", "Valor": 66500.0}
        )
        dados_rede.append(
            {"Ambiente": "Host", "Metrica": "Jitter UDP (ms)", "Valor": 0.014}
        )

    df_rede = pd.DataFrame(dados_rede)
    df_iozone = pd.DataFrame(dados_iozone)

    if not df_rede.empty:
        resumo_rede = (
            df_rede.groupby(["Metrica", "Ambiente"])["Valor"]
            .agg(["mean", "std"])
            .round(2)
            .unstack()
        )
        resumo_rede.columns = [f"{env}_{stat}" for stat, env in resumo_rede.columns]
        resumo_rede.to_csv("rede_final.csv")
        print("Criado: rede_final.csv")

    if not df_iozone.empty:
        resumo_iozone = (
            df_iozone.groupby(["Operacao", "Ambiente"])["Valor"]
            .agg(["mean", "std"])
            .round(2)
            .unstack()
        )
        ordem = ["Write", "Re-write", "Read", "Re-read", "Random Read", "Random Write"]
        resumo_iozone = resumo_iozone.reindex(ordem)
        resumo_iozone.columns = [f"{env}_{stat}" for stat, env in resumo_iozone.columns]
        resumo_iozone.to_csv("iozone_final.csv")
        print("Criado: iozone_final.csv")


if __name__ == "__main__":
    extrair_dados()
