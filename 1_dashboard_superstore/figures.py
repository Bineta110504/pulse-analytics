# ===========================================================
# figures.py
# Construction des graphiques Plotly, avec un thème visuel
# cohérent (police, couleurs, fonds transparents) appliqué à
# chaque figure via THEME_LAYOUT.
# ===========================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import PALETTE

THEME_LAYOUT = dict(
    font=dict(family="Segoe UI, Arial, sans-serif", color="#334155", size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=50, b=10),
    title_font=dict(size=16, color="#0B1C39", family="Segoe UI, Arial, sans-serif"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
    hoverlabel=dict(bgcolor="#0B1C39", font_color="white", font_size=12),
)


def _empty(titre):
    fig = go.Figure()
    fig.add_annotation(text="Aucune donnée pour ces filtres", x=0.5, y=0.5, showarrow=False,
                        font=dict(size=14, color="#94A3B8"))
    fig.update_layout(**THEME_LAYOUT, title=titre, xaxis=dict(visible=False), yaxis=dict(visible=False), height=360)
    return fig


def fig_evolution_ca(dff: pd.DataFrame):
    if len(dff) == 0:
        return _empty("Évolution du chiffre d'affaires")

    evo = dff.groupby("YearMonth").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index().sort_values("YearMonth")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=evo["YearMonth"], y=evo["Sales"], name="Chiffre d'affaires", mode="lines",
        line=dict(color=PALETTE["primary"], width=3), fill="tozeroy",
        fillcolor="rgba(99,102,241,0.12)",
    ))
    fig.add_trace(go.Scatter(
        x=evo["YearMonth"], y=evo["Profit"], name="Profit", mode="lines",
        line=dict(color=PALETTE["accent"], width=2, dash="dot"),
    ))
    fig.update_layout(**THEME_LAYOUT, title="Évolution mensuelle du chiffre d'affaires et du profit", height=360)
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    return fig


def fig_top_produits(dff: pd.DataFrame, n=10):
    if len(dff) == 0:
        return _empty("Top 10 produits")

    top = dff.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(n).reset_index()
    top = top.sort_values("Sales")

    fig = px.bar(
        top, x="Sales", y="Product Name", orientation="h",
        color="Sales", color_continuous_scale=[PALETTE["secondary"], PALETTE["primary"]],
        text="Sales",
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(**THEME_LAYOUT, title=f"Top {n} des produits par chiffre d'affaires", height=380,
                       coloraxis_showscale=False, yaxis_title="", xaxis_title="")
    fig.update_xaxes(tickprefix="$", separatethousands=True)
    return fig


def fig_carte_ventes(dff: pd.DataFrame):
    if len(dff) == 0:
        return _empty("Carte des ventes")

    par_etat = dff.groupby(["State", "State_Code"])["Sales"].sum().reset_index().dropna(subset=["State_Code"])

    fig = px.choropleth(
        par_etat, locations="State_Code", locationmode="USA-states", color="Sales",
        scope="usa", color_continuous_scale=[PALETTE["secondary"], PALETTE["primary"], PALETTE["navy"]],
        hover_name="State", hover_data={"State_Code": False, "Sales": ":$,.0f"},
    )
    fig.update_layout(**THEME_LAYOUT, title="Répartition géographique du chiffre d'affaires", height=380,
                       geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)"),
                       coloraxis_colorbar=dict(title="CA ($)"))
    return fig


def fig_repartition_benefices(dff: pd.DataFrame):
    if len(dff) == 0:
        return _empty("Répartition des bénéfices")

    par_cat = dff.groupby("Category")["Profit"].sum().reset_index()

    fig = go.Figure(data=[go.Pie(
        labels=par_cat["Category"], values=par_cat["Profit"], hole=0.55,
        marker=dict(colors=PALETTE["sequence"]),
        textinfo="label+percent",
    )])
    total = par_cat["Profit"].sum()
    fig.update_layout(
        **THEME_LAYOUT, title="Répartition des bénéfices par catégorie", height=380,
        annotations=[dict(text=f"Profit<br><b>${total:,.0f}</b>", x=0.5, y=0.5, font_size=14, showarrow=False)],
    )
    return fig


def fig_pareto(dff: pd.DataFrame, n=15):
    if len(dff) == 0:
        return _empty("Pareto des produits")

    par_produit = dff.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).reset_index()
    top = par_produit.head(n).copy()
    top["Cumule_%"] = top["Sales"].cumsum() / par_produit["Sales"].sum() * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top["Product Name"], y=top["Sales"], name="Chiffre d'affaires",
        marker_color=PALETTE["primary"], yaxis="y1",
    ))
    fig.add_trace(go.Scatter(
        x=top["Product Name"], y=top["Cumule_%"], name="% cumulé", mode="lines+markers",
        line=dict(color=PALETTE["accent"], width=2), yaxis="y2",
    ))
    fig.add_hline(y=80, line_dash="dash", line_color=PALETTE["danger"], yref="y2",
                  annotation_text="Seuil 80%", annotation_position="top left")

    fig.update_layout(
        **THEME_LAYOUT,
        title=f"Analyse Pareto — Top {n} produits (règle des 80/20)", height=420,
        xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(title="Chiffre d'affaires ($)", tickprefix="$", separatethousands=True),
        yaxis2=dict(title="% cumulé", overlaying="y", side="right", range=[0, 105], ticksuffix="%"),
    )
    return fig
