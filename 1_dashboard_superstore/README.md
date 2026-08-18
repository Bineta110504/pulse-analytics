# Superstore Analytics — Tableau de bord de performance commerciale

Tableau de bord Dash suivant le chiffre d'affaires, les bénéfices, les
commandes et les clients à partir du jeu de données Kaggle **Superstore**
(vivek468/superstore-dataset-final).

## Installation

```bash
pip install -r requirements.txt
```

## Données

Deux options :

1. **Vrai jeu de données (recommandé pour la publication finale)** :
   télécharger `Sample - Superstore.csv` depuis Kaggle
   (vivek468/superstore-dataset-final) et le placer dans le dossier `data/`.
   `data_loader.py` le détecte automatiquement (voir `CANDIDATE_FILES`).

2. **Jeu de démonstration (déjà fourni)** : le fichier
   `data/superstore_demo.csv` est inclus pour pouvoir lancer et tester
   l'application immédiatement, sans dépendre de Kaggle. Il est généré par
   `generate_demo_data.py` (même schéma de colonnes que le vrai dataset).
   Tant que le vrai fichier n'est pas présent, la barre latérale affiche un
   badge « Données de démonstration » pour que ce soit toujours visible.

Pour régénérer le jeu de démonstration :
```bash
python generate_demo_data.py
```

## Lancement

```bash
python app.py
```

Application accessible sur http://127.0.0.1:8050

## Structure du projet

```
dash_superstore/
├── app.py                  # layout (sidebar + contenu) et callbacks
├── data_loader.py          # chargement, filtrage, calcul des KPIs
├── figures.py               # construction des 5 graphiques Plotly (thème visuel commun)
├── generate_demo_data.py   # générateur du jeu de démonstration
├── assets/
│   ├── style.css            # feuille de style premium (sidebar sombre, cartes KPI)
│   └── logo.svg              # logo "Pulse Analytics" (généré, sans marque déposée)
├── data/
│   └── superstore_demo.csv  # jeu de démonstration (remplacer par le vrai fichier Kaggle)
└── requirements.txt
```

## Avant de publier sur LinkedIn

Remplacer le jeu de démonstration par le vrai fichier Kaggle
(`Sample - Superstore.csv` dans `data/`) afin que les chiffres affichés
soient ceux du dataset réel, pas des données synthétiques.
