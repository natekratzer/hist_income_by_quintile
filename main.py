## Import libraries
import pandas as pd

## Read in quintile data
# I made a csv of table F-1: https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-families.html
# All values are in 2019 dollars as provided by the Census
hist_income = pd.read_csv("hist_income47.csv")

## Cleaning
# Footnotes for the data are available here: https://www.census.gov/topics/income-poverty/income/guidance/cps-historic-footnotes.html

# Fix Years
#remove the footnotes that are linked in parentheses
hist_income['Year'] = hist_income['Year'].str.replace(r"\(.*\)" , "")

#remove all commas
hist_income = hist_income.apply(lambda x: x.str.replace(',', '')) #using a lambda function and applying to all columns

# Dictionary to retype columns
type_dict = {
    "Year"  : "datetime64[ns]", 
    "20"  : "int32",
    "40" : "int32",
    "60" : "int32",
    "80" : "int32",
    "95": "int32"
}

# Change data types
hist_income = hist_income.astype(type_dict)

# Average of years with multiple values
# See linked footnotes above - two slightly different methods available for each year
hist_income = hist_income.groupby(['Year']).mean() #this also turns year into my index, which is convenient for later applying changes to all columns except year

print(hist_income.head())

hist_income = hist_income.pct_change() #percent change
hist_income = hist_income.dropna() #filter out the first year since it's NA for percent change
hist_income = hist_income.apply(lambda x: x * 100) # multiply by 100 for convenience

print(hist_income.head())

## Pull in presidential data
pres = pd.read_csv("pres_year.csv")

pres["Year"] = pd.to_datetime(pres["Year"], format = "%Y") # need to manually convert because going straight from int to date causes issues

# Dictionary to retype columns
type_dict_pres = {
    "Year"  : "datetime64[ns]", 
    "President"  : "string",
    "Term" : "string",
    "Democrat" : "bool",
    "Second Term" : "bool"
}

# Change data types
pres = pres.astype(type_dict_pres)

pres = pres.set_index("Year")

# Join datasets
df = pres.join(hist_income) #join is for joining on index, merge is for merging on columns

print(df.head())

# make a lagged dataframe

# transform data from wide to long
df = pd.melt(df, id_vars = ['Democrat'], value_vars =['20', '40', '60', '80', '95'], ignore_index = False, var_name = "Percentile", value_name = "Growth")

print(df.head())

# Plot data in altair
import altair as alt

chart = alt.Chart(df).mark_bar().encode(
    x = 'Democrat',
    y = 'mean(Growth)',
    color = 'Democrat',
    column = 'Percentile'
)

chart.save("test_alt.html")

# save data as images https://altair-viz.github.io/user_guide/saving_charts.html
