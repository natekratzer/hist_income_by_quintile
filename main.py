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

#remove all commas
hist_income = hist_income.apply(lambda x: x.str.replace(',', '')) #using a lambda function and applying to all columns

# Rename columns
rename_dict = {
    "Year" : "year",
    "Lowest\nfifth" : "0-20",
    "Second\nfifth" : "20-40",
    "Middle\nfifth" : "40-60",
    "Fourth\nfifth" : "60-80",
    "Highest\nfifth" : "80-100",
    "Top 5\npercent" : "95-100"
}

hist_income = hist_income.rename(columns = rename_dict)

# Dictionary to retype columns
type_dict = {
    "year"  : "datetime64[ns]", 
    "0-20"  : "int32",
    "20-40" : "int32",
    "40-60" : "int32",
    "60-80" : "int32",
    "80-100": "int32",
    "95-100": "int32"
}

# Change data types
hist_income = hist_income.astype(type_dict)

# Average of years with multiple values
# See linked footnotes above - two slightly different methods available for each year
hist_income = hist_income.groupby(['year']).mean() #this also turns year into my index, which is convenient for later applying changes to all columns except year

print(hist_income.head())

hist_income = hist_income.pct_change() #percent change
hist_income = hist_income.dropna() #filter out the first year since it's NA for percent change
hist_income = hist_income.apply(lambda x: x * 100) # multiply by 100 for convenience

print(hist_income.head())

## Pull in presidential data

# Join datasets

# Plot data in altair

# save data as images https://altair-viz.github.io/user_guide/saving_charts.html
