"""
Google Trends and Market Data Analysis using Pandas and Matplotlib

This project demonstrates how to:
1. Read multiple CSV datasets.
2. Explore and clean data.
3. Handle missing values.
4. Convert string dates to datetime.
5. Resample daily Bitcoin prices into monthly data.
6. Analyze Tesla search trends vs stock prices.
7. Analyze Bitcoin search trends vs Bitcoin prices.
8. Analyze unemployment search trends vs unemployment rate.
9. Calculate rolling averages.
10. Visualize relationships using dual-axis charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ============================ LOAD DATASETS ============================ #

df_tesla = pd.read_csv("TESLA Search Trend vs Price.csv")
df_btc_search = pd.read_csv("Bitcoin Search Trend.csv")
df_btc_price = pd.read_csv("Daily Bitcoin Price.csv")
df_unemployment = pd.read_csv("UE Benefits Search vs UE Rate 2004-19.csv")

# ============================ TESLA DATASET ============================ #


print("TESLA DATASET")
print()

print("First 5 Rows")
print(df_tesla.head())

print("\nLast 5 Rows")
print(df_tesla.tail())

print("\nDataset Shape")
print(df_tesla.shape)

print("\nColumns")
print(df_tesla.columns)

print("\nHighest Tesla Web Search")
print(df_tesla.TSLA_WEB_SEARCH.max())

print("\nLowest Tesla Web Search")
print(df_tesla.TSLA_WEB_SEARCH.min())

print("\nStatistical Summary")
print(df_tesla.describe())


# ============================ UNEMPLOYMENT DATASET ============================ #

print()
print("UNEMPLOYMENT DATASET")
print()

print("Dataset Shape")
print(df_unemployment.shape)

print("\nFirst 5 Rows")
print(df_unemployment.head())

print("\nLast 5 Rows")
print(df_unemployment.tail())

print("\nColumns")
print(df_unemployment.columns)

print("\nMaximum Web Search")
print(df_unemployment.UE_BENEFITS_WEB_SEARCH.max())

print("\nStatistical Summary")
print(df_unemployment.describe())


# ============================ BITCOIN PRICE DATASET ============================ #

print()
print("BITCOIN PRICE DATASET")
print()

print(df_btc_price.head())

print("\nLast 5 Rows")
print(df_btc_price.tail())

print("\nShape")
print(df_btc_price.shape)

print("\nSummary")
print(df_btc_price.describe())


# ============================ BITCOIN SEARCH DATASET ============================ #

print()
print("BITCOIN SEARCH TREND DATASET")
print()

print(df_btc_search.head())

print("\nLast 5 Rows")
print(df_btc_search.tail())

print("\nShape")
print(df_btc_search.shape)

print("\nMaximum Search Volume")
print(df_btc_search.BTC_NEWS_SEARCH.max())

print("\nSummary")
print(df_btc_search.describe())


# ============================ MISSING VALUES ============================ #

print()
print("CHECKING MISSING VALUES")
print()

print("Tesla")
print(df_tesla.isna().any())

print("\nUnemployment")
print(df_unemployment.isna().any())

print("\nBitcoin Search")
print(df_btc_search.isna().any())

print("\nBitcoin Price")
print(df_btc_price.isna().any())

print("\nTotal Missing Values")
print(df_btc_price.isna().sum().sum())

print("\nRows Containing Missing Values")
print(df_btc_price[df_btc_price["CLOSE"].isna()])


# ============================ DATA CLEANING ============================ #

"""
Remove rows that contain missing values
from the Bitcoin price dataset.
"""

df_btc_price.dropna(inplace=True)

print("\nMissing Values After Cleaning")
print(df_btc_price.isna().any())


# ============================ DATE CONVERSION ============================ #

"""
Convert date columns into datetime format.
"""


print(type(df_tesla["MONTH"][0]))
print(type(df_unemployment["MONTH"][0]))
print(type(df_btc_price["DATE"][0]))
print(type(df_btc_search["MONTH"][0]))

df_tesla["MONTH"] = pd.to_datetime(df_tesla["MONTH"])
df_unemployment["MONTH"] = pd.to_datetime(df_unemployment["MONTH"])
df_btc_search["MONTH"] = pd.to_datetime(df_btc_search["MONTH"])
df_btc_price["DATE"] = pd.to_datetime(df_btc_price["DATE"])




# ============================ MONTHLY BITCOIN DATA ============================ #

"""
Convert daily Bitcoin prices
into monthly prices.
"""

df_btc_price_monthly = (df_btc_price.resample(rule="ME", on="DATE").last())

print("\nMonthly Bitcoin Dataset")
print(df_btc_price_monthly.head())

print(df_btc_price_monthly.shape)


# ============================ DATE FORMATTERS ============================ #

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter("%Y")


# ============================ TESLA VISUALIZATION ============================ #

plt.figure(figsize=(14, 8), dpi=120)

plt.title("Tesla Web Search vs Tesla Stock Price")

plt.xticks(rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_xlabel("Months", fontsize=14)

ax1.set_ylabel(
    "Tesla Web Search",
    color="blue",
    fontsize=14
)

ax2.set_ylabel(
    "Tesla Stock Price",
    color="red",
    fontsize=14
)

ax1.set_xlim(
    df_tesla.MONTH.min(),
    df_tesla.MONTH.max()
)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.plot(
    df_tesla.MONTH,
    df_tesla.TSLA_WEB_SEARCH,
    color="blue",
    linewidth=2
)

ax2.plot(
    df_tesla.MONTH,
    df_tesla.TSLA_USD_CLOSE,
    color="red",
    linewidth=2
)



plt.show()


# ============================ BITCOIN VISUALIZATION ============================ #

plt.figure(figsize=(14, 8), dpi=120)

plt.title("Bitcoin Search Trend vs Bitcoin Price")

plt.xticks(rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_xlabel("Months", fontsize=14)

ax1.set_ylabel(
    "Bitcoin Search",
    color="blue",
    fontsize=14
)

ax2.set_ylabel(
    "Bitcoin Price",
    color="red",
    fontsize=14
)

ax1.set_xlim(
    df_btc_price_monthly.index.min(),
    df_btc_price_monthly.index.max()
)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.plot(
    df_btc_price_monthly.index,
    df_btc_price_monthly.VOLUME,
    color="blue",
    linewidth=2,
    linestyle="--"
)

ax2.plot(
    df_btc_price_monthly.index,
    df_btc_price_monthly.CLOSE,
    color="red",
    linewidth=2,
    marker="o"
)

plt.show()


# ============================ UNEMPLOYMENT ANALYSIS ============================ #

plt.figure(figsize=(14, 8), dpi=120)

plt.title("Unemployment Benefits Search vs Unemployment Rate")

plt.xticks(rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_xlabel("Months", fontsize=14)

ax1.set_ylabel(
    "Benefit Searches",
    color="blue",
    fontsize=14
)

ax2.set_ylabel(
    "Unemployment Rate",
    color="skyblue",
    fontsize=14
)

ax1.set_xlim(
    df_unemployment.MONTH.min(),
    df_unemployment.MONTH.max()
)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color="grey",linestyle="--")

ax1.plot(
    df_unemployment.MONTH,
    df_unemployment.UE_BENEFITS_WEB_SEARCH,
    color="blue",
    linewidth=2,
    linestyle="--"
)

ax2.plot(
    df_unemployment.MONTH,
    df_unemployment.UNRATE,
    color="skyblue",
    linewidth=2
)



plt.show()


# ============================ ROLLING AVERAGE ============================ #

"""
Calculate the 6-month rolling average
to smooth the unemployment trend.
"""

rolling_avg_data = (df_unemployment[["UE_BENEFITS_WEB_SEARCH","UNRATE"]].rolling(window=6).mean())

print("\nRolling Average")
print(rolling_avg_data.head(10))


# ============================ ROLLING AVERAGE VISUALIZATION ============================ #

plt.figure(figsize=(14, 8), dpi=120)

plt.title(
    'Rolling Monthly "Unemployment Benefits" Searches vs UNRATE'
)

plt.xticks(rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_xlabel("Months", fontsize=14)

ax1.set_ylabel(
    "Benefit Searches",
    color="blue",
    fontsize=14
)

ax2.set_ylabel(
    "Unemployment Rate",
    color="skyblue",
    fontsize=14
)

ax1.set_xlim(
    df_unemployment.MONTH.min(),
    df_unemployment.MONTH.max()
)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(
    color="grey",
    linestyle="--"
)

ax1.plot(
    df_unemployment.MONTH,
    rolling_avg_data.UE_BENEFITS_WEB_SEARCH,
    color="blue",
    linewidth=2,
    linestyle="--"
)

ax2.plot(
    df_unemployment.MONTH,
    rolling_avg_data.UNRATE,
    color="skyblue",
    linewidth=2
)
plt.show()


# ============================ UPDATED UNEMPLOYMENT DATA ============================ #

updated_ue_df = pd.read_csv("UE Benefits Search vs UE Rate 2004-20.csv")

updated_ue_df.MONTH = pd.to_datetime(updated_ue_df.MONTH)

plt.figure(figsize=(14, 8), dpi=120)

plt.title("Unemployment Benefits Search vs Unemployment Rate (2004-2020)")

plt.xticks(rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_xlabel("Months", fontsize=14)

ax1.set_ylabel(
    "Benefit Searches",
    color="blue",
    fontsize=14
)

ax2.set_ylabel(
    "Unemployment Rate",
    color="skyblue",
    fontsize=14
)

ax1.set_xlim(
    updated_ue_df.MONTH.min(),
    updated_ue_df.MONTH.max()
)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(
    color="grey",
    linestyle="--"
)

ax1.plot(
    updated_ue_df.MONTH,
    updated_ue_df.UE_BENEFITS_WEB_SEARCH,
    color="blue",
    linewidth=2
)

ax2.plot(
    updated_ue_df.MONTH,
    updated_ue_df.UNRATE,
    color="skyblue",
    linewidth=2
)
plt.show()

