"""
LEGO Dataset Analysis using Pandas and Matplotlib

This project demonstrates how to:
1. Read multiple CSV datasets.
2. Explore and summarize LEGO data.
3. Analyze colors and transparency.
4. Analyze LEGO sets over time.
5. Study the growth of LEGO themes.
6. Calculate average parts per set.
7. Merge datasets.
8. Visualize data using line, scatter, and bar charts.
"""

import pandas as pd
import matplotlib.pyplot as plt

# ============================ LOAD COLORS DATASET ============================ #

# Read the colors dataset.
colors = pd.read_csv("colors.csv")

print()
print("FIRST 5 ROWS OF COLORS DATASET")
print()
print(colors.head())


# ============================ COLOR ANALYSIS ============================ #

print()
print("NUMBER OF UNIQUE COLORS")
print()
print(colors["name"].nunique())

print()
print("COUNT OF TRANSPARENT AND NON-TRANSPARENT COLORS")
print()
print(colors.groupby("is_trans").count())

print()
print("TRANSPARENCY VALUE COUNTS")
print()
print(colors["is_trans"].value_counts())


# ============================ LOAD SETS DATASET ============================ #

sets = pd.read_csv("sets.csv")

print()
print("FIRST 5 ROWS OF SETS DATASET")
print()
print(sets.head())

print()
print("LAST 5 ROWS OF SETS DATASET")
print()
print(sets.tail())


# ============================ SORT DATA BY YEAR ============================ #

sorted_year = sets.sort_values("year")

print()
print("SETS SORTED BY YEAR")
print()
print(sorted_year.head())


# ============================ FIRST YEAR ANALYSIS ============================ #

print()
print("NUMBER OF SETS RELEASED IN 1949")
print()
print(sets[sets["year"] == 1949].count())


# ============================ BIGGEST LEGO SETS ============================ #

largest_sets = sets.sort_values(
    "num_parts",
    ascending=False
)

print()
print("TOP 5 LARGEST LEGO SETS")
print()
print(largest_sets.head())


# ============================ SETS PER YEAR ============================ #

"""
Group the data by year and
count the number of sets released.
"""

sets_by_year = sets.groupby("year").count()

print()
print("NUMBER OF SETS RELEASED EACH YEAR")
print()
print(sets_by_year["set_num"])


# ============================ LINE GRAPH ============================ #

"""
Visualize the number of LEGO sets
released every year.
"""

plt.figure(figsize=(12, 6))

plt.plot(
    sets_by_year.index[:-2],
    sets_by_year["set_num"][:-2]
)

plt.title("Number of LEGO Sets Released Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Sets")

print("\nDisplaying graph: LEGO Sets Per Year")

plt.show()


# ============================ THEMES PER YEAR ============================ #

"""
Find the number of unique LEGO themes
introduced each year.
"""

theme_by_year = sets.groupby("year").agg(
    {"theme_id": pd.Series.nunique}
)

print()
print("FIRST 5 YEARS OF UNIQUE THEMES")
print()
print(theme_by_year.head())

print()
print("LAST 5 YEARS OF UNIQUE THEMES")
print()
print(theme_by_year.tail())


# ============================ DUAL AXIS GRAPH ============================ #

"""
Compare:

1. Number of LEGO sets
2. Number of LEGO themes

using two Y-axes.
"""

fig, ax1 = plt.subplots(figsize=(14, 8))

ax2 = ax1.twinx()

ax1.set_xlabel("Year", fontsize=14)
ax1.set_ylabel("Number of Sets", fontsize=14)
ax2.set_ylabel("Number of Themes", fontsize=14)

ax1.plot(
    sets_by_year.index[:-2],
    sets_by_year["set_num"][:-2],
    color="green",
    linewidth=2,
    label="Sets"
)

ax2.plot(
    theme_by_year.index[:-2],
    theme_by_year["theme_id"][:-2],
    color="blue",
    linewidth=2,
    label="Themes"
)

plt.title("LEGO Sets vs LEGO Themes Over Time")

print("\nDisplaying graph: Sets vs Themes")

plt.show()


# ============================ AVERAGE PARTS PER SET ============================ #

"""
Calculate the average number of
pieces per LEGO set each year.
"""

parts_per_set = sets.groupby("year").agg(
    {"num_parts": pd.Series.mean}
)

print()
print("AVERAGE PARTS PER SET")
print()
print(parts_per_set.head())


# ============================ SCATTER PLOT ============================ #

plt.figure(figsize=(12, 6))

plt.scatter(
    parts_per_set.index[:-2],
    parts_per_set["num_parts"][:-2]
)

plt.title("Average Number of Parts Per LEGO Set")
plt.xlabel("Year")
plt.ylabel("Average Parts")

print("\nDisplaying scatter plot...")

plt.show()


# ============================ MOST POPULAR THEMES ============================ #

"""
Count how many sets belong
to each LEGO theme.
"""

theme_by_id = sets["theme_id"].value_counts()

print()
print("TOP 10 MOST POPULAR THEMES")
print()
print(theme_by_id.head(10))


# ============================ LOAD THEMES DATASET ============================ #

themes = pd.read_csv("themes.csv")

print()
print("FIRST 5 ROWS OF THEMES DATASET")
print()
print(themes.head())


# ============================ STAR WARS THEME ============================ #

print()
print("STAR WARS THEME INFORMATION")
print()
print(themes[themes["name"] == "Star Wars"])

print()
print("SETS BELONGING TO STAR WARS")
print()
print(sets[sets["theme_id"] == 17])


# ============================ MERGE DATASETS ============================ #

"""
Merge the theme counts
with the themes dataset.
"""

set_theme = pd.DataFrame({
    "id": theme_by_id.index,
    "set_count": theme_by_id.values
})

print()
print("THEME COUNT DATAFRAME")
print()
print(set_theme.head())

merged_df = pd.merge(
    set_theme,
    themes,
    on="id"
)

print()
print("MERGED DATAFRAME")
print()
print(merged_df.head())


# ============================ BAR CHART ============================ #

"""
Display the top 10 LEGO themes
based on the number of sets.
"""

plt.figure(figsize=(10, 8))

plt.xticks(
    fontsize=14,
    rotation=45
)

plt.yticks(fontsize=14)

plt.xlabel(
    "Theme Name",
    fontsize=16
)

plt.ylabel(
    "Number of Sets",
    fontsize=16
)

plt.title("Top 10 LEGO Themes")

plt.bar(
    merged_df["name"].head(10),
    merged_df["set_count"].head(10)
)
print("\nDisplaying bar chart...")
plt.show()