#pip install wikitables --user
#pip install panda --user
#pip install currencyconverter -- user

from wikitables import import_tables
from pandas import pandas as pd
from pandas import DataFrame as df
import re
import sqlite3
from currency_converter import CurrencyConverter
c = CurrencyConverter('./eurofxref-hist.csv')
tables = import_tables('Farebox recovery ratio')
t = tables

#Treating Fare Rates
def dz(*dicts, **kwargs):
    fillvalue = kwargs.get('fillvalue', None)
    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d.get(k, fillvalue) for d in dicts] for k in all_keys}

currency = {'HKD': 'HK$', 'JPY': '\xc2\xa5', 'PKR': 'Rs', 'NTD': 'NT$', 'SGD': 'SG$', 'EUR': '\xe2\x82\xac', 'CZK': 'Kc', 'SEK': 'SEK', 'CHF': 'SFr.', 'USD': 'US', 'CAD': 'C$', 'AUD': 'A$'}
curr2 = {}
for key in currency.iterkeys():
    curr2[currency[key]] = key

def parse(row):
    key = ('{System}'.format(**row))
    if key.find('\xe2\x80\x93') != -1:
        key = key.replace('\xe2\x80\x93', '-')
    return key

system_currency = {}

for row in tables[0].rows:
    raw_rate = '{Fare rate}'.format(**row)
    for key in currency.iterkeys():
        if raw_rate.find(key) != -1:
            system_currency[parse(row)] = key
    for value in currency.itervalues():
        if raw_rate.find(value) != -1:
            system_currency[parse(row)] = curr2[value]

system_rate = {}
for row in tables[0].rows:
    raw_rate = '{Fare rate}'.format(**row)
    system_rates = re.findall(r"[-+]?\d*\.\d+|\d+", raw_rate)
    key = parse(row)
    if not system_rates:
        system_rate[key] = "N/A"
    else:
        system_rate[key] = system_rates[0]

system_rate_currency = dz(system_rate, system_currency)

clean_rate = {}
for key, value in system_rate_currency.items():
    if value[0] == "N/A" or value[1] is None:
        clean_rate[key] = "N/A"
    else:
        clean_rate[key] = round(c.convert(value[0], value[1], 'USD'),2)

#Treating Ratios
system_ratio = {}
for row in tables[0].rows:
    raw_ratio = '{Ratio}'.format(**row)
    pos = raw_ratio.find('%')
    clean_ratio = raw_ratio[:pos]
    system_ratio[('{System}'.format(**row))] = clean_ratio

#Treating Fare System
system_faresystem= {}
for row in tables[0].rows:
    raw_fare_system = '{Fare system}'.format(**row)
    b = [str.lower() for str in raw_fare_system]
    fare_system = "".join(b)
    system_faresystem['{System}'.format(**row)] = fare_system
    system_faresystem.update({'Paris (STIF)': 'variable rate'})
    system_faresystem.update({'Washington, DC (WMATA)': 'variable rate'})
    system_faresystem.update({'VIA Rail': 'variable rate'})
    system_faresystem.update({'Helsinki': 'zone based'})
    system_faresystem.update({'Vancouver TransLink': 'zone based'})
    system_faresystem.update({'Puget Sound Region (Sound Transit)': 'variable rate'})
    system_faresystem.update({'Minneapolis - St. Paul': 'flat rate'})
    system_faresystem.update({'Maryland': 'variable rate'})
    system_faresystem.update({'Santa Clara County (VTA)': 'variable rate'})
    system_faresystem.update({'Melbourne': 'variable rate'})
    system_faresystem.update({'Greater Seattle Area (King County Metro)': 'variable rate'})
    system_faresystem.update({'Amtrak': 'variable rate'})

#Creating Individual Dictionaries for Other Attributes
system_system = {}
for row in tables[0].rows:
    system_system[parse(row)] = parse(row)

system_continent = {}
for row in tables[0].rows:
    system_continent[parse(row)] = '{Continent}'.format(**row)

system_country = {}
for row in tables[0].rows:
    system_country[parse(row)] = '{Country}'.format(**row)

ds = [system_system, system_continent, system_country, system_ratio, system_faresystem, clean_rate]
db = {}
for k in clean_rate.iterkeys():
    db[k] = tuple(d[k] for d in ds)

#Export to DataFrame and SQL Database
farebox = sqlite3.connect('mydb.db')
data = df.from_dict(db, orient='index', dtype=None, columns = ['System', 'Continent', 'Country', 'Farebox_Ratio', 'Fare_System', 'Fare_Rate_USD'])
data.to_sql("FareBox", farebox, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
