import logging
import webbrowser
from threading import Timer

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import PROJ_DATA, app
from apps import about, data_process, project, cpt_process

# --------------------Define the logger below -------------------------------------------
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
# -------------------------------------------------------------------------------------

arup_logo = 'logo.png'
navbar = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url(
                        arup_logo), height='30x')),
                    dbc.Col(dbc.NavbarBrand(
                        'Offshore CPT', className='ml-2')),
                    dbc.Col(dbc.NavLink('Project', href='project')),
                    dbc.Col(dbc.NavLink("Data", href='data_process')),
                    dbc.Col(dbc.NavLink('CPT', href='CPT')),
                    dbc.Col(dbc.NavLink('Pile', href='settlement')),
                    # dbc.Col(dbc.NavLink('Progress', href='progress')),
                    dbc.Col(dbc.NavLink('Caissons', href='analysis')),
                    dbc.Col(dbc.NavLink('Site', href='plaxis')),
                    dbc.Col(dbc.NavLink('About',
                                        href='report'), className="width800")
                ],
                className="g-0"
            )
        )
    ],
    color="light",
    dark=True,
)
body = dbc.Container([
    html.Div([dcc.Location(id='url', refresh=False)], className='row'),
    html.Div(id='page-content'),
], fluid=True)
app.layout = html.Div([navbar, html.Br(), body])

# --- Callbacks --- #


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/data_process':
        return data_process.layout()
#         # return
#     elif pathname == '/settlement':
#         # importlib.reload(sm)
#         sm.layout = sm.__layout()  # we force recalculation
#         return sm.layout
    elif pathname == '/project':
        return project.project_layout(PROJ_DATA)
    elif pathname == '/CPT':
        return cpt_process.layout()
#     elif pathname == 'extensometer':
#         return extensometer.layout
#     elif pathname == '/progress':
#         return progress.layout
#     elif pathname == '/analysis':
#         return analysis.layout
#     elif pathname == '/plaxis':
#         return plaxis.layout
    else:
        return about.layout


port = 5000


def open_browser():
    webbrowser.open_new(f'http://localhost:{port}')


if __name__ == '__main__':

    # Timer(1, open_browser).start()
    app.run_server(debug=False, port=port)
