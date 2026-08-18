# ===========================================================
# app.py
# Tableau de bord commercial (Superstore) — layout premium à
# sidebar fixe. Chaque graphique a son propre callback (Inputs :
# les 4 filtres) pour un code modulaire et des mises à jour
# ciblées, plutôt qu'un unique callback monolithique.
# ===========================================================

from dash import Dash, html, dcc, Input, Output

from data_loader import (
    df, filtrer, calculer_kpis, formater_montant, USING_DEMO_DATA,
    LISTE_ANNEES, LISTE_REGIONS, LISTE_CATEGORIES, LISTE_SEGMENTS,
)
from figures import (
    fig_evolution_ca, fig_top_produits, fig_carte_ventes,
    fig_repartition_benefices, fig_pareto,
)

EXTERNAL_STYLESHEETS = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
]

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
app.title = "Superstore Analytics — Performance commerciale"
server = app.server


# ===========================================================
# COMPOSANTS DE LAYOUT
# ===========================================================

def filtre(label, id_, options, placeholder):
    return html.Div([
        html.Label(label, className="filtre-label"),
        dcc.Dropdown(id=id_, options=[{"label": str(o), "value": o} for o in options],
                     placeholder=placeholder, className="filtre-dropdown", clearable=True),
    ], className="filtre-item")


def sidebar():
    return html.Div([
        html.Div([
            html.Img(src="/assets/logo.svg", className="logo-img"),
        ], className="logo-wrap"),

        html.Div("FILTRES", className="sidebar-section-title"),
        filtre("Année", "f-annee", LISTE_ANNEES, "Toutes les années"),
        filtre("Région", "f-region", LISTE_REGIONS, "Toutes les régions"),
        filtre("Catégorie", "f-categorie", LISTE_CATEGORIES, "Toutes les catégories"),
        filtre("Segment client", "f-segment", LISTE_SEGMENTS, "Tous les segments"),

        html.Div([
            html.I(className="fas fa-circle-info"),
            html.Span(" Données de démonstration" if USING_DEMO_DATA else " Données Superstore (Kaggle)"),
        ], className="sidebar-datasource"),

        html.Div([
            html.P("Bineta FAYE", className="sidebar-author"),
            html.P("Dashboard Performance Commerciale", className="sidebar-author-sub"),
        ], className="sidebar-footer"),
    ], className="sidebar")


def kpi_card(icone, titre, id_, id_sub, couleur):
    return html.Div([
        html.Div(html.I(className=f"fas {icone}"), className="kpi-icon-wrap", style={"background": couleur}),
        html.Div([
            html.P(titre, className="kpi-titre"),
            html.H2("—", id=id_, className="kpi-valeur"),
            html.P("—", id=id_sub, className="kpi-sous-valeur"),
        ]),
    ], className="kpi-card")


def contenu_principal():
    return html.Div([
        html.Div([
            html.Div([
                html.H1("Performance commerciale", className="page-titre"),
                html.P("Suivi du chiffre d'affaires, des bénéfices et des ventes", className="page-soustitre"),
            ]),
        ], className="topbar"),

        html.Div([
            kpi_card("fa-sack-dollar", "Chiffre d'affaires", "kpi-ca", "kpi-ca-sub", "linear-gradient(135deg,#6366F1,#8B5CF6)"),
            kpi_card("fa-chart-line", "Profit", "kpi-profit", "kpi-profit-sub", "linear-gradient(135deg,#2DD4BF,#22C55E)"),
            kpi_card("fa-file-invoice", "Commandes", "kpi-commandes", "kpi-commandes-sub", "linear-gradient(135deg,#F4B400,#F4436C)"),
            kpi_card("fa-users", "Clients", "kpi-clients", "kpi-clients-sub", "linear-gradient(135deg,#0B1C39,#334155)"),
        ], className="kpi-grid"),

        html.Div([
            html.Div(dcc.Graph(id="g-evolution", config={"displayModeBar": False}), className="card graph-card span-2"),
            html.Div(dcc.Graph(id="g-repartition", config={"displayModeBar": False}), className="card graph-card"),
        ], className="grid-row"),

        html.Div([
            html.Div(dcc.Graph(id="g-carte", config={"displayModeBar": False}), className="card graph-card"),
            html.Div(dcc.Graph(id="g-top-produits", config={"displayModeBar": False}), className="card graph-card"),
        ], className="grid-row"),

        html.Div([
            html.Div(dcc.Graph(id="g-pareto", config={"displayModeBar": False}), className="card graph-card full"),
        ], className="grid-row"),

        html.Footer("© 2026 — Bineta FAYE · Superstore Analytics · Données Kaggle (Superstore Dataset)", className="footer"),
    ], className="contenu-principal")


app.layout = html.Div([
    dcc.Store(id="filtres-store"),
    sidebar(),
    contenu_principal(),
], className="app-shell")


# ===========================================================
# CALLBACKS
# ===========================================================

FILTER_INPUTS = [
    Input("f-annee", "value"),
    Input("f-region", "value"),
    Input("f-categorie", "value"),
    Input("f-segment", "value"),
]


def _dff(annee, region, categorie, segment):
    return filtrer(df, annee=annee, region=region, categorie=categorie, segment=segment)


@app.callback(
    Output("kpi-ca", "children"), Output("kpi-ca-sub", "children"),
    Output("kpi-profit", "children"), Output("kpi-profit-sub", "children"),
    Output("kpi-commandes", "children"), Output("kpi-commandes-sub", "children"),
    Output("kpi-clients", "children"), Output("kpi-clients-sub", "children"),
    FILTER_INPUTS,
)
def maj_kpis(annee, region, categorie, segment):
    dff = _dff(annee, region, categorie, segment)
    k = calculer_kpis(dff)
    return (
        formater_montant(k["ca"]), f"{len(dff):,} lignes de vente",
        formater_montant(k["profit"]), f"Marge {k['marge']}%",
        f"{k['commandes']:,}", "commandes distinctes",
        f"{k['clients']:,}", "clients actifs",
    )


@app.callback(Output("g-evolution", "figure"), FILTER_INPUTS)
def maj_evolution(annee, region, categorie, segment):
    return fig_evolution_ca(_dff(annee, region, categorie, segment))


@app.callback(Output("g-repartition", "figure"), FILTER_INPUTS)
def maj_repartition(annee, region, categorie, segment):
    return fig_repartition_benefices(_dff(annee, region, categorie, segment))


@app.callback(Output("g-carte", "figure"), FILTER_INPUTS)
def maj_carte(annee, region, categorie, segment):
    return fig_carte_ventes(_dff(annee, region, categorie, segment))


@app.callback(Output("g-top-produits", "figure"), FILTER_INPUTS)
def maj_top_produits(annee, region, categorie, segment):
    return fig_top_produits(_dff(annee, region, categorie, segment))


@app.callback(Output("g-pareto", "figure"), FILTER_INPUTS)
def maj_pareto(annee, region, categorie, segment):
    return fig_pareto(_dff(annee, region, categorie, segment))


if __name__ == "__main__":
    app.run(debug=True)
