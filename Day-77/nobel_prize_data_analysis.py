"""
Nobel Prize Data Analysis

This project explores Nobel Prize data using Pandas, NumPy,
Matplotlib, Seaborn, and Plotly.

The analysis includes:
- Dataset inspection and cleaning
- Gender distribution
- Repeated Nobel Prize winners
- Prize distribution by category
- Male vs Female prize distribution
- Nobel Prizes awarded over time
- Prize-share analysis
- Top countries by number of Nobel Prizes
- Geographic distribution of Nobel Prizes
- Country-wise prize distribution by category
"""

import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from fractions import Fraction


# ============================ DISPLAY SETTINGS ============================ #

pd.options.display.float_format = "{:,.2f}".format


# ============================ LOAD DATA ============================ #

df_data = pd.read_csv("nobel_prize_data.csv")


print("NOBEL PRIZE DATASET")
print()

print("\nDataset Shape:")
print(df_data.shape)

print("\nDataset Columns:")
print(df_data.columns.tolist())

print("\nFirst 5 Rows:")
print(df_data.head())


# ============================ FIRST AND MOST RECENT YEAR ============================ #


print("FIRST AND MOST RECENT NOBEL PRIZE YEARS")
print()

first_year = df_data.sort_values(by="year").head(1)
recent_year = df_data.sort_values(
    by="year",
    ascending=False
).head(1)

print("\nFirst Nobel Prize Record:")
print(first_year)

print("\nMost Recent Nobel Prize Record:")
print(recent_year)


# ============================ CHECK DUPLICATES ============================ #


print("DUPLICATE RECORDS")
print()

duplicate_count = df_data.duplicated().sum()

print(f"Number of duplicate rows: {duplicate_count}")


# ============================ CHECK MISSING VALUES ============================ #


print("MISSING VALUES")
print()

print(df_data.isna().sum())


# ============================ MISSING BIRTH DATE ============================ #

columns_to_check = [
    "year",
    "category",
    "laureate_type",
    "full_name",
    "birth_date",
    "organization_name"
]

missing_birth_date = df_data.loc[
    df_data["birth_date"].isna(),
    columns_to_check
]

print("\nRecords with missing birth dates:")
print(missing_birth_date)


# ============================ MISSING ORGANIZATION NAME ============================ #

missing_organization = df_data.loc[
    df_data["organization_name"].isna(),
    columns_to_check
]

print("\nRecords with missing organization names:")
print(missing_organization)


# ============================ DATA TYPE CONVERSION ============================ #

"""
Convert the birth_date column from strings into
Pandas datetime objects.
"""

df_data["birth_date"] = pd.to_datetime(
    df_data["birth_date"]
)


print("UPDATED DATA TYPES")
print()

print(df_data.dtypes)


# ============================ CALCULATE PRIZE SHARE ============================ #

"""
The prize_share column contains fractions such as:

1/1
1/2
1/3
1/4

Fraction() converts these strings into mathematical
fractions, which are then converted into percentages.
"""

df_data["share_pct"] = df_data["prize_share"].apply(
    lambda x: float(Fraction(x)) * 100
)

print("\nPrize share converted to percentage:")

print(
    df_data[
        ["prize_share", "share_pct"]
    ].head()
)


# ============================ GENDER DISTRIBUTION ============================ #

gender = df_data.value_counts("sex")


print("NOBEL PRIZE DISTRIBUTION BY GENDER")
print()

print(gender)


# ============================ GENDER DONUT CHART ============================ #

pie_chart = px.pie(
    names=gender.index,
    values=gender.values,
    title="Nobel Prize Distribution by Gender",
    hole=0.4
)

pie_chart.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

pie_chart.show()


# ============================ FIRST FEMALE NOBEL LAUREATES ============================ #

female_laureates = (
    df_data
    .query('sex == "Female"')
    .sort_values(by="year")
    .head(3)
)


print("EARLIEST FEMALE NOBEL LAUREATES")
print()

print(female_laureates)


# ============================ REPEATED WINNERS ============================ #

repeated_winners = df_data.value_counts("full_name")

repeated_winners = repeated_winners[
    repeated_winners > 1
]


print("REPEATED NOBEL PRIZE WINNERS")
print()

print(repeated_winners)


# ============================ PRIZES BY CATEGORY ============================ #

categories = df_data["category"].value_counts()


print("PRIZES BY CATEGORY")
print()

print(categories)


# ============================ CATEGORY BAR CHART ============================ #

fig = px.bar(
    x=categories.index,
    y=categories.values,
    title="Number of Prizes Awarded by Category",
    color_discrete_sequence=px.colors.sequential.Aggrnyl
)

fig.update_layout(
    showlegend=False,
    yaxis_title="Number of Prizes Awarded",
    xaxis_title="Category"
)

fig.show()


# ============================ FIRST ECONOMICS PRIZE ============================ #

first_economics_prize = (
    df_data
    .query('category == "Economics"')
    .sort_values(by="year")
    .head(1)
)


print("FIRST ECONOMICS NOBEL PRIZE")
print()

print(first_economics_prize)


# ============================ CATEGORY BY GENDER ============================ #

split_check = (
    df_data
    .groupby(
        ["category", "sex"],
        as_index=False
    )
    .agg({"prize": "count"})
)

split_check.sort_values(
    by="prize",
    ascending=False,
    inplace=True
)

print("PRIZES BY CATEGORY AND GENDER")
print()

print(split_check.head())


# ============================ STACKED CATEGORY CHART ============================ #

bar_split = px.bar(
    split_check,
    x="category",
    y="prize",
    color="sex",
    title="Number of Prizes by Category Split by Male and Female",
    barmode="stack"
)

bar_split.update_layout(
    showlegend=False,
    yaxis_title="Number of Prizes Awarded",
    xaxis_title="Category",
    xaxis={
        "categoryorder": "total descending"
    }
)

bar_split.show()


# ============================ PRIZES PER YEAR ============================ #

prize_per_year = (
    df_data
    .groupby(by="year")
    .count()["prize"]
)

print()
print("NOBEL PRIZES PER YEAR")
print()

print(prize_per_year.head())

print("\nLast 5 Years:")
print(prize_per_year.tail())


# ============================ FIVE-YEAR MOVING AVERAGE ============================ #

moving_average = prize_per_year.rolling(
    window=5
).mean()

print("\nFive-year moving average:")
print(moving_average.head(10))


# ============================ PRIZES PER YEAR CHART ============================ #

plt.figure(
    figsize=(16, 8),
    dpi=200
)

plt.title(
    "Number of Nobel Prizes Awarded per Year",
    fontsize=18
)

plt.yticks(fontsize=14)

plt.xticks(
    ticks=np.arange(1900, 2021, step=5),
    fontsize=14,
    rotation=45
)

ax = plt.gca()

ax.set_xlim(
    1900,
    2020
)

ax.scatter(
    x=prize_per_year.index,
    y=prize_per_year.values,
    c="dodgerblue",
    alpha=0.7,
    s=100
)

ax.plot(
    prize_per_year.index,
    moving_average.values,
    c="crimson",
    linewidth=3
)

plt.show()


# ============================ YEARLY AVERAGE PRIZE SHARE ============================ #

yearly_avg_share = (
    df_data
    .groupby(by="year")
    .agg({
        "share_pct": pd.Series.mean
    })
)

share_moving_average = (
    yearly_avg_share
    .rolling(window=5)
    .mean()
)

print()
print("AVERAGE PRIZE SHARE PER YEAR")
print()
print(yearly_avg_share.head())


# ============================ PRIZE SHARE AND PRIZE COUNT ============================ #

plt.figure(
    figsize=(16, 8),
    dpi=200
)

plt.title(
    "Nobel Prizes and Average Prize Share per Year",
    fontsize=18
)

plt.yticks(fontsize=14)

plt.xticks(
    ticks=np.arange(1900, 2021, step=5),
    fontsize=14,
    rotation=45
)

ax1 = plt.gca()

ax2 = ax1.twinx()

ax1.set_xlim(
    1900,
    2020
)

# Plot number of prizes.

ax1.scatter(
    x=prize_per_year.index,
    y=prize_per_year.values,
    c="dodgerblue",
    alpha=0.7,
    s=100
)

ax1.plot(
    prize_per_year.index,
    moving_average.values,
    c="crimson",
    linewidth=3
)

# Plot average prize share.

ax2.plot(
    prize_per_year.index,
    share_moving_average["share_pct"].values,
    c="grey",
    linewidth=3
)

plt.show()


# ============================ TOP 20 COUNTRIES ============================ #

top20_countries = (
    df_data
    .value_counts("birth_country_current")
    .head(20)
)

top20_countries = pd.DataFrame(
    top20_countries
)

top20_countries.reset_index(
    inplace=True
)

top20_countries.columns = [
    "birth_country_current",
    "prize"
]

print()
print("TOP 20 COUNTRIES BY NOBEL PRIZES")
print()

print(top20_countries)


# ============================ TOP 20 COUNTRIES BAR CHART ============================ #

plotly_chart = px.bar(
    top20_countries,
    x="prize",
    y="birth_country_current",
    title="Number of Nobel Prizes Won by Country",
    orientation="h",
    color="prize"
)

plotly_chart.update_layout(
    showlegend=False,
    xaxis_title="Number of Prizes Won",
    yaxis_title="Country",
    yaxis={
        "categoryorder": "total ascending"
    }
)

plotly_chart.show()


# ============================ COUNTRY AND ISO DATA ============================ #

df_countries = (
    df_data
    .groupby(
        ["birth_country_current", "ISO"],
        as_index=False
    )
    .agg({
        "prize": pd.Series.count
    })
)

df_countries.sort_values(
    "prize",
    ascending=False,
    inplace=True
)

print("\n" + "=" * 70)
print("COUNTRY-WISE NOBEL PRIZE DATA")
print("=" * 70)

print(df_countries.head(20))


# ============================ WORLD MAP ============================ #

world_map = px.choropleth(
    df_countries,
    locations="ISO",
    color="prize",
    hover_name="birth_country_current",
    color_continuous_scale=px.colors.sequential.matter
)

world_map.update_layout(
    coloraxis_showscale=True
)

world_map.show()


# ============================ COUNTRY AND CATEGORY ============================ #

cat_country = (
    df_data
    .groupby(
        ["birth_country_current", "category"],
        as_index=False
    )
    .agg({
        "prize": pd.Series.count
    })
)

cat_country.sort_values(
    by="prize",
    ascending=False,
    inplace=True
)

print("\n" + "=" * 70)
print("COUNTRY-WISE PRIZES BY CATEGORY")
print("=" * 70)

print(cat_country.head(20))


# ============================ MERGE COUNTRY DATA ============================ #

merged_df = pd.merge(
    cat_country,
    top20_countries,
    on="birth_country_current"
)

merged_df.columns = [
    "birth_country_current",
    "category",
    "cat_prize",
    "total_prize"
]

merged_df.sort_values(
    by="total_prize",
    inplace=True
)

print("\nMerged country and category data:")
print(merged_df.head(20))


# ============================ TOP COUNTRIES BY CATEGORY CHART ============================ #

cat_cntry_bar = px.bar(
    x=merged_df.cat_prize,
    y=merged_df.birth_country_current,
    color=merged_df.category,
    orientation="h",
    title="Top 20 Countries by Number of Prizes and Category"
)

cat_cntry_bar.update_layout(
    xaxis_title="Number of Prizes",
    yaxis_title="Country",
    yaxis={
        "categoryorder": "total ascending"
    }
)

cat_cntry_bar.show()
