# ===========================================================
# data_loader.py
# Chargement et préparation des données. Cherche en priorité le
# vrai fichier Kaggle, puis retombe sur le jeu de démonstration
# généré par generate_demo_data.py.
# ===========================================================

import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
CANDIDATE_FILES = [
    "Sample - Superstore.csv",
    "Superstore.csv",
    "superstore.csv",
    "superstore_demo.csv",
]

US_STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC",
}

PALETTE = {
    "primary": "#6366F1",
    "secondary": "#2DD4BF",
    "accent": "#F4B400",
    "danger": "#F4436C",
    "navy": "#0B1C39",
    "sequence": ["#6366F1", "#2DD4BF", "#F4B400", "#F4436C", "#8B5CF6", "#22C55E"],
}


def _find_data_file():
    for name in CANDIDATE_FILES:
        path = os.path.join(BASE_DIR, "data", name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "Aucun fichier de données trouvé dans data/. Placez-y le fichier Kaggle "
        "'Sample - Superstore.csv' (vivek468/superstore-dataset-final), ou lancez "
        "generate_demo_data.py pour créer un jeu de démonstration."
    )


def _load_raw() -> pd.DataFrame:
    path = _find_data_file()
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")  # le CSV Kaggle est souvent en latin-1

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["Order Date", "Sales"])

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["YearMonth"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["State_Code"] = df["State"].map(US_STATE_ABBREV)
    df["Marge"] = (df["Profit"] / df["Sales"].replace(0, pd.NA)) * 100

    return df


df = _load_raw()
USING_DEMO_DATA = "demo" in _find_data_file()

LISTE_ANNEES = sorted(df["Year"].dropna().unique().tolist())
LISTE_REGIONS = sorted(df["Region"].dropna().unique().tolist())
LISTE_CATEGORIES = sorted(df["Category"].dropna().unique().tolist())
LISTE_SEGMENTS = sorted(df["Segment"].dropna().unique().tolist())


def filtrer(dff: pd.DataFrame, annee=None, region=None, categorie=None, segment=None) -> pd.DataFrame:
    if annee:
        dff = dff[dff["Year"] == annee]
    if region:
        dff = dff[dff["Region"] == region]
    if categorie:
        dff = dff[dff["Category"] == categorie]
    if segment:
        dff = dff[dff["Segment"] == segment]
    return dff


def calculer_kpis(dff: pd.DataFrame) -> dict:
    if len(dff) == 0:
        return {"ca": 0, "profit": 0, "commandes": 0, "clients": 0, "marge": 0}
    ca = dff["Sales"].sum()
    profit = dff["Profit"].sum()
    return {
        "ca": ca,
        "profit": profit,
        "commandes": dff["Order ID"].nunique(),
        "clients": dff["Customer ID"].nunique(),
        "marge": round((profit / ca) * 100, 1) if ca else 0,
    }


def formater_montant(valeur: float) -> str:
    """Formate un montant en K$ / M$ pour un affichage compact des KPIs."""
    abs_v = abs(valeur)
    signe = "-" if valeur < 0 else ""
    if abs_v >= 1_000_000:
        return f"{signe}{abs_v/1_000_000:.2f} M$"
    if abs_v >= 1_000:
        return f"{signe}{abs_v/1_000:.1f} k$"
    return f"{signe}{abs_v:.0f} $"
