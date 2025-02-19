from dash import dcc, html, callback, Dash, Input, Output
import dash_bootstrap_components as dbc
from HelperClass import *

default_graph = "water"
default_year = data_range[default_graph][0]

# Initialize Dash app with Bootstrap styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([

    # Row 1: World Map & Ranking of Countries
    dbc.Row([
        # Choropleth Map (75% width)
        dbc.Col(dcc.Graph(id="choropleth-map", figure=get_viz(default_graph, default_year)), width=9),

        # Ranking of Countries (25% width, scrollable)
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Ranking of Regions"),
                dbc.CardBody([
                    html.Ul(id="ranking-list",
                            style={"maxHeight": "400px", "overflowY": "scroll"})
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
                dbc.CardBody(html.P(children=data_desc[default_graph], id="data-desc")),
                dbc.CardHeader("Citation"),
                dbc.CardBody(html.P(children=data_citation[default_graph], id="data-citation"))
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
                        value=default_year,  # Default year
                        marks={year: str(year) for year in data_range[default_graph]}
                    )
                ])
            ]),
            width=12
        )
    ], className="mt-3")

], fluid=True)  # Full width layout


@app.callback(Output(component_id="choropleth-map", component_property="figure"),
          [Input(component_id="map-selection", component_property="value"),
           Input(component_id="year-slider", component_property="value")])
def update_viz(map_selected: str, year: int):
    return get_viz(map_selected, year)


@app.callback(
    Output("ranking-list", "children"),
    [Input(component_id="map-selection", component_property="value"),
     Input(component_id="year-slider", component_property="value")]
)
def update_ranks(map_selected: str, year: int):
    return [html.Li(item.region + ": " + item.value.__str__()) for item in get_rank(map_selected, year)]


@app.callback(
    [Output(component_id="year-slider", component_property="value"),
     Output(component_id="year-slider", component_property="marks")],
    Input(component_id="map-selection", component_property="value")
)
def update_years(map_selected: str):
    years = {year: str(year) for year in data_range[map_selected]}
    year = data_range[map_selected][0]
    return year, years


@app.callback(
    [Output(component_id="data-desc", component_property="children"),
     Output(component_id="data-citation", component_property="children")],
    Input(component_id="map-selection", component_property="value")
)
def update_text(map_selected: str):
    return data_desc[map_selected], data_citation[map_selected]


# Run app
if __name__ == "__main__":
    print("Starting Instance")
    app.run_server(debug=True)
