import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Initialize Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([

    # Row 1: World Map & Ranking of Countries
    dbc.Row([
        # Choropleth Map (75% width)
        dbc.Col(dcc.Graph(id="choropleth-map"), width=9),

        # Ranking of Countries (25% width, scrollable)
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Ranking of Countries"),
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
                dbc.CardBody(html.P("This section will describe the selected data..."))
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
                        min=2000,
                        max=2025,
                        step=1,
                        value=2020,  # Default year
                        marks={year: str(year) for year in range(2000, 2026, 5)}
                    )
                ])
            ]),
            width=12
        )
    ], className="mt-3")

], fluid=True)  # Full width layout

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
