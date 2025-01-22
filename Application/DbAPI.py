from sqlite3 import connect
import pandas as pd

conn = connect("..\\Data\\EnvironmentData.db")
cur = conn.cursor()

cur.execute("SELECT DISTINCT year FROM energy_security_predictions")
energy_prediction_years = [row[0] for row in cur.fetchall()]

cur.execute("SELECT DISTINCT year FROM food_insecurity")
food_security_years = [row[0] for row in cur.fetchall()]

def get_2023_energy_security_df() -> pd.DataFrame:
    cur.execute("SELECT country, percent_no_electricity FROM energy_security")
    data = [{"country": row[0], "percent_no_electricity": row[1]} for row in cur.fetchall()]
    return pd.DataFrame(data)


def get_energy_predictions_by_year(year: int) -> pd.DataFrame:
    if year not in energy_prediction_years:
        raise Exception("Invalid year input")
    cur.execute("SELECT country, ej_value FROM energy_security_predictions")
    data = [{"country": row[0], "ej_value": row[1]} for row in cur.fetchall()]
    return pd.DataFrame(data)


def get_food_insecurity_by_year(year: int) -> pd.DataFrame:
    if year not in food_security_years:
        raise Exception("Invalid year input")
    cur.execute("SELECT year, iso3c, country, value FROM food_insecurity")
    data = [{"year": row[0], "iso3c": row[1], "country": row[2], "value": row[3]} for row in cur.fetchall()]
    return pd.DataFrame(data)


def get_2022_water_security() -> pd.DataFrame:
    cur.execute("SELECT country, water_per_capita FROM water_security")
    data = [{"country": row[0], "water_per_capita": row[1]} for row in cur.fetchall()]
    return pd.DataFrame(data)
