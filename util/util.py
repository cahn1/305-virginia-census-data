import json
import pandas as pd


fips_master = pd.read_csv('resources/county_fips_master.csv')[
    ['fips', 'county_name']]
county_fips = json.loads(fips_master.to_json(orient='records'))
fips = fips_master.rename(
    columns={'fips': 'FIPS', 'county_name': 'County'})

def pick_options(df):
    valid_options = []
    for col in df:
        if df[col].dtype == float or df[col].dtype == int:
            valid_options.append(col)
    return valid_options


def pick_fip(county):
    for record in county_fips:
        if record.get('county_name', '').lower() == county.lower():
            return str(record.get('fips', '')).zfill(5)
    return ''


def find_fip(county):
    return fips[fips['County'] == county]['FIPS']
