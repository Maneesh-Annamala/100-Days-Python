"""
Programming Language Popularity Analysis using Pandas and Matplotlib

This project demonstrates how to:
1. Read a CSV file.
2. Rename columns.
3. Explore the dataset.
4. Group and summarize data.
5. Convert date columns.
6. Reshape data using Pivot Table.
7. Handle missing values.
8. Apply Rolling Average.
9. Visualize trends using Matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt

# ============================ LOAD DATASET ============================ #

# Read the CSV file into a Pandas DataFrame.
df = pd.read_csv("QueryResults.csv")

print()
print("FIRST 5 ROWS OF THE DATASET")
print()
print(df.head())

print()
print("DATASET SHAPE")
print()
print(df.shape)

print()
print("COLUMN NAMES")
print()
print(df.columns)


# ============================ RENAME COLUMNS ============================ #

"""
Rename the columns to more meaningful names.
"""

df.rename(
    columns={
        "m": "DATE",
        "TagName": "TAG",
        "Unnamed: 2": "COUNT"
    },
    inplace=True
)

print()
print("COLUMN NAMES AFTER RENAMING")
print()
print(df.columns)


# ============================ DATASET INFORMATION ============================ #

print()
print("NUMBER OF NON-NULL VALUES")
print()
print(df.count())


# ============================ GROUPBY ANALYSIS ============================ #

"""
Find the total number of posts
for every programming language.
"""

print()
print("TOTAL COUNT FOR EACH PROGRAMMING LANGUAGE")
print()
print(df.groupby("TAG").sum(numeric_only=True))

print()
print("NUMBER OF RECORDS FOR EACH PROGRAMMING LANGUAGE")
print()
print(df.groupby("TAG").count())


# ============================ DATE CONVERSION ============================ #

"""
Convert the DATE column into
datetime format.
"""

df["DATE"] = pd.to_datetime(df["DATE"])

print()
print("DATASET AFTER DATE CONVERSION")
print()
print(df.head())


# ============================ PIVOT TABLE ============================ #

"""
Convert the dataset into a pivot table.

Rows    -> DATE
Columns -> Programming Language
Values  -> COUNT
"""

reshaped_df = df.pivot(
    index="DATE",
    columns="TAG",
    values="COUNT"
)

print()
print("PIVOT TABLE (FIRST 5 ROWS)")
print()
print(reshaped_df.head())

print()
print("PIVOT TABLE (LAST 5 ROWS)")
print()
print(reshaped_df.tail())


# ============================ HANDLE MISSING VALUES ============================ #

"""
Replace all missing values with zero.
"""

reshaped_df.fillna(0, inplace=True)

print()
print("CHECKING FOR MISSING VALUES")
print()
print(reshaped_df.isna().any())


# ============================ ROLLING AVERAGE ============================ #

"""
Calculate the 12-month rolling average.

Rolling average smooths the graph
and removes sudden spikes.
"""

roll_df = reshaped_df.rolling(window=12).mean()

print()
print("FIRST 10 ROWS OF ROLLING AVERAGE")
print()
print(roll_df.head(10))


# ============================ DATA VISUALIZATION ============================ #

"""
Plot the popularity trend of each
programming language over time.
"""

plt.figure(figsize=(16, 10))

plt.xticks(fontsize=8)
plt.yticks(fontsize=14)

plt.xlabel("DATE", fontsize=14)
plt.ylabel("COUNT", fontsize=14)

plt.title(
    "Programming Language Popularity Over Time",
    fontsize=18
)

plt.ylim(0, 35000)

for column in roll_df.columns:
    plt.plot(
        roll_df.index,
        roll_df[column],
        linewidth=3,
        label=column
    )

plt.legend(fontsize=12)
print()
print("DISPLAYING THE GRAPH...")
print()

plt.show()
