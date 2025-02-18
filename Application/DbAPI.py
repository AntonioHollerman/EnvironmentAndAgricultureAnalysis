from sqlite3 import connect
import pandas as pd

conn = connect("..\\Data\\EnvironmentData.db")
cur = conn.cursor()

cur.execute("SELECT DISTINCT year FROM energy_security_predictions")
energy_prediction_years = [row[0] for row in cur.fetchall()]

cur.execute("SELECT DISTINCT year FROM water_security")
water_security_years = [row[0] for row in cur.fetchall()]

cur.execute("SELECT DISTINCT year FROM food_insecurity")
food_security_years = [row[0] for row in cur.fetchall()]

cur.execute("SELECT DISTINCT indicator FROM food_insecurity")
food_security_indicators = [row[0] for row in cur.fetchall()]

def get_2023_energy_security_df() -> pd.DataFrame:
    cur.execute("SELECT iso3c, percent_no_electricity, country FROM energy_security")
    data = [{"id": row[0], "percent_no_electricity": row[1], "country": row[2]} for row in cur.fetchall()]
    return pd.DataFrame(data)


def get_energy_predictions_df(year: int) -> pd.DataFrame:
    if year not in energy_prediction_years:
        raise Exception("Invalid year input")
    cur.execute("SELECT continent, ej_value FROM energy_security_predictions WHERE year = ?", (year,))
    data = [{"id": row[0], "ej_value": row[1]} for row in cur.fetchall()]
    return pd.DataFrame(data)


def get_food_insecurity_df(year: int, indicator: str = "Prevalence of Severe Food Insecurity (%)") -> pd.DataFrame:
    if year not in food_security_years:
        raise Exception("Invalid year input")
    cur.execute("SELECT year, iso3c, country, value FROM food_insecurity WHERE year = ? AND indicator = ?",
                (year, indicator))
    data = [{"year": row[0], "id": row[1], "country": row[2], "value": row[3]} for row in cur.fetchall()]
    return pd.DataFrame(data)


def get_water_security_df(year: int) -> pd.DataFrame:
    cur.execute("SELECT iso3c, water_per_capita, country FROM water_security WHERE year = ?", (year,))
    data = [{"id": row[0], "water_per_capita": row[1], "country": row[2]} for row in cur.fetchall()]
    return pd.DataFrame(data)


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
