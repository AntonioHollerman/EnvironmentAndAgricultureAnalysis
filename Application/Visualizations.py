from Application.DbAPI import *
import json
import plotly.express as px

continents_geo = json.load(open("..\\Data\\GeoJson\\continents.geojson"))
for feature in continents_geo["features"]:
    feature["id"] = feature["properties"]["CONTINENT"]

countries_geo = json.load(open("..\\Data\\GeoJson\\countries.json"))
for feature in countries_geo["features"]:
    feature["id"] = feature["properties"]["ISO_A3"]


def energy_predictions_viz(year: int):
    energy_predictions_df = get_energy_predictions_by_year(year)
    fig = px.choropleth(energy_predictions_df,
                        locations='id',
                        geojson=continents_geo,
                        color="ej_value",
                        scope="world",
                        color_continuous_scale=["#ffffff", "#fff5cc", "#ffeb99", "#ffd700", "#b8860b"],
                        title=f"Energy Security Predictions of {year}",
                        range_color=(0, 100),
                        hover_name="id"
                        )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="EJ Output",  # Custom title for the color bar
            title_side="top",  # Position of the title (default is 'right')
        ),
        geo=dict(
            bgcolor="lightblue",  # Change ocean/background color
        ),
        paper_bgcolor="white"  # Set background outside the map
    )
    return fig



def food_security_viz(year: int):
    food_df = get_food_insecurity_by_year(year)
    million = 1_000_000
    fig = px.choropleth(food_df,
                        locations='id',
                        geojson=countries_geo,
                        color="value",
                        scope="world",
                        color_continuous_scale=["#ffffff", "#ffe5e5", "#ff9999", "#ff4d4d", "#800000"],
                        title=f"Food Security of {year}",
                        hover_name="country",
                        range_color=(0, 2 * million)
                        )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Number of Calories Needed to Feed the Hungry",  # Custom title for the color bar
            title_side="top",  # Position of the title (default is 'right')
        ),
        paper_bgcolor="white",  # Set background outside the map
        geo=dict(bgcolor="lightblue"),  # Ocean/background color,
    )
    return fig

def water_security_viz(year: int):
    water_df = get_water_security(year)
    fig = px.choropleth(water_df,
                        locations='id',
                        geojson=countries_geo,
                        color="water_per_capita",
                        scope="world",
                        color_continuous_scale=["#ffffff", "#d6eaff", "#88cfff", "#1f77b4", "#08306b"],
                        title=f"Water Security of {year}",
                        range_color=(0, 100000),
                        hover_name="country"
                        )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Water Per Capita",  # Custom title for the color bar
            title_side="top",  # Position of the title (default is 'right')
        ),
        geo=dict(bgcolor="lightblue"),  # Ocean/background color,
        paper_bgcolor="white"
    )
    return fig