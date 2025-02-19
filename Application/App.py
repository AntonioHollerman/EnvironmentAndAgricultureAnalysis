from dash import dcc, html, callback, Dash, Input, Output
import dash_bootstrap_components as dbc

from Application.HelperClass import data_range, data_citation, data_desc

# Initialize Dash app with Bootstrap styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([

    # Row 1: World Map & Ranking of Countries
    dbc.Row([
        # Choropleth Map (75% width)
        dbc.Col(dcc.Graph(id="choropleth-map"), width=9),

        # Ranking of Countries (25% width, scrollable)
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Ranking of Regions"),
                dbc.CardBody([
                    html.Ul(id="ranking-list", style={"maxHeight": "400px", "overflowY": "scroll"})
                ])
            ]),
            width=3
        )
    ], className="mt-3"),

    # Row 2: Data Description
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Description of Data"),
                dbc.CardBody(html.P(children=data_desc["water"], id="data-desc")),
                dbc.CardHeader("Citation"),
                dbc.CardBody(html.P(children=data_citation["water"], id="data-citation"))
            ]),
            width=12
        )
    ], className="mt-3"),

    # Row 3: User Input (Dropdown & Slider)
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("User Input"),
                dbc.CardBody([
                    # Dropdown to switch between maps
                    html.Label("Select Map:", className="fw-bold"),
                    dcc.Dropdown(
                        id="map-selection",
                        options=[
                            {"label": "Water Security", "value": "water"},
                            {"label": "Food Security", "value": "food"},
                            {"label": "Electricity Security", "value": "electricity"}
                        ],
                        value="water",  # Default selection
                        clearable=False
                    ),
                    html.Br(),

                    # Slider for Year Selection
                    html.Label("Select Year:", className="fw-bold"),
                    dcc.Slider(
                        id="year-slider",
                        step=None,  # Restrict to specific marks
                        value=data_range["water"][0],  # Default year
                        marks={year: str(year) for year in data_range["water"]}
                    )
                ])
            ]),
            width=12
        )
    ], className="mt-3")

], fluid=True)  # Full width layout


def update_viz():
    pass


def update_ranks():
    pass


@callback(
    [Output(component_id="year-slider", component_property="value"),
     Output(component_id="year-slider", component_property="marks")],
    Input(component_id="map-selection", component_property="value")
)
def update_years(map_selected: str):
    years = {year: str(year) for year in data_range[map_selected]}
    year = data_range[map_selected][0]
    return year, years


@callback(
    [Output(component_id="data-desc", component_property="children"),
     Output(component_id="data-citation", component_property="children")],
    Input(component_id="map-selection", component_property="value")
)
def update_text(map_selected: str):
    return data_desc[map_selected], data_citation[map_selected]



# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
