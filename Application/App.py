from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
from HelperClass import get_viz, get_rank, data_range, data_desc, data_citation

# Default selections
default_graph = "water"
default_year = data_range[default_graph][0]

# Initialize Dash app with Bootstrap styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # Row 1: User Input (Dropdown & Slider)
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("User Input"),
                dbc.CardBody([
                    html.Label("Select Map:", className="fw-bold"),
                    dcc.Dropdown(
                        id="map-selection",
                        options=[
                            {"label": "Water Security", "value": "water"},
                            {"label": "Food Security", "value": "food"},
                            {"label": "Electricity Security", "value": "electricity"}
                        ],
                        value=default_graph,
                        clearable=False
                    ),
                    html.Br(),
                    html.Label("Select Year:", className="fw-bold"),
                    dcc.Slider(
                        id="year-slider",
                        step=None,
                        value=default_year,
                        marks={year: str(year) for year in data_range[default_graph]}
                    )
                ])
            ], style={"height": "100%"}),
            width=12
        )
    ], className="mt-3", style={"paddingTop": "30px"}),

    # Row 2: World Map + Ranking Column
    dbc.Row([
        # World Map (Left Side)
        dbc.Col(
            dcc.Graph(id="choropleth-map", figure=get_viz(default_graph, default_year)),
            width=9
        ),

        # Ranking Column (Right Side, only next to the map)
        # Ranking Column (Right Side, only next to the map)
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Ranking of Regions"),
                dbc.CardBody([
                    html.Ul(id="ranking-list",
                            style={"maxHeight": "400px",  # Adjust height dynamically
                                   "overflowY": "auto",  # Enables scrolling
                                   "margin": "0", "padding": "0"})
                ], style={"flex": "1", "display": "flex", "flexDirection": "column"})  # Ensures full stretch
            ], style={"height": "100%", "display": "flex", "flexDirection": "column"}),
            width=3,
            style={"display": "flex", "flexDirection": "column"}  # Matches height with the graph
        )
    ], className="mt-3", style={"display": "flex", "alignItems": "stretch"}),

    # Row 3: Data Description (Below the map, spanning full width)
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Description of Data"),
                dbc.CardBody(html.P(id="data-desc", children=data_desc[default_graph])),
                dbc.CardHeader("Citation"),
                dbc.CardBody(html.P(id="data-citation", children=data_citation[default_graph]))
            ], style={"height": "100%"}),
            width=12
        )
    ], className="mt-3", style={"paddingBottom": "30px"})

], fluid=True)



# Callbacks
@app.callback(
    Output("choropleth-map", "figure"),
    [Input("map-selection", "value"), Input("year-slider", "value")]
)
def update_viz(map_selected, year):
    return get_viz(map_selected, year)

@app.callback(
    Output("ranking-list", "children"),
    [Input("map-selection", "value"), Input("year-slider", "value")]
)
def update_ranks(map_selected, year):
    return [html.Li(f"{item.region}: {item.value}") for item in get_rank(map_selected, year)]

@app.callback(
    [Output("year-slider", "value"), Output("year-slider", "marks")],
    Input("map-selection", "value")
)
def update_years(map_selected):
    years = {year: str(year) for year in data_range[map_selected]}
    return data_range[map_selected][0], years

@app.callback(
    [Output("data-desc", "children"), Output("data-citation", "children")],
    Input("map-selection", "value")
)
def update_text(map_selected):
    return data_desc[map_selected], data_citation[map_selected]

# Run app
if __name__ == "__main__":
    print("Starting Instance")
    app.run_server(debug=True)
