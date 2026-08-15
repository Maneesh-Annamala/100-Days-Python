import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

pd.options.display.float_format = '{:,.2f}'.format

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
df_monthly = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])

print(df_yearly.shape)
print(df_monthly.shape)

print(df_yearly.columns)
print(df_monthly.columns)

print(df_yearly.isna().sum())
print(df_monthly.isna().sum())

print(df_yearly.duplicated().sum())
print(df_monthly.duplicated().sum())

print(df_monthly.head())

print(f"Average births: {df_monthly['births'].mean():.2f}")
print(f"Average deaths: {df_monthly['deaths'].mean():.2f}")

prob = df_yearly['deaths'].sum() / df_yearly['births'].sum() * 100
print(f"Percentage of women dying in childbirth: {prob:.2f}%")

# Monthly births and deaths
plt.figure(figsize=(12, 6))
plt.title("Deaths and Births in the 1840s")

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.plot(
    df_monthly['date'],
    df_monthly['births'],
    color='skyblue',
    label='Birth',
    linewidth=3
)

ax2.plot(
    df_monthly['date'],
    df_monthly['deaths'],
    color='crimson',
    label='Deaths',
    linestyle='--',
    linewidth=2
)

ax1.grid(True)
ax1.set_xlabel('Years')
ax1.set_ylabel('Number of Births', color='skyblue')
ax2.set_ylabel('Number of Deaths', color='crimson')

plt.show()

print(df_yearly.sample(10))

# Births by clinic
birth_chart = px.line(
    df_yearly,
    x='year',
    y='births',
    color='clinic',
    title='Births by Clinic'
)

birth_chart.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Births'
)

birth_chart.show()

# Deaths by clinic
death_chart = px.line(
    df_yearly,
    x='year',
    y='deaths',
    color='clinic',
    title='Deaths by Clinic'
)

death_chart.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Deaths'
)

death_chart.show()

# Death percentage by clinic
df_yearly['pct_deaths'] = (
    df_yearly['deaths'] / df_yearly['births'] * 100
)

print(df_yearly.groupby('clinic')['pct_deaths'].mean())

death_pct_chart = px.line(
    df_yearly,
    x='year',
    y='pct_deaths',
    color='clinic',
    title='Percentage of Deaths by Clinic'
)

death_pct_chart.update_layout(
    xaxis_title='Year',
    yaxis_title='Percentage of Deaths'
)

death_pct_chart.show()

# Compare death rates before and after handwashing
handwashing_start = pd.to_datetime('1847-06-01')

df_monthly['pct_deaths'] = (
    df_monthly['deaths'] / df_monthly['births'] * 100
)

before_handwash = df_monthly[
    df_monthly['date'] < handwashing_start
]

after_handwash = df_monthly[
    df_monthly['date'] >= handwashing_start
]

before_avg = before_handwash['pct_deaths'].mean()
after_avg = after_handwash['pct_deaths'].mean()

print(f"Average death rate before June 1847: {before_avg:.2f}%")
print(f"Average death rate after June 1847: {after_avg:.2f}%")

before_handwash = before_handwash.sort_values('date')

rolling_df = (
    before_handwash
    .set_index('date')
    .rolling(window=6)
    .mean()
)

print(rolling_df.head(10))

# Death rate over time
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(12, 6))
plt.title("Deaths and Births in the 1840s")

ax = plt.gca()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)

plt.grid(True)
plt.xlabel('Years')
plt.ylabel('Percentage of Deaths')

ax.set_xlim(
    df_monthly['date'].min(),
    df_monthly['date'].max()
)

before_line, = plt.plot(
    before_handwash['date'],
    before_handwash['pct_deaths'],
    color='black',
    linestyle='dotted',
    linewidth=1,
    label='Before Handwashing'
)

rolling_line, = plt.plot(
    rolling_df.index,
    rolling_df['pct_deaths'],
    color='crimson',
    linestyle='--',
    linewidth=3,
    label='6-Month Moving Average'
)

after_line, = plt.plot(
    after_handwash['date'],
    after_handwash['pct_deaths'],
    color='skyblue',
    marker='o',
    linewidth=2,
    label='After Handwashing'
)

plt.legend(handles=[before_line, rolling_line, after_line])
plt.show()

beforewash = before_handwash['pct_deaths'].mean()
afterwash = after_handwash['pct_deaths'].mean()

death_diff = beforewash - afterwash
improvement = beforewash / afterwash

print(f"Average monthly deaths before handwashing: {beforewash:.2f}%")
print(f"Average monthly deaths after handwashing: {afterwash:.2f}%")
print(f"Difference in average death rate: {death_diff:.2f}%")
print(f"Improvement: {improvement:.2f} times")

df_monthly['washing'] = np.where(
    df_monthly['date'] < handwashing_start,
    'Before',
    'After'
)

# Box plot
box = px.box(
    df_monthly,
    x='washing',
    y='pct_deaths',
    color='washing',
    title='Death Rate Before and After Handwashing'
)

box.update_layout(
    xaxis_title='Handwashing',
    yaxis_title='Percentage of Deaths'
)

box.show()

# Histogram
hist = px.histogram(
    df_monthly,
    x='pct_deaths',
    color='washing',
    nbins=30,
    opacity=0.6,
    barmode='overlay',
    histnorm='percent',
    marginal='box'
)

hist.update_layout(
    xaxis_title='Percentage of Monthly Deaths',
    yaxis_title='Percentage of Months'
)

hist.show()

# KDE distribution
plt.figure(dpi=200)

sns.kdeplot(
    before_handwash['pct_deaths'],
    fill=True,
    label='Before Handwashing'
)

sns.kdeplot(
    after_handwash['pct_deaths'],
    fill=True,
    label='After Handwashing'
)

plt.xlim(0, 40)
plt.title("Death Rate Before vs After Handwashing")
plt.legend()
plt.show()

# Independent t-test
t_stat, p_value = stats.ttest_ind(
    before_handwash['pct_deaths'],
    after_handwash['pct_deaths']
)

print(f"P-value: {p_value:.10f}")
print(f"T-statistic: {t_stat:.4f}")