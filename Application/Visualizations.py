from DbAPI import *  # Importing database API functions
import json  # Importing JSON module for handling GeoJSON files
import plotly.express as px  # Importing Plotly Express for data visualization

# Load and preprocess continents GeoJSON data
continents_geo = json.load(open("..\\Data\\GeoJson\\continents.geojson"))
for feature in continents_geo["features"]:
    feature["id"] = feature["properties"]["CONTINENT"]  # Set feature ID to continent name

# Load and preprocess countries GeoJSON data
countries_geo = json.load(open("..\\Data\\GeoJson\\countries.json"))
for feature in countries_geo["features"]:
    feature["id"] = feature["properties"]["ISO_A3"]  # Set feature ID to country ISO3 code


def energy_predictions_viz(year: int):
    """
    Generates a choropleth map to visualize energy security predictions for a given year.

    Args:
        year (int): The year for which energy security predictions should be visualized.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object displaying the energy security predictions.
    """
    energy_predictions_df = get_energy_predictions_df(year)  # Fetch energy predictions data

    fig = px.choropleth(
        energy_predictions_df,
        locations='id',
        geojson=continents_geo,
        color="ej_value",
        scope="world",
        color_continuous_scale="Plasma",
        title=f"Energy Security Predictions of {year}",
        range_color=(0, 100),
        hover_name="id"
    )

    # Customizing the layout
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="EJ Output",  # Custom title for the color bar
            title_side="top",  # Position of the title
        ),
        geo=dict(
            bgcolor="lightblue",  # Change ocean/background color
        ),
        paper_bgcolor="white"  # Set background outside the map
    )

    return fig


def food_security_viz(year: int, indicator: str = "Prevalence of Severe Food Insecurity (%)"):
    """
    Generates a choropleth map to visualize food security for a given year and indicator.

    Args:
        year (int): The year for which food security data should be visualized.
        indicator (str, optional): The food security indicator to display.
                                   Defaults to "Prevalence of Severe Food Insecurity (%)".

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object displaying the food security data.
    """
    food_df = get_food_insecurity_df(year, indicator)  # Fetch food insecurity data

    fig = px.choropleth(
        food_df,
        locations='id',
        geojson=countries_geo,
        color="value",
        scope="world",
        color_continuous_scale="YlOrRd",
        title=f"Food Security of {year}",
        hover_name="country",
        range_color=(0, 40)
    )

    # Customizing the layout
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Percent experiencing food insecurity",  # Custom title for the color bar
            title_side="top",  # Position of the title
        ),
        paper_bgcolor="white",  # Set background outside the map
        geo=dict(bgcolor="lightblue")  # Ocean/background color
    )

    return fig


def water_security_viz(year: int):
    """
    Generates a choropleth map to visualize water security for a given year.

    Args:
        year (int): The year for which water security data should be visualized.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object displaying the water security data.
    """
    water_df = get_water_security_df(year)  # Fetch water security data

    fig = px.choropleth(
        water_df,
        locations='id',
        geojson=countries_geo,
        color="water_per_capita",
        scope="world",
        color_continuous_scale="Blues",
        title=f"Water Security of {year}",
        range_color=(0, 100000),
        hover_name="country"
    )

    # Customizing the layout
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Water Per Capita",  # Custom title for the color bar
            title_side="top",  # Position of the title
        ),
        geo=dict(bgcolor="lightblue"),  # Ocean/background color
        paper_bgcolor="white"  # Set background outside the map
    )

    return fig
