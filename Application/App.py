from dash import dcc, html, Dash, Input, Output, dash_table

import dash_bootstrap_components as dbc
from HelperClass import *

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
                dbc.CardBody([
                    html.Label("Select Map:", className="fw-bold"),
                    html.Br(),
                    dcc.Dropdown(
                        id="map-selection",
                        options=[
                            {"label": "Water Security", "value": "water"},
                            {"label": "Food Security", "value": "food"},
                            {"label": "Electricity Security", "value": "electricity"}
                        ],
                        value=default_graph,
                        clearable=False,
                        style={"width": "auto", "minWidth": "150px", "display": "inline-block", "paddingTop": "10px"}
                    ),
                    html.Br(),
                    html.Label("Select Year:", className="fw-bold", style={"paddingTop": "10px"}),
                    dcc.Slider(
                        id="year-slider",
                        step=None,
                        value=default_year,
                        marks={year: str(year) for year in data_range[default_graph]}
                    )
                ])
            ], style={"height": "100%", "border": "none"}),  # Hide border
            width=12
        )
    ], className="mt-3", style={"paddingTop": "10px"}),

    # Row 2: World Map + Ranking Column
    dbc.Row([
        # World Map (Left Side)
        dbc.Col(
            dcc.Graph(id="choropleth-map", figure=get_viz(default_graph, default_year)),
            width=9
        ),

        # Ranking Column (Right Side, only next to the map)
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Ranking of Regions", style={"textAlign": "center"}),
                dbc.CardBody([
                    dash_table.DataTable(
                        id="ranking-table",
                        columns=[
                            {"name": "Region", "id": "region"},
                            {"name": "Value", "id": "value"},
                        ],
                        style_as_list_view=True,  # Disables vertical lines
                        style_cell={"textAlign": "left"},  # Aligns text to the left
                        style_header={
                            "fontWeight": "bold",
                            "borderBottom": "2px solid black"  # Emphasize header
                        },
                        style_data={
                            "borderBottom": "1px solid #ddd"  # Only horizontal lines
                        },
                        style_table={
                            "maxHeight": "400px",  # Enables scrolling
                            "overflowY": "auto"
                        }
                    )
                ], style={"flex": "1", "display": "flex", "flexDirection": "column"})  # Ensures full stretch
            ], style={"height": "100%", "display": "flex", "flexDirection": "column"}),  # Keep border
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
            ], style={"height": "100%", "border": "none"}),  # Hide border
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
    [Output("ranking-table", "columns"),
     Output("ranking-table", "data")],
    [Input("map-selection", "value"), Input("year-slider", "value")]
)
def update_ranks(map_selected, year):
    new_columns=[
        {"name": map_region[map_selected], "id": "region"},
        {"name": map_value[map_selected], "id": "value"},
    ]

    # Fetch rankings from get_rank() function
    rankings = get_rank(map_selected, year)

    # Convert to list of dictionaries (DataTable format)
    return new_columns, [{"region": item.region, "value": item.value_d} for item in rankings]

@app.callback(
    [Output("year-slider", "value"), Output("year-slider", "marks")],
    Input("map-selection", "value")
)
def update_years(map_selected):
    year_range = data_range[map_selected]
    def display_year(i, _year):
        if i % 5 == 0:
            return str(_year)
        else:
            return ""

    if map_selected == "water":
        years = {year: display_year(index, year) for index, year in enumerate(year_range)}
    else:
        years = {year: str(year) for year in year_range}
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
