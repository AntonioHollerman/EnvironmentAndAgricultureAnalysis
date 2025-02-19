from Visualizations import *  # Import visualization functions
import plotly.express as px  # Import Plotly Express for visualization

# Maximum length for displaying region names
MAX_REGION_LEN = 15

# Mapping for value descriptions in different visualizations
map_value = {
    "water": "Cubic Meters of Water",
    "food": "Experiencing Food Insecurity",
    "electricity": "EJ Output"
}

# Mapping for the type of regions used in different datasets
map_region = {
    "water": "Country",
    "food": "Country",
    "electricity": "Region"
}

# Descriptions of the datasets used for each category
data_desc = {
    "water": "The data presented was gathered from \"World Bank Group\". The metrics used to describe water security is "
             "\"Water Per Capita\" in cubic meters, which represents the total fresh renewable water available per person. "
             "Calculated from 'Total Renewable Water' divided by 'Total Population'.",

    "food": "The data presented was gathered from \"World Bank Group\". The metric used to describe food security is "
            "the \"Prevalence of Severe Food Insecurity,\" which represents the percentage of households experiencing "
            "severe food insecurity. A household is classified as severely food insecure if one or more adults go hungry "
            "for one or more days.",

    "electricity": "The data presented was gathered by \"IEA\". The metric used is the total energy supply (EJ) a region "
                   "produces. Data was collected through household surveys, and values were estimated using modeling."
}

# Citation sources for each dataset
data_citation = {
    "water": """The World Bank
    Renewable internal freshwater resources per capita (cubic meters)
    Accessed January 20, 2025. https://data.worldbank.org/indicator/ER.H2O.INTR.PC
    files: water-data.csv""",

    "food": """The World Bank
    World Food Security Outlook
    Accessed January 20, 2025. https://microdata.worldbank.org/index.php/catalog/6103/get-microdata,
    files: Files found in "FoodSecurity" folder""",

    "electricity": """IEA, SDG7 Database, IEA, Paris
    Accessed January 20, 2025. https://www.iea.org/data-and-statistics/data-product/sdg7-database, Licence: CC BY 4.0
    files: WEO2024_AnnexA_Free_Dataset_Regions.csv, WEO2024_AnnexA_Free_Dataset_World.csv"""
}

# Mapping datasets to available years
data_range = {
    "water": water_security_years,
    "food": food_security_years,
    "electricity": energy_prediction_years
}


class RegionRank:
    """
    Represents a ranked region with a corresponding value for sorting and comparison.

    Attributes:
        region (str): The name of the region (country or continent).
        value (float): The numerical value associated with the region (e.g., water per capita, food insecurity %).
        value_d (str): A formatted string representation of the value for display.
    """

    def __init__(self, region, value, value_d):
        self.region = region  # Region name
        self.value = value  # Numerical value (e.g., EJ output, water per capita)
        self.value_d = value_d  # Formatted display value (e.g., "30.5%")

    def __eq__(self, other):
        """Equality comparison based on value."""
        if isinstance(other, RegionRank):
            return self.value == other.value
        return False

    def __lt__(self, other):
        """Less-than comparison for sorting based on value."""
        if isinstance(other, RegionRank):
            return self.value < other.value
        return False

    def __le__(self, other):
        """Less-than or equal comparison."""
        return self == other or self < other

    def __gt__(self, other):
        """Greater-than comparison."""
        return not self <= other

    def __ge__(self, other):
        """Greater-than or equal comparison."""
        return not self < other


def get_viz(graph: str, year: int):
    """
    Returns the appropriate visualization based on the selected dataset.

    Args:
        graph (str): The type of visualization ("water", "food", or "electricity").
        year (int): The year for which data should be visualized.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object for the selected dataset.
        If an invalid dataset is provided, returns an empty Plotly line chart.
    """
    try:
        if graph == "water":
            return water_security_viz(year)
        elif graph == "food":
            return food_security_viz(year)
        elif graph == "electricity":
            return energy_predictions_viz(year)
        else:
            return None
    except Exception as e:
        print("Get Viz Failed: " + e.__str__())
        return px.line()  # Return an empty line plot in case of failure


def get_rank(graph: str, year: int):
    """
    Retrieves and ranks regions based on the selected dataset.

    Args:
        graph (str): The type of ranking dataset ("water", "food", or "electricity").
        year (int): The year for which rankings should be retrieved.

    Returns:
        list[RegionRank]: A sorted list of `RegionRank` objects.
        If an error occurs, returns an empty list.
    """
    try:
        if graph == "water":
            regions = []
            df = get_water_security_df(year)

            for index, row in df.iterrows():
                regions.append(RegionRank(
                    format_region(row["country"]),
                    row["water_per_capita"],
                    str(round(row["water_per_capita"]))
                ))
            return sorted(regions)

        if graph == "food":
            regions = []
            df = get_food_insecurity_df(year)

            for index, row in df.iterrows():
                regions.append(RegionRank(
                    format_region(row["country"]),
                    row["value"],
                    f"{row['value']:.1f}%"
                ))
            return sorted(regions, reverse=True)  # Sorting in descending order for food insecurity

        if graph == "electricity":
            regions = []
            df = get_energy_predictions_df(year)

            for index, row in df.iterrows():
                regions.append(RegionRank(
                    format_region(row["id"]),
                    row["ej_value"],
                    f"{row['ej_value']:.2f}"
                ))
            return sorted(regions)

        return None
    except Exception as e:
        print("Get Rank Failed: " + e.__str__())
        return []  # Return an empty list in case of failure


def format_region(region: str) -> str:
    """
    Formats a region name to ensure it does not exceed the maximum display length.

    Args:
        region (str): The region name.

    Returns:
        str: The formatted region name, truncated if necessary.
    """
    if len(region) > MAX_REGION_LEN:
        return region[:MAX_REGION_LEN] + "..."  # Truncate and add ellipsis
    return region
