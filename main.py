## Import libraries
import numpy as np
import pandas as pd
import altair as alt

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
hist_income = hist_income.pct_change() #percent change
hist_income = hist_income.dropna() #filter out the first year since it's NA for percent change
hist_income = hist_income.apply(lambda x: x * 100) # multiply by 100 for convenience

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

# make a lagged dataframe to give each president a 1 year lag before their economic policy kicks in. 
pres_lag = pres.shift(periods = -1)
df_lag = pres_lag.join(hist_income)


# transform data from wide to long
df = pd.melt(df, id_vars = ['Democrat'], value_vars =['20', '40', '60', '80', '95'], ignore_index = False, var_name = "Percentile", value_name = "Growth")
df_lag = pd.melt(df_lag, id_vars = ['Democrat'], value_vars =['20', '40', '60', '80', '95'], ignore_index = False, var_name = "Percentile", value_name = "Growth")


# Plot data in altair
df['Party'] = np.where(df['Democrat']== True, 'Dem', 'Rep')
df_lag['Party'] = np.where(df_lag['Democrat']== True, 'Dem', 'Rep')

#set up for colors
domain = ['Dem', 'Rep']
range_ = ['blue', 'red']

#Unlagged chart
chart = alt.Chart(df).mark_bar().encode(
    alt.X('Party', title = ""),
    alt.Y('mean(Growth)', title = "Percent Growth"),
    color = alt.Color('Party', scale = alt.Scale(domain = domain, range = range_)),
    column = 'Percentile'
).properties(
    title = 'Avg Annual Income Growth, 1947-2019'
)
chart.save("pres.html")

#Unlagged chart
chart_lag = alt.Chart(df_lag).mark_bar().encode(
    alt.X('Party', title = ""),
    alt.Y('mean(Growth)', title = "Percent Growth"),
    color = alt.Color('Party', scale = alt.Scale(domain = domain, range = range_)),
    column = 'Percentile'
).properties(
    title = 'Avg Annual Income Growth, 1947-2019, 1 year lag'
)
chart_lag.save("pres_lag.html")

# save data as images https://altair-viz.github.io/user_guide/saving_charts.html
