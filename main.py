import pandas as pd
from pandas_datareader.data import DataReader
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# ------------
# 1. download
# ------------
start = '2021-04-01'
fred_series = [
    'DCPF3M',               # CP
    'IR3TCD01USM156N',      # CDs
    'IR3TED01USM156N',      # Eurodollar/YCD
    # 'SNDR',                 # deposit rate
    'BAMLC1A0C13YEY',       # short-corp bonds
    'TB3MS'                 # 3-month T-bill for TED
]

df = DataReader(fred_series, 'fred', start)

# 2. basic cleaning
# forward-fill the monthly data so everything is daily
df = df.ffill()

# 3. stitch the “pseudo-BSBY” (all rates are already % p.a. on A/360 or A/365 basis)
weights = {
    'DCPF3M':0.45,
    'IR3TCD01USM156N':0.38,
    'IR3TED01USM156N':0.15,
    # 'SNDR':0.05,
    'BAMLC1A0C13YEY':0.01
}

df['BSBY_proxy_3M'] = sum(df[s]*w for s,w in weights.items())

# 4. new TED spread
df['TED_new'] = df['BSBY_proxy_3M'] - df['TB3MS']

# 5. inspect the latest value
print(df[['BSBY_proxy_3M','TB3MS','TED_new']].dropna().tail())

df.to_csv('output.csv', index=True)
