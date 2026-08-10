"""
Movie Budget and Revenue Analysis

This project analyzes a movie dataset containing production budgets,
domestic revenue, worldwide revenue, and release dates.

The project covers:
1. Loading the dataset using Pandas.
2. Inspecting the dataset.
3. Cleaning currency columns.
4. Converting dates.
5. Finding missing and duplicate values.
6. Analyzing zero-revenue movies.
7. Calculating the percentage of movies that lost money.
8. Comparing production budgets with worldwide revenue.
9. Analyzing movie trends over time.
10. Comparing movies released before and after 1970.
11. Creating visualizations using Matplotlib and Seaborn.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================ DISPLAY SETTINGS ============================ #

pd.options.display.float_format = "{:,.2f}".format


# ============================ LOAD DATA ============================ #

data = pd.read_csv("cost_revenue_dirty.csv")

print("DATASET INFORMATION")

print("\nDataset Shape:")
print(data.shape)

print("\nFirst 5 Rows:")
print(data.head())

print("\nColumn Names:")
print(data.columns.tolist())

print("\nData Types:")
print(data.dtypes)


# ============================ CHECK MISSING VALUES ============================ #

print("MISSING VALUES")

missing_values = data.isna().sum()

print(missing_values)


# ============================ CHECK DUPLICATE VALUES ============================ #

print("DUPLICATE VALUES")

duplicate_count = data.duplicated().sum()

print(f"Number of duplicate rows: {duplicate_count}")


# ============================ CLEAN CURRENCY COLUMNS ============================ #

"""
The budget and revenue columns contain values stored as strings
with dollar signs and commas.

Example:

$100,000,000

These characters need to be removed before converting
the values into numeric data.
"""

currency_columns = [
    "USD_Production_Budget",
    "USD_Worldwide_Gross",
    "USD_Domestic_Gross"
]

for column in currency_columns:
    data[column] = (
        data[column]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

print("CLEANED CURRENCY DATA")

print(data[currency_columns].head())

print("\nUpdated Data Types:")
print(data.dtypes)


# ============================ CONVERT RELEASE DATE ============================ #

data["Release_Date"] = pd.to_datetime(data["Release_Date"])

print("RELEASE DATE")

print("Release Date Data Type:")
print(data["Release_Date"].dtype)

print("\nFirst 5 Release Dates:")
print(data["Release_Date"].head())


# ============================ BASIC STATISTICS ============================ #


print("BASIC STATISTICS")


average_production_budget = data["USD_Production_Budget"].mean()
average_worldwide_gross = data["USD_Worldwide_Gross"].mean()

print(
    f"\nAverage Production Budget: "
    f"${average_production_budget:,.2f}"
)

print(
    f"Average Worldwide Gross: "
    f"${average_worldwide_gross:,.2f}"
)

print(
    f"Minimum Worldwide Gross: "
    f"${data['USD_Worldwide_Gross'].min():,.2f}"
)

print(
    f"Minimum Domestic Gross: "
    f"${data['USD_Domestic_Gross'].min():,.2f}"
)

print(
    f"25th Percentile of Worldwide Gross: "
    f"${data['USD_Worldwide_Gross'].quantile(0.25):,.2f}"
)


# ============================ ZERO DOMESTIC REVENUE ============================ #

zero_domestic_revenue = data[
    data["USD_Domestic_Gross"] == 0
]


print("MOVIES WITH ZERO DOMESTIC REVENUE")


print(
    f"Number of films with zero domestic revenue: "
    f"{len(zero_domestic_revenue)}"
)

print("\nHighest Budget Movies Among Them:")
print(
    zero_domestic_revenue
    .sort_values(
        by="USD_Production_Budget",
        ascending=False
    )
    .head()
)


# ============================ ZERO WORLDWIDE REVENUE ============================ #

international_zero_revenue = data[
    data["USD_Worldwide_Gross"] == 0
]


print("MOVIES WITH ZERO WORLDWIDE REVENUE")


print(
    f"Number of films with zero worldwide revenue: "
    f"{len(international_zero_revenue)}"
)

print("\nHighest Budget Movies Among Them:")

print(
    international_zero_revenue
    .sort_values(
        by="USD_Production_Budget",
        ascending=False
    )
    .head()
)


# ============================ INTERNATIONAL RELEASES ============================ #

international_release = data[
    (data["USD_Worldwide_Gross"] > 0)
    & (data["USD_Domestic_Gross"] == 0)
]

print("INTERNATIONAL RELEASES")


print(f"Films with worldwide revenue but no domestic revenue:{len(international_release)}"
)

print("\nFirst 5 Results:")
print(international_release.head())


# ============================ USING QUERY ============================ #

international_release_query = data.query("USD_Worldwide_Gross > 0 and USD_Domestic_Gross == 0")

print("\nUsing Pandas query():")
print(international_release_query.head())

print(f"\nNumber of international releases:{len(international_release_query)}"
)


# ============================ FILTER DATA BY DATE ============================ #

"""
The original dataset was scraped around May 1, 2018.

Therefore, movies released after this date are removed
from the analysis.
"""

scrape_date = pd.Timestamp("2018-05-01")

data_clean = data[data["Release_Date"] <= scrape_date]

print("FILTERED DATASET")


print(f"Number of movies after date filtering:{len(data_clean)}")

print("\nFirst 5 Rows:")
print(data_clean.head())


# ============================ MOVIES THAT LOST MONEY ============================ #

"""
A movie is considered to have lost money when
its production budget is greater than its worldwide gross.
"""

money_lost = data[
    data["USD_Production_Budget"]
    > data["USD_Worldwide_Gross"]
]

percentage_lost = len(money_lost) / len(data) * 100

print("MOVIES THAT LOST MONEY")


print(f"Number of movies where production cost exceeded worldwide revenue: {len(money_lost)}")

print(f"Percentage of movies that lost money:{percentage_lost:.2f}%")


# ============================ PRODUCTION BUDGET VS WORLDWIDE GROSS ============================ #

plt.figure(figsize=(8, 6), dpi=120)

ax = sns.scatterplot(
    data=data_clean,
    x="USD_Production_Budget",
    y="USD_Worldwide_Gross"
)

ax.set_title("Production Budget vs Worldwide Gross")
ax.set_xlabel("Production Budget")
ax.set_ylabel("Worldwide Gross")

plt.show()


# ============================ RELEASE DATE VS PRODUCTION BUDGET ============================ #

plt.figure(figsize=(8, 6), dpi=120)

with sns.axes_style("dark"):
    ax = sns.scatterplot(
        data=data_clean,
        x="Release_Date",
        y="USD_Production_Budget",
        hue="USD_Worldwide_Gross",
        size="USD_Worldwide_Gross"
    )

    ax.set(
        title="Release Date vs Production Budget",
        ylabel="Production Budget",
        xlabel="Release Date",
        xlim=(
            data_clean["Release_Date"].min(),
            data_clean["Release_Date"].max()
        )
    )

plt.show()


# ============================ BUDGET VS WORLDWIDE GROSS WITH HUE ============================ #

plt.figure(figsize=(8, 6), dpi=120)

with sns.axes_style("darkgrid"):
    ax = sns.scatterplot(
        data=data_clean,
        x="USD_Production_Budget",
        y="USD_Worldwide_Gross",
        hue="USD_Worldwide_Gross",
        size="USD_Worldwide_Gross"
    )

    ax.set(
        title="Production Budget vs Worldwide Gross",
        ylabel="Worldwide Gross",
        xlabel="Production Budget"
    )

plt.show()


# ============================ CREATE DECADE COLUMN ============================ #

"""
Extract the year from Release_Date and convert it into a decade.

Example:

1965 -> 1960
1987 -> 1980
2015 -> 2010
"""

data_index = pd.DatetimeIndex(data_clean["Release_Date"])

year = data_index.year

decade = year // 10 * 10

data_clean["Decade"] = decade


print("DECADE INFORMATION")

print(data_clean[["Release_Date", "Decade"]].head())


# ============================ SPLIT OLD AND NEW MOVIES ============================ #

old_films = data_clean[
    data_clean["Decade"] <= 1969
]

new_films = data_clean[
    data_clean["Decade"] > 1969
]


print("OLD VS NEW MOVIES")


print(f"Number of movies released before 1970:{old_films.shape[0]}")

print(f"Number of movies released from 1970 onwards:{new_films.shape[0]}")


# ============================ REGRESSION FOR OLD MOVIES ============================ #

plt.figure(figsize=(8, 6), dpi=120)

with sns.axes_style("darkgrid"):

    linear_old = sns.regplot(
        data=old_films,
        x="USD_Production_Budget",
        y="USD_Worldwide_Gross",
        scatter_kws={"color": "black"},
        line_kws={"color": "red"}
    )

    linear_old.set(
        xlim=(
            0,
            old_films["USD_Production_Budget"].max()
        ),
        ylim=(
            0,
            old_films["USD_Worldwide_Gross"].max()
        ),
        xlabel="Budget in $ millions",
        ylabel="Revenue in $ billions",
        title="Films Before 1970"
    )

plt.show()


# ============================ REGRESSION FOR NEW MOVIES ============================ #

plt.figure(figsize=(8, 6), dpi=200)

with sns.axes_style("whitegrid"):

    linear_new = sns.regplot(
        data=new_films,
        x="USD_Production_Budget",
        y="USD_Worldwide_Gross",
        scatter_kws={"color": "blue"},
        line_kws={"color": "red"}
    )

    linear_new.set(
        xlim=(
            0,
            new_films["USD_Production_Budget"].max()
        ),
        ylim=(
            0,
            new_films["USD_Worldwide_Gross"].max()
        ),
        xlabel="Budget in $ millions",
        ylabel="Revenue in $ billions",
        title="Films From 1970"
    )

plt.show()

