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

modal_excel = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle('Excel')),
        dbc.ModalBody(
            dbc.Form(
                dbc.Row(
                    [
                        dbc.Label('Select x value', width='auto'),
                        dcc.Dropdown(
                            options=[1, 2, 3],
                            id='dropdown-excel-x'
                        ),
                        dbc.Label('Select y value', width='auto'),
                        dcc.Dropdown(
                            options=[1, 2, 3],
                            id='dropdown-excel-y'
                        ),
                        dbc.Button('Submit', id='btn-modal-submit-excel')
                    ]
                )
            )
        )
    ],
    id='modal-excel',
    is_open=False
)

# -----------------------------------------[CPT Control]---------------------------------------------
cpt_control = dbc.Card(
    [
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
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Label('upload Excel'), width=5),
                dbc.Col(dbc.Button('Upload', id='btn-upload-excel')),
                modal_excel
            ]
        )
    ],
    # style=SIDEBAR_STYLE
)

# -----------------------------------------[CPT-Output]-------------------------------------
content_DIV = dbc.Card(
    [
        dbc.Row(
            html.H5('Location Plan')
        ),
        dcc.Graph(id='graph-location-plan', figure=[]),
    ],
    # style=CONTENT_STYLE
)
# ========================================[Layout]========================================


def layout():
    layout = dbc.Row(
        [
            dbc.Col(cpt_control, width=3),
            dbc.Col(content_DIV, width=8)
        ], justify='around')
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
                            height=500, width=900, zoom=11)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


@app.callback(
    Output('modal-excel', 'is_open'),
    Input('btn-upload-excel', 'n_clicks'),
    Input('btn-modal-submit-excel', 'n_clicks'),
    State('modal-excel', 'is_open')
)
def toggle_modal(open_modal_click, submit_click, is_open):
    if open_modal_click or submit_click:
        return not is_open
