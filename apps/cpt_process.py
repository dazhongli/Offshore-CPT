import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State

from app import PROJ_DATA, PROJECT_PATH, app
from src.cpt import CPT
import geopandas as gpd

# ========================================[Global Variables]========================================
px.set_mapbox_access_token(open('./data/mapbox/mapbox_token').read())
cpt_driver = CPT(net_area_ratio=0.85)
# cpt_driver.read_ASCII()
__project_name__ = PROJ_DATA['active_project']

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 60,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "border": "solid"
}

CONTENT_STYLE = {
    "position": "fixed",
    "top": 60,
    "left": "22rem",
    "bottom": 0,
    "width": "100rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "border": "solid"
}
# ========================================[Global Functions]========================================

# ========================================[Components]========================================


# -----------------------------------------[CPT Control]---------------------------------------------
cpt_control = html.Div(
    [
        dbc.Row(html.H4('CPT Process')),
        dbc.Row(html.H5('Input')),
        dbc.Row(                                        # Area Radio
            [
                dbc.Col(dbc.Label('Area Ratio'), width=5),
                dbc.Col(dbc.Input('input-area-ratio', value=0.85), width=6)
            ]
        ),
        dbc.Row(                                        # Area Radio
            [
                dbc.Col(dbc.Label('Read ASCII'), width=5),
                dbc.Col(dbc.Input('input-area-ratio', value=0.85), width=6)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Label('CPT Process'), width=5),
                dbc.Col(dbc.Button('Site Boundary'), width=6),
                dbc.Col(dbc.Checkbox(id='cbx-site-boundary'), width=1)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Label('Show Layout'), width=5),
                dbc.Col(dbc.Button('Layout', id='btn-show-layout'), width=6)
            ]
        )
    ],
    style=SIDEBAR_STYLE
)

# -----------------------------------------[CPT-Output]-------------------------------------
content_DIV = html.Div(
    [
        dbc.Row(
            html.H5('Location Plan')
        ),
        dcc.Graph(id='graph-location-plan'),
    ],
    style=CONTENT_STYLE
)
# ========================================[Layout]========================================


def layout():
    layout = html.Div([cpt_control, content_DIV])
    return layout


# ========================================[Callbacks]========================================
@app.callback(
    Output('graph-location-plan', 'figure'),
    Input('btn-show-layout', 'n_clicks')
)
def show_CPT_location(n_clicks):
    filename = PROJECT_PATH / __project_name__ / 'data' / 'shp' / 'CPT_coords.json'
    assert (filename.exists())
    gdf = gpd.read_file(filename)
    fig = px.scatter_mapbox(gdf, lat='Lon', lon='Lat',
                            height=500, width=1000, zoom=11)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig
