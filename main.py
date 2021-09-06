## Import libraries
import pandas as pd

## Read in quintile data
# I made a csv of table H-3 
# All values are in 2019 dollars as provided by the Census: https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html
hist_income = pd.read_csv("hist_income.csv")

## Cleaning
# Footnotes for the data are available here: https://www.census.gov/topics/income-poverty/income/guidance/cps-historic-footnotes.html

# Fix Years
#remove the footnotes that are linked in parentheses
hist_income['Year'] = hist_income['Year'].str.replace(r"\(.*\)" , "")

# Change data types


# Rename columns


# Average of years with multiple values


print(hist_income.head())