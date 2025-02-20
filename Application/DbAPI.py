from sqlite3 import connect  # Importing SQLite module to connect to the database
import pandas as pd  # Importing pandas for data manipulation and DataFrame creation

# Establishing a global connection to the database
global_conn = connect("EnvironmentData.db")
global_cur = global_conn.cursor()

# Retrieving distinct years from the energy security predictions table
global_cur.execute("SELECT DISTINCT year FROM energy_security_predictions")
energy_prediction_years = [row[0] for row in global_cur.fetchall()]

# Retrieving distinct years from the water security table
global_cur.execute("SELECT DISTINCT year FROM water_security")
water_security_years = [row[0] for row in global_cur.fetchall()]

# Retrieving distinct years from the food insecurity table
global_cur.execute("SELECT DISTINCT year FROM food_insecurity")
food_security_years = [row[0] for row in global_cur.fetchall()]

# Retrieving distinct food insecurity indicators
global_cur.execute("SELECT DISTINCT indicator FROM food_insecurity")
food_security_indicators = [row[0] for row in global_cur.fetchall()]



def get_2023_energy_security_df() -> pd.DataFrame:
    """
    Retrieves energy security data for 2023, including the percentage of people without electricity
    for each country.

    Returns:
        pd.DataFrame: A DataFrame containing the columns:
                      - id (ISO3 country code)
                      - percent_no_electricity (percentage of population without electricity)
                      - country (country name)
    """
    conn = connect("EnvironmentData.db")
    cur = conn.cursor()

    # Fetching energy security data
    cur.execute("SELECT iso3c, percent_no_electricity, country FROM energy_security")
    data = [{"id": row[0], "percent_no_electricity": row[1], "country": row[2]} for row in cur.fetchall()]

    return pd.DataFrame(data)


def get_energy_predictions_df(year: int) -> pd.DataFrame:
    """
    Retrieves energy security predictions for a given year.

    Args:
        year (int): The year for which predictions are needed.

    Returns:
        pd.DataFrame: A DataFrame containing the columns:
                      - id (continent name)
                      - ej_value (energy consumption in exajoules)

    Raises:
        Exception: If the given year is not available in the dataset.
    """
    conn = connect("EnvironmentData.db")
    cur = conn.cursor()

    # Validate year input
    if year not in energy_prediction_years:
        raise Exception("Invalid year input")

    # Fetching energy security predictions
    cur.execute("SELECT continent, ej_value FROM energy_security_predictions WHERE year = ?", (year,))
    data = [{"id": row[0], "ej_value": row[1]} for row in cur.fetchall()]

    return pd.DataFrame(data)


def get_food_insecurity_df(year: int, indicator: str = "Prevalence of Severe Food Insecurity (%)") -> pd.DataFrame:
    """
    Retrieves food insecurity data for a given year and indicator.

    Args:
        year (int): The year for which food insecurity data is needed.
        indicator (str, optional): The specific food insecurity indicator. Defaults to
                                   "Prevalence of Severe Food Insecurity (%)".

    Returns:
        pd.DataFrame: A DataFrame containing the columns:
                      - year (year of data)
                      - id (ISO3 country code)
                      - country (country name)
                      - value (indicator value)

    Raises:
        Exception: If the given year is not available in the dataset.
    """
    conn = connect("EnvironmentData.db")
    cur = conn.cursor()

    # Validate year input
    if year not in food_security_years:
        raise Exception("Invalid year input")

    # Fetching food insecurity data
    cur.execute("SELECT year, iso3c, country, value FROM food_insecurity WHERE year = ? AND indicator = ?",
                (year, indicator))
    data = [{"year": row[0], "id": row[1], "country": row[2], "value": row[3]} for row in cur.fetchall()]


    return pd.DataFrame(data)


def get_water_security_df(year: int) -> pd.DataFrame:
    """
    Retrieves water security data for a given year.

    Args:
        year (int): The year for which water security data is needed.

    Returns:
        pd.DataFrame: A DataFrame containing the columns:
                      - id (ISO3 country code)
                      - water_per_capita (amount of water per capita)
                      - country (country name)
    """
    conn = connect("EnvironmentData.db")
    cur = conn.cursor()

    # Fetching water security data
    cur.execute("SELECT iso3c, water_per_capita, country FROM water_security WHERE year = ?", (year,))
    data = [{"id": row[0], "water_per_capita": row[1], "country": row[2]} for row in cur.fetchall()]


    return pd.DataFrame(data)


# Dictionary mapping country names to their ISO3 codes
iso3_dict = {
    "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA", "Andorra": "AND", "Angola": "AGO",
    "Antigua and Barbuda": "ATG", "Argentina": "ARG", "Armenia": "ARM", "Australia": "AUS", "Austria": "AUT",
    "Azerbaijan": "AZE", "Bahamas, The": "BHS", "Bahrain": "BHR", "Bangladesh": "BGD", "Barbados": "BRB",
    "Belarus": "BLR", "Belgium": "BEL", "Belize": "BLZ", "Benin": "BEN", "Bhutan": "BTN",
    "Bolivia": "BOL", "Bosnia and Herzegovina": "BIH", "Botswana": "BWA", "Brazil": "BRA", "Brunei Darussalam": "BRN",
    "Bulgaria": "BGR", "Burkina Faso": "BFA", "Burundi": "BDI", "Cabo Verde": "CPV", "Cambodia": "KHM",
    "Cameroon": "CMR", "Canada": "CAN", "Central African Republic": "CAF", "Chad": "TCD", "Chile": "CHL",
    "China": "CHN", "Colombia": "COL", "Comoros": "COM", "Congo, Dem. Rep.": "COD", "Congo, Rep.": "COG",
    "Costa Rica": "CRI", "Cote d'Ivoire": "CIV", "Croatia": "HRV", "Cuba": "CUB", "Czech Republic": "CZE",
    "Denmark": "DNK", "Djibouti": "DJI", "Dominica": "DMA", "Dominican Republic": "DOM", "Ecuador": "ECU",
    "Egypt, Arab Rep.": "EGY", "El Salvador": "SLV", "Equatorial Guinea": "GNQ", "Eritrea": "ERI", "Estonia": "EST",
    "Eswatini": "SWZ", "Ethiopia": "ETH", "Fiji": "FJI", "Finland": "FIN", "France": "FRA",
    "Gabon": "GAB", "Gambia, The": "GMB", "Georgia": "GEO", "Germany": "DEU", "Ghana": "GHA",
    "Greece": "GRC", "Grenada": "GRD", "Guatemala": "GTM", "Guinea": "GIN", "Guinea-Bissau": "GNB",
    "Guyana": "GUY", "Haiti": "HTI", "Honduras": "HND", "Hungary": "HUN", "Iceland": "ISL",
    "India": "IND", "Indonesia": "IDN", "Iran, Islamic Rep.": "IRN", "Iraq": "IRQ", "Ireland": "IRL",
    "Israel": "ISR", "Italy": "ITA", "Jamaica": "JAM", "Japan": "JPN", "Jordan": "JOR",
    "Kazakhstan": "KAZ", "Kenya": "KEN", "Korea, Rep.": "KOR", "Kuwait": "KWT", "Kyrgyz Republic": "KGZ",
    "Lao PDR": "LAO", "Latvia": "LVA", "Lebanon": "LBN", "Lesotho": "LSO", "Liberia": "LBR",
    "Libya": "LBY", "Lithuania": "LTU", "Luxembourg": "LUX", "Macedonia, FYR": "MKD", "Madagascar": "MDG",
    "Malawi": "MWI", "Malaysia": "MYS", "Maldives": "MDV", "Mali": "MLI", "Malta": "MLT",
    "Mauritania": "MRT", "Mauritius": "MUS", "Mexico": "MEX", "Moldova": "MDA", "Mongolia": "MNG",
    "Morocco": "MAR", "Mozambique": "MOZ", "Myanmar": "MMR", "Namibia": "NAM", "Nepal": "NPL",
    "Netherlands": "NLD", "New Zealand": "NZL", "Nicaragua": "NIC", "Niger": "NER", "Nigeria": "NGA",
    "Norway": "NOR", "Oman": "OMN", "Pakistan": "PAK", "Panama": "PAN", "Papua New Guinea": "PNG",
    "Paraguay": "PRY", "Peru": "PER", "Philippines": "PHL", "Poland": "POL", "Portugal": "PRT",
    "Puerto Rico": "PRI", "Qatar": "QAT", "Romania": "ROU", "Russian Federation": "RUS", "Rwanda": "RWA",
    "Sao Tome and Principe": "STP", "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia": "SRB", "Sierra Leone": "SLE",
    "Singapore": "SGP", "Slovak Republic": "SVK", "Slovenia": "SVN", "Solomon Islands": "SLB", "South Africa": "ZAF",
    "Spain": "ESP", "Sri Lanka": "LKA", "St. Kitts and Nevis": "KNA", "St. Lucia": "LCA", "St. Vincent and the Grenadines": "VCT",
    "Sudan": "SDN", "Suriname": "SUR", "Sweden": "SWE", "Switzerland": "CHE", "Tajikistan": "TJK",
    "Tanzania": "TZA", "Thailand": "THA", "Timor-Leste": "TLS", "Togo": "TGO", "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN", "Turkey": "TUR", "Turkmenistan": "TKM", "Uganda": "UGA", "Ukraine": "UKR",
    "United Arab Emirates": "ARE", "United Kingdom": "GBR", "United States": "USA", "Uruguay": "URY", "Uzbekistan": "UZB",
    "Vanuatu": "VUT", "Venezuela, RB": "VEN", "Vietnam": "VNM", "West Bank and Gaza": "PSE", "Yemen, Rep.": "YEM",
    "Zambia": "ZMB", "Zimbabwe": "ZWE"
}
