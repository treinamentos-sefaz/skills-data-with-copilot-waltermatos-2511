"""Módulo 2 — Manipulação de DataFrames com pandas.

Complete cada função com o apoio do GitHub Copilot. Prefira operações
vetorizadas e evite alterar o DataFrame original (use ``.copy()``).

Valide com:  ``python lab/check.py --module pandas``
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def load_wines(path: str) -> pd.DataFrame:
    """Leia o CSV em ``path`` e retorne um DataFrame do pandas."""
    return pd.read_csv(path)


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Converta a coluna ``rating`` para numérico e remova as linhas cujo
    ``rating`` seja nulo. Retorne o DataFrame limpo."""
    out = df.copy()
    out["rating"] = pd.to_numeric(out["rating"], errors="coerce")
    return out.dropna(subset=["rating"]).reset_index(drop=True)


def top_varieties_by_avg_rating(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Retorne as ``n`` variedades com maior média de ``rating`` (colunas:
    variety, avg_rating), ordenadas da maior para a menor."""
    medias = (
        df.groupby("variety", as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "avg_rating"})
    )
    return medias.sort_values(
        ["avg_rating", "variety"], ascending=[False, True]
    ).head(n).reset_index(drop=True)


def add_rating_category(df: pd.DataFrame) -> pd.DataFrame:
    """Adicione a coluna ``rating_category`` com as faixas: "Baixa" (< 85),
    "Média" (85 a 90) e "Alta" (> 90). Dica: use ``pd.cut``."""
    out = df.copy()
    rating = out["rating"]
    # pd.cut não fecha as duas bordas (85 e 90) na mesma faixa; np.select sim.
    out["rating_category"] = np.select(
        [rating < 85, rating <= 90, rating > 90],
        ["Baixa", "Média", "Alta"],
        default=None,
    )
    return out


def enrich_with_country(df: pd.DataFrame) -> pd.DataFrame:
    """Adicione a coluna ``country`` extraindo o último trecho após a vírgula de
    ``region`` (ex.: "Mendocino, California" -> "California")."""
    out = df.copy()
    out["country"] = out["region"].str.split(",").str[-1].str.strip()
    return out

