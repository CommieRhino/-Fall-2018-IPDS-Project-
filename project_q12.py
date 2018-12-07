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
curr2 = {}
for key in currency.iterkeys():
    curr2[currency[key]] = key
    
system_og_currency = {}
for row in tables[0].rows:
    raw_rate = '{Fare rate}'.format(**row)
    for key in currency.iterkeys():
        if raw_rate.find(key) != -1:
            system_og_currency['{System}'.format(**row)] = key
    for value in currency.itervalues():
        if raw_rate.find(value) != -1:
            system_og_currency['{System}'.format(**row)] = curr2[value]
            
a = '{Fare rate}'.format(**row)
result = re.findall(r"[-+]?\d*\.\d+|\d+", a)

scores = [10, 12, 43, 65]

def SumScores(scores):
    running_sum = 0
    for score in scores:
        running_sum += score
    return (1.0 * running_sum)

def AvgScores(scores):
    return SumScores(scores)/len(scores)

#Treating Ratios
for row in tables[0].rows:
    raw_ratio = '{Ratio}'.format(**row)
    pos = raw_ratio.find('%')
    clean_ratio = raw_ratio[:pos]

#Treating Fare System

#Creating Individual Dictionaries
system_continent = {}
for row in tables[0].rows:
    system_continent['{System}'.format(**row)] = '{Continent}'.format(**row)

system_country = {}
for row in tables[0].rows:
    system_country['{System}'.format(**row)] = '{Country}'.format(**row)
    
system_rate = {}
for row in tables[0].rows:
    system_rate['{System}'.format(**row)] = '{Fare rate}'.format(**row)

system_ratio = {}
for row in tables[0].rows:
    system_ratio['{System}'.format(**row)] = clean_ratio 

#Merging Dictionaries
def dict_zip(*dicts, **kwargs):
    fillvalue = kwargs.get('fillvalue', None)
    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d.get(k, fillvalue) for d in dicts] for k in all_keys}

print(dict_zip(system_rate, system_ratio))

#Export to DataFrame and SQL Database
