import pandas as pd
from pandas_datareader.data import DataReader
from datetime import datetime
import matplotlib.pyplot as plt
import mplcursors

# ------------
# 1. download
# ------------
start = '1996-02-01'
fred_series = [
    'DCPF3M',               # CP
    'IR3TCD01USM156N',      # CDs
    #'IR3TED01USM156N',      # Eurodollar/YCD
    # 'SNDR',                 # deposit rate
    #'BAMLC1A0C13YEY',       # short-corp bonds
    'TB3MS'                 # 3-month T-bill for TED
]

df = DataReader(fred_series, 'fred', start)

# 2. basic cleaning
# forward-fill the monthly data so everything is daily
df = df.ffill()

# 3. stitch the “pseudo-BSBY” (all rates are already % p.a. on A/360 or A/365 basis)
weights = {
    'DCPF3M':0.55,
    'IR3TCD01USM156N':0.45,
    #'IR3TED01USM156N':0.15,
    # 'SNDR':0.05,
    #'BAMLC1A0C13YEY':0.01
}

df['BSBY_proxy_3M'] = sum(df[s]*w for s,w in weights.items())

# 4. new TED spread
df['TED_new'] = df['BSBY_proxy_3M'] - df['TB3MS']

# 5. Save data to csv
df.to_csv('output.csv', index=True)

# 6. create a plot of the TED Spread Continued
df_plot = df[['TED_new']].dropna()


line, = plt.plot(df_plot.index, df_plot['TED_new'], label='TED Spread (Continued)')

plt.title('TED Spread (Continued)')
plt.xlabel('Date')
plt.ylabel('Spread (%)')
plt.grid(True)
plt.legend()
plt.tight_layout()
mplcursors.cursor(line, hover=True)
plt.show()