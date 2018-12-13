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

def dict_zip(*dicts, **kwargs):
    fillvalue = kwargs.get('fillvalue', None)
    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d.get(k, fillvalue) for d in dicts] for k in all_keys}

#Treating Fare Rates
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
for row in tables[0].rows:
    raw_ratio = '{Ratio}'.format(**row)
    pos = raw_ratio.find('%')
    clean_ratio = raw_ratio[:pos]

#Treating Fare System

#Creating Individual Dictionaries
system_continent = {}
for row in tables[0].rows:
    system_continent[parse(row)] = '{Continent}'.format(**row)

system_country = {}
for row in tables[0].rows:
    system_country[parse(row)] = '{Country}'.format(**row)
    
system_rate = {}
for row in tables[0].rows:
    system_rate[parse(row)] = clean_rate 

system_ratio = {}
for row in tables[0].rows:
    system_ratio[parse(row)] = clean_ratio 

#Merging Dictionaries
print(dict_zip(system_continent, system_country, system_rate, system_ratio))

#Export to DataFrame and SQL Database


#From SQL to RStudio 
con = dbconnect(drv=SQLite(), dbname=“rates.db”)
df.ratios <- dbGetQuery(con, “SELECT * FROM systems”)
df.summary <- dbGetQuery(con, “SELECT AVG(ratio) AS avg_ratio FROM systems GROUP BY continent”) #example

ggplot(data= df.ratios, aes(x=ratio)) +
	geom_density() + 
	geom_vline(intercept = mean(df.ratios

