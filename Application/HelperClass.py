from Visualizations import *

data_desc = {
    "water": "The data presented was gathered from \"World Bank Group\". The metrics used to describe water security is "
             "\"Water Per Capita\" in cubic meters which is the total fresh renewable water available per person. "
             "Calculated from 'Total Renewable Water' divided by 'total population'",
    "food": "The data presented was gathered from \"World Bank Group\". The metrics used to describe food security is "
            "is the \"Prevalence of Severe Food Insecurity\" which is the the percentage of house holds experience "
            "severe food insecurity. A household is flagged for severe food insecurity if one or more adults goes hungry "
            "for one or more days",
    "electricity": "The data presented was gathered by \"IEA\". The metric used is the total energy supple of EJ a region "
                   "produces. Data was collected through surveying households then values estimated using modeling."
}

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

data_range = {
    "water": water_security_years,
    "food": food_security_years,
    "electricity": energy_prediction_years
}

class RegionRank:
    def __init__(self, region, value):
        self.region = region
        self.value = value

    def __eq__(self, other):
        if isinstance(other, RegionRank):
            return self.value == other.value
        return False

    def __lt__(self, other):
        if isinstance(other, RegionRank):
            return self.value < other.value
        return False

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other


def get_viz(graph: str, year: int):
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
        return px.line()

def get_rank(graph: str, year: int):
    try:
        if graph == "water":
            regions = []
            df = get_water_security_df(year)

            for index, row in df.iterrows():
                regions.append(RegionRank(row["country"], row["water_per_capita"]))
            return sorted(regions, reverse=True)

        if graph == "food":
            regions = []
            df = get_food_insecurity_df(year)

            for index, row in df.iterrows():
                regions.append(RegionRank(row["country"], row["value"]))
            return sorted(regions)

        if graph == "electricity":
            regions = []
            df = get_energy_predictions_df(year)

            for index, row in df.iterrows():
                regions.append(RegionRank(row["id"], row["ej_value"]))
            return sorted(regions, reverse=True)

        return None
    except Exception as e:
        print("Get Rank Failed: " + e.__str__())
        return []
