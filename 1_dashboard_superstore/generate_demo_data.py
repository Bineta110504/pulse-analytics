# ===========================================================
# generate_demo_data.py
# Génère un jeu de données de démonstration au même schéma que
# le dataset Kaggle "Superstore" (vivek468/superstore-dataset-final),
# pour pouvoir lancer et tester l'application immédiatement.
# À REMPLACER par le vrai fichier Kaggle pour la version finale
# (voir README.md).
# ===========================================================

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

REGIONS_STATES = {
    "West": ["California", "Washington", "Oregon", "Nevada", "Arizona", "Colorado", "Utah"],
    "East": ["New York", "Pennsylvania", "New Jersey", "Massachusetts", "Virginia", "Maryland"],
    "Central": ["Texas", "Illinois", "Ohio", "Michigan", "Missouri", "Wisconsin", "Minnesota"],
    "South": ["Florida", "Georgia", "North Carolina", "Tennessee", "Alabama", "Louisiana"],
}

CATEGORIES = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels", "Fasteners"],
    "Technology": ["Phones", "Machines", "Accessories", "Copiers"],
}

PRODUCT_ADJ = ["Premium", "Standard", "Executive", "Deluxe", "Compact", "Pro", "Classic", "Ultra"]
PRODUCT_NOUN = {
    "Chairs": "Office Chair", "Tables": "Meeting Table", "Bookcases": "Bookcase", "Furnishings": "Desk Lamp",
    "Binders": "Ring Binder", "Paper": "Copy Paper Ream", "Storage": "Storage Box", "Art": "Desk Organizer",
    "Labels": "Label Set", "Fasteners": "Stapler",
    "Phones": "Smartphone", "Machines": "Label Printer", "Accessories": "Wireless Mouse", "Copiers": "Copier",
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

N_ROWS = 9800
N_CUSTOMERS = 780
N_ORDERS = 5000


def build():
    customer_ids = [f"CU-{10000+i}" for i in range(N_CUSTOMERS)]
    order_ids = [f"US-{2020 + i % 4}-{100000+i}" for i in range(N_ORDERS)]

    rows = []
    start = pd.Timestamp("2020-01-01")
    end = pd.Timestamp("2023-12-31")
    date_range_days = (end - start).days

    for i in range(N_ROWS):
        region = rng.choice(list(REGIONS_STATES.keys()), p=[0.32, 0.28, 0.24, 0.16])
        state = rng.choice(REGIONS_STATES[region])
        category = rng.choice(list(CATEGORIES.keys()), p=[0.22, 0.55, 0.23])
        subcat = rng.choice(CATEGORIES[category])
        product = f"{rng.choice(PRODUCT_ADJ)} {PRODUCT_NOUN[subcat]}"

        order_date = start + pd.Timedelta(days=int(rng.integers(0, date_range_days)))
        ship_date = order_date + pd.Timedelta(days=int(rng.integers(1, 7)))

        base_price = {"Furniture": 220, "Office Supplies": 35, "Technology": 340}[category]
        quantity = int(rng.integers(1, 9))
        discount = float(rng.choice([0, 0, 0, 0.1, 0.15, 0.2, 0.3, 0.4], p=[0.35, 0.15, 0.1, 0.15, 0.1, 0.07, 0.05, 0.03]))
        unit_price = base_price * rng.uniform(0.6, 1.8)
        sales = round(unit_price * quantity * (1 - discount * 0.3), 2)

        margin_rate = rng.normal(0.18, 0.15)
        if discount >= 0.3:
            margin_rate -= 0.25
        profit = round(sales * margin_rate, 2)

        rows.append({
            "Row ID": i + 1,
            "Order ID": rng.choice(order_ids),
            "Order Date": order_date.strftime("%m/%d/%Y"),
            "Ship Date": ship_date.strftime("%m/%d/%Y"),
            "Ship Mode": rng.choice(SHIP_MODES, p=[0.6, 0.2, 0.15, 0.05]),
            "Customer ID": rng.choice(customer_ids),
            "Customer Name": f"Client {rng.choice(customer_ids)}",
            "Segment": rng.choice(SEGMENTS, p=[0.5, 0.3, 0.2]),
            "Country": "United States",
            "City": state,
            "State": state,
            "Postal Code": int(rng.integers(10000, 99999)),
            "Region": region,
            "Product ID": f"{category[:3].upper()}-{subcat[:2].upper()}-{1000+i}",
            "Category": category,
            "Sub-Category": subcat,
            "Product Name": product,
            "Sales": sales,
            "Quantity": quantity,
            "Discount": discount,
            "Profit": profit,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build()
    out_path = "data/superstore_demo.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"{len(df)} lignes générées -> {out_path}")
