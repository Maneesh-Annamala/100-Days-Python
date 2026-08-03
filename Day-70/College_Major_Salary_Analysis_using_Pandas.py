"""
College Major Salary Analysis using Pandas

This project demonstrates how to:
1. Read a CSV file using Pandas.
2. Explore the dataset.
3. Clean missing values.
4. Find majors with the highest and lowest salaries.
5. Calculate salary spread.
6. Sort the data.
7. Perform group-by analysis.
"""

import pandas as pd

# ============================ LOAD DATASET ============================ #

# Read the CSV file into a DataFrame.
df = pd.read_csv("salaries_by_college_major.csv")

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

print()
print("CHECKING FOR MISSING VALUES")
print()
print(df.isna())

print()
print("LAST 5 ROWS OF THE DATASET")
print()
print(df.tail())


# ============================ DATA CLEANING ============================ #

# Remove all rows containing missing values.
clean_df = df.dropna()

print()
print("DATASET AFTER REMOVING NULL VALUES")
print()
print(clean_df.tail())


# ============================ HIGHEST STARTING SALARY ============================ #

highest_starting_salary_index = clean_df["Starting Median Salary"].idxmax()

print()
print("MAJOR WITH THE HIGHEST STARTING MEDIAN SALARY")
print()
print(clean_df.loc[highest_starting_salary_index])

print("\nMajor:")
print(clean_df.loc[highest_starting_salary_index, "Undergraduate Major"])


# ============================ HIGHEST MID-CAREER SALARY ============================ #

highest_mid_salary_index = clean_df["Mid-Career Median Salary"].idxmax()

print()
print("MAJOR WITH THE HIGHEST MID-CAREER MEDIAN SALARY")
print()
print(clean_df.loc[highest_mid_salary_index])


# ============================ LOWEST STARTING SALARY ============================ #

lowest_starting_salary_index = clean_df["Starting Median Salary"].idxmin()

print()
print("MAJOR WITH THE LOWEST STARTING SALARY")
print()
print(clean_df.loc[lowest_starting_salary_index])


# ============================ LOWEST MID-CAREER SALARY ============================ #

lowest_mid_salary_index = clean_df["Mid-Career Median Salary"].idxmin()

print()
print("MAJOR WITH THE LOWEST MID-CAREER MEDIAN SALARY")
print()
print(clean_df.loc[lowest_mid_salary_index, "Undergraduate Major"])


# ============================ CALCULATE SALARY SPREAD ============================ #

"""
Salary Spread = Highest salary - Lowest salary.

This shows how much salary varies
within the same career.
"""

salary_spread = (
    clean_df["Mid-Career 90th Percentile Salary"]
    -
    clean_df["Mid-Career 10th Percentile Salary"]
)

clean_df.insert(1, "Spread", salary_spread)

print()
print("DATASET AFTER ADDING SPREAD COLUMN")
print()
print(clean_df.head())


# ============================ SORT BY LOWEST SPREAD ============================ #

sorted_spread = clean_df.sort_values("Spread")

print()
print("TOP 5 MAJORS WITH LOWEST SALARY SPREAD")
print()
print(sorted_spread[["Undergraduate Major", "Spread"]].head())


# ============================ SORT BY HIGHEST SPREAD ============================ #

sorted_spread_desc = clean_df.sort_values(
    "Spread",
    ascending=False
)

print()
print("TOP 5 MAJORS WITH HIGHEST SALARY SPREAD")
print()
print(sorted_spread_desc[["Undergraduate Major", "Spread"]].head())


# ============================ HIGHEST 90TH PERCENTILE SALARY ============================ #

highest_salary = clean_df.sort_values(
    "Mid-Career 90th Percentile Salary",
    ascending=False
)

print()
print("TOP 5 MAJORS WITH HIGHEST 90TH PERCENTILE SALARY")
print()
print(highest_salary.head())


# ============================ HIGHEST MID-CAREER MEDIAN SALARY ============================ #

highest_median_salary = clean_df.sort_values(
    "Mid-Career Median Salary",
    ascending=False
)

print()
print("TOP 5 MAJORS WITH HIGHEST MID-CAREER MEDIAN SALARY")
print()
print(
    highest_median_salary[
        ["Undergraduate Major", "Mid-Career Median Salary"]
    ].head()
)


# ============================ GROUPBY ANALYSIS ============================ #

print()
print("NUMBER OF MAJORS IN EACH GROUP")
print()
print(clean_df.groupby("Group").count())


# ============================ GROUP AVERAGES ============================ #

# Format floating-point numbers for better readability.
pd.options.display.float_format = "{:,.2f}".format
print()
print("AVERAGE NUMERIC VALUES FOR EACH GROUP")
print()
print(clean_df.groupby("Group").mean(numeric_only=True))



