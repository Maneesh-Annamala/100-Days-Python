"""
Google Play Store Apps Data Analysis using Pandas and Plotly

This project demonstrates how to:

1. Load and explore a Google Play Store apps dataset.
2. Remove unnecessary columns and missing values.
3. Remove duplicate app records.
4. Analyze app ratings, reviews, sizes, and installs.
5. Clean numeric columns such as Installs and Price.
6. Estimate potential revenue for paid apps.
7. Analyze app categories and genres.
8. Compare free and paid applications.
9. Analyze app installs and pricing using Plotly visualizations.
10. Create interactive charts using Plotly Express.
"""

import pandas as pd
import plotly.express as px


# ============================ DISPLAY SETTINGS ============================ #

# Format floating-point numbers with commas and two decimal places.
pd.options.display.float_format = "{:,.2f}".format


# ============================ LOAD DATASET ============================ #

print()
print("LOADING GOOGLE PLAY STORE DATASET")
print()

df_apps = pd.read_csv("apps.csv")

print("Dataset loaded successfully!")


# ============================ INITIAL DATA EXPLORATION ============================ #

print()
print("DATASET SHAPE")
print()
print(df_apps.shape)

print()
print("DATASET COLUMNS")
print()
print(df_apps.columns)

print()
print("RANDOM 5 ROWS")
print()
print(df_apps.sample(5))


# ============================ REMOVE UNNECESSARY COLUMNS ============================ #

"""
Remove columns that are not required for this analysis.
"""

new_df_apps = df_apps.drop(
    ["Last_Updated", "Android_Ver"],
    axis=1
)

print()
print("COLUMNS AFTER REMOVING UNNECESSARY DATA")
print()
print(new_df_apps.columns)


# ============================ CHECK MISSING VALUES ============================ #

print()
print("MISSING VALUES BEFORE CLEANING")
print()
print(new_df_apps.isna().sum())


# ============================ REMOVE MISSING VALUES ============================ #

"""
Remove rows containing missing values.
"""

cleaned_df_apps = new_df_apps.dropna()

print()
print("MISSING VALUES AFTER CLEANING")
print()
print(cleaned_df_apps.isna().sum())

print("\nDataset shape after removing missing values:")
print(cleaned_df_apps.shape)


# ============================ CHECK DUPLICATE DATA ============================ #
print()
print("NUMBER OF DUPLICATE ROWS")
print()
print(cleaned_df_apps.duplicated().sum())

print()
print("INSTAGRAM RECORDS")
print()
print(
    cleaned_df_apps[
        cleaned_df_apps["App"] == "Instagram"
    ]
)


# ============================ REMOVE DUPLICATE APPS ============================ #

"""
Remove duplicate applications based on:
- App name
- App type
- Price

This allows the same app to appear if it has
a different type or price.
"""

cleaned_df_apps = cleaned_df_apps.drop_duplicates(
    subset=["App", "Type", "Price"]
)

print()
print("DUPLICATES AFTER CLEANING")
print()
print(cleaned_df_apps.duplicated().sum())

print("\nDataset shape after removing duplicates:")
print(cleaned_df_apps.shape)


# ============================ HIGHEST RATED APPS ============================ #

print()
print("TOP 10 HIGHEST RATED APPS")
print()

print(
    cleaned_df_apps
    .sort_values("Rating", ascending=False)
    .head(10)
)


# ============================ LARGEST APPS ============================ #

print()
print("TOP 5 LARGEST APPS")
print()

print(
    cleaned_df_apps
    .sort_values("Size_MBs", ascending=False)
    .head(5)
)


# ============================ MOST REVIEWED APPS ============================ #

"""
Find the 50 applications with the highest
number of reviews.
"""

reviews_df = (
    cleaned_df_apps
    .sort_values("Reviews", ascending=False)
    .head(50)
)

print()
print("TOP 50 MOST REVIEWED APPS")
print()
print(reviews_df.head())


# ============================ PAID APPS AMONG TOP REVIEWED ============================ #

check_df = reviews_df[
    reviews_df["Type"] == "Paid"
]

print()
print("PAID APPS AMONG TOP 50 MOST REVIEWED")
print()
print(check_df.shape)
print(check_df)


# ============================ CONTENT RATING ANALYSIS ============================ #

"""
Count the number of apps belonging to
each content rating category.
"""

ratings_df = cleaned_df_apps[
    "Content_Rating"
].value_counts()

print()
print("CONTENT RATING COUNTS")
print()
print(ratings_df)


# ============================ CONTENT RATING PIE CHART ============================ #

fig = px.pie(
    names=ratings_df.index,
    values=ratings_df.values,
    title="Content Rating"
)

fig.update_traces(
    textposition="outside",
    textinfo="percent+label"
)
fig.show()


# ============================ CLEAN INSTALLS COLUMN ============================ #

"""
The Installs column contains commas and is initially
stored as a string.

Remove commas and convert the column to numeric data.
"""

print(type(cleaned_df_apps["Installs"].iloc[0]))

cleaned_df_apps["Installs"] = (
    cleaned_df_apps["Installs"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

cleaned_df_apps["Installs"] = pd.to_numeric(
    cleaned_df_apps["Installs"]
)

# ============================ INSTALLS GROUPBY ============================ #

print()
print("NUMBER OF APPS BY INSTALL COUNT")
print()

print(
    cleaned_df_apps[
        ["Installs", "App"]
    ].groupby("Installs").count()
)


# ============================ CLEAN PRICE COLUMN ============================ #

"""
The Price column contains the "$" symbol.

Remove the symbol and convert the column
to numeric data.
"""

cleaned_df_apps["Price"] = (
    cleaned_df_apps["Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
)

cleaned_df_apps["Price"] = pd.to_numeric(
    cleaned_df_apps["Price"]
)

print()
print("PRICE DATA TYPE")
print()
print(cleaned_df_apps["Price"].dtype)


# ============================ REMOVE UNREALISTIC PRICES ============================ #

"""
Remove apps costing more than $250.

These extremely expensive apps can distort
the price analysis.
"""

cleaned_df_apps.drop(
    cleaned_df_apps[
        cleaned_df_apps["Price"] > 250
    ].index,
    inplace=True
)

print()
print("MOST EXPENSIVE APPS AFTER CLEANING")
print()

print(
    cleaned_df_apps
    .sort_values("Price", ascending=False)
    .head(20)
)

print("\nDataset shape:")
print(cleaned_df_apps.shape)


# ============================ ESTIMATE REVENUE ============================ #

"""
Estimate potential revenue using:

Revenue Estimate = Price × Installs

This is only a rough estimate because actual
revenue may be affected by many other factors.
"""

Revenue_Estimate = (
    cleaned_df_apps["Price"]
    * cleaned_df_apps["Installs"]
)

cleaned_df_apps["Revenue_Estimate"] = Revenue_Estimate

print()
print("DATASET COLUMNS AFTER ADDING REVENUE ESTIMATE")
print()
print(cleaned_df_apps.columns)

print()
print("TOP 10 APPS BY ESTIMATED REVENUE")
print()

print(
    cleaned_df_apps
    .sort_values(
        "Revenue_Estimate",
        ascending=False
    )
    .head(10)
)


# ============================ TOP APP CATEGORIES ============================ #

"""
Find the 10 categories containing
the largest number of applications.
"""

top_app_categories = (
    cleaned_df_apps["Category"]
    .value_counts()
    .head(10)
)

print()
print("TOP 10 APP CATEGORIES BY NUMBER OF APPS")
print()
print(top_app_categories)

fig = px.bar(
    x=top_app_categories.index,
    y=top_app_categories.values,
    title="Category Popularity by Apps Available"
)
fig.show()


# ============================ CATEGORIES BY DOWNLOADS ============================ #

"""
Calculate the total number of installs
for every app category.
"""

top_category_by_downloads = (
    cleaned_df_apps
    .groupby("Category")
    .agg({"Installs": "sum"})
    .sort_values(
        "Installs",
        ascending=False
    )
    .head(10)
)

print()
print("TOP 10 CATEGORIES BY TOTAL DOWNLOADS")
print()
print(top_category_by_downloads)


# ============================ CATEGORY DOWNLOAD BAR CHART ============================ #

fig = px.bar(
    x=top_category_by_downloads.index,
    y=top_category_by_downloads["Installs"],
    title="Category Popularity by Downloads"
)
fig.show()


# ============================ HORIZONTAL CATEGORY CHART ============================ #

fig = px.bar(
    y=top_category_by_downloads.index,
    x=top_category_by_downloads["Installs"],
    orientation="h",
    title="Category Popularity"
)
fig.show()


# ============================ APPS VS INSTALLS ============================ #

"""
Compare the number of applications in each category
with the total number of installs.

A category with fewer apps but many installs
can indicate a highly concentrated category.
"""

highest_installs_and_apps_count = (
    cleaned_df_apps
    .groupby("Category")
    .agg({
        "Installs": "sum",
        "App": "count"
    })
)

print()
print("NUMBER OF APPS AND INSTALLS BY CATEGORY")
print()
print(highest_installs_and_apps_count)


# ============================ CATEGORY SCATTER PLOT ============================ #

scatter = px.scatter(
    highest_installs_and_apps_count,
    x="App",
    y="Installs",
    size="App",
    hover_name=highest_installs_and_apps_count.index,
    color="Installs"
)

scatter.update_layout(
    xaxis_title="Number of Apps (Lower = More Concentrated)",
    yaxis_title="Installs",
    yaxis=dict(type="log")
)
scatter.show()


# ============================ GENRE ANALYSIS ============================ #

"""
Some apps belong to multiple genres separated by ";".

Split those genres and count each genre individually.
"""

stack = (
    cleaned_df_apps["Genres"]
    .str.split(";", expand=True)
    .stack()
)

new_genre_df = stack.value_counts().head(20)

print()
print("TOP 20 APP GENRES")
print()
print(new_genre_df)


# ============================ GENRE BAR CHART ============================ #

bar = px.bar(
    new_genre_df,
    x=new_genre_df.index,
    y=new_genre_df.values,
    title="Top Genres",
    hover_name=new_genre_df.index,
    color=new_genre_df.values,
    color_continuous_scale="Agsunset"
)

bar.update_layout(
    xaxis_title="Genre",
    yaxis_title="Number of Apps",
    coloraxis_showscale=False
)
bar.show()


# ============================ FREE VS PAID APPS ============================ #

"""
Count free and paid apps for every category.
"""

df_free_vs_paid = (
    cleaned_df_apps
    .groupby(
        ["Category", "Type"],
        as_index=False
    )
    .agg({"App": "count"})
)
print()
print("FREE VS PAID APPS BY CATEGORY")
print()
print(df_free_vs_paid)


# ============================ FREE VS PAID BAR CHART ============================ #

g_bar = px.bar(
    df_free_vs_paid,
    x="Category",
    y="App",
    title="Free vs Paid Apps by Category",
    color="Type",
    barmode="group"
)

g_bar.update_layout(
    xaxis_title="Category",
    yaxis_title="Number of Apps",
    xaxis={
        "categoryorder": "total descending"
    },
    yaxis=dict(type="log")
)
g_bar.show()


# ============================ PAID VS FREE INSTALLS ============================ #

"""
Compare the distribution of installs
between free and paid applications.
"""

box = px.box(
    cleaned_df_apps,
    x="Type",
    y="Installs",
    title="Paid vs Free Apps Installs",
    color="Type",
    notched=True,
    points="all"
)

box.update_layout(
    xaxis_title="App Type",
    yaxis_title="Installs",
    yaxis=dict(type="log")
)
box.show()


# ============================ PAID APP REVENUE ============================ #

"""
Filter only paid apps and analyze
their estimated revenue by category.
"""

df_paid_apps = cleaned_df_apps[
    cleaned_df_apps["Type"] == "Paid"
]

box = px.box(
    df_paid_apps,
    x="Category",
    y="Revenue_Estimate",
    title="How Much Can Paid Apps Earn?"
)

box.update_layout(
    xaxis_title="Category",
    yaxis_title="Paid App Ballpark Revenue",
    xaxis={
        "categoryorder": "min ascending"
    },
    yaxis=dict(type="log")
)
box.show()


# ============================ PAID APP PRICING ============================ #

"""
Analyze how much paid apps charge
across different categories.
"""

df_paid_apps_for_price = cleaned_df_apps[
    cleaned_df_apps["Type"] == "Paid"
]

box = px.box(
    df_paid_apps_for_price,
    x="Category",
    y="Price",
    title="How Much Are Paid Apps Charging?"
)

box.update_layout(
    xaxis_title="Category",
    yaxis_title="Paid App Price",
    xaxis={
        "categoryorder": "max descending"
    },
    yaxis=dict(type="log")
)

print("\nDisplaying Paid App Price Box Plot...")

box.show()

