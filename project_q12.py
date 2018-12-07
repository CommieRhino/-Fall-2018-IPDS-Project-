#pip install wikitables --user
#pip install panda --user
#pip install currencyconverter -- user

from wikitables import import_tables
from currency_converter import CurrencyConverter as c
import pandas as pd
tables = import_tables('Farebox recovery ratio')
t = tables

#Treating Fare Rates
currency = {'HKD': 'HK$', 'YEN': '\xc2\xa5', 'PKR': 'PKR', 'NTD': 'NT$', 'SGD': 'SGD', 'EUR': '\xe2\x82\xac', 'CZK': 'CZK', 'SEK': 'SEK', 'CHF': 'CHF', 'USD': 'US$', 'CAN': 'C$', 'AUD': 'A$'}

system_og_currency = {}
for row in tables[0].rows:
    raw_rate = '{Fare rate}'.format(**row)
    for key in currency.iterkeys():
        if raw_rate.find(key) != -1:
            system_og_currency['{System}'.format(**row)] = key
    for value in currency.itervalues():
        if raw_rate.find(value) != -1:
            system_og_currency['{System}'.format(**row)] = key

print(system_og_currency)
#Treating Ratios

#Treating Fare System

#Creating Individual Dictionaries
system_continent = {}
for row in tables[0].rows:
    system_continent['{System}'.format(**row)] = '{Continent}'.format(**row)

system_country = {}

system_rate = {}
for row in tables[0].rows:
    system_rate['{System}'.format(**row)] = '{Fare rate}'.format(**row)

system_ratio = {}
for row in tables[0].rows:
    raw_ratio = '{Ratio}'.format(**row)
    clean_ratio = raw_ratio.rstrip('%')
    system_ratio['{System}'.format(**row)] = clean_ratio
    #print(clean_ratio)

#Merging Dictionaries
def dict_zip(*dicts, **kwargs):
    fillvalue = kwargs.get('fillvalue', None)
    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d.get(k, fillvalue) for d in dicts] for k in all_keys}

#Print(dict_zip(system_rate, system_ratio))

#Export to DataFrame and SQL Database
