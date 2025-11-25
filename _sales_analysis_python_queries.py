%md
### **Meta Data**

A generic, simulated dataset which indicates the daily trading information for a large retail store has been provided. The data is only for one of the products sold at the store. The objective is to derive meaningful metrics.
%md
## **Import Libraries**
#Panda library - a library used to process data on python
import pandas as pd

#Numpy Library - a library used to process mathematical operations on python
import numpy as np

#Matplotlib Library - a library used to plot graphs on python
import matplotlib.pyplot as plt

import plotly
# this is a library used to plot graphs on python
import plotly.express as px
import plotly.graph_objects as go


%md
## **Data Load**
#Data source
data_path = "/Workspace/Users/mokwenakoketso5@gmail.com/Sales Case Study (2).csv"

#Reading the data file from the source using pandas
sales_analysis = pd.read_csv('/Workspace/Users/mokwenakoketso5@gmail.com/Sales Case Study (2).csv')

#Displaying the data
display(sales_analysis)
%md
## **Exploratory Data Analysis**
# 1. Checking the number of rows and columns in the dataset
sales_analysis.shape
%md
The dataset has 1053 rows and 4 colums
# 2. Checking the data type of each column
sales_analysis.dtypes

%md
The Date column is incorrectly read as object data type
#Correcting the date column to datetime
sales_analysis['Date'] = pd.to_datetime(sales_analysis['Date'])

sales_analysis.dtypes
%md
All columns data types are correct
# 3. Checking for duplicates in the dataset
sales_analysis.duplicated().sum()
%md
Zero duplicates found
# 4. Checking for missing values in each column
sales_analysis.isnull().sum()
%md
There are no null/missing values in the dataset
%md
## **Data metrics And Insights**
%md
1. Calculating the daily sales price per unit

# Calculating the sales price per unit
sales_analysis['Sales Price Per Unit'] = sales_analysis['Sales'] / sales_analysis['Quantity Sold']
print(sales_analysis)

%md
The sales price per unit for each day is shown in the last column created after the calculations.
%md
2. The average unit sales price of this product
# Calculating the average sales price of the product
average_sales_price = sales_analysis['Sales Price Per Unit'].mean()
print(average_sales_price)
%md
The average unit sales price of this product is R37.07
%md
3.The daily % gross profit of this product
# Calculating the % gross profit of this product
sales_analysis['Gross Profit Percentage'] = (sales_analysis['Sales'] - sales_analysis['Cost Of Sales']) / sales_analysis['Sales'] *100
print(sales_analysis)
%md
Insight 1: Negative % gross profit means Cost of Sales was higher than Sales and therefore loss instead of profit was made

Insight 2: Positive % gross profit means the Sales was higher than the Cost of Sales therefore profit was made
%md
4. The % gross profit per unit
# Calculating the percentage gross profit per unit
sales_analysis['Cost of Sale Per Unit'] = sales_analysis['Cost Of Sales'] / sales_analysis['Quantity Sold']
sales_analysis['Gross Profit Per Unit'] = sales_analysis['Sales Price Per Unit'] - sales_analysis['Cost of Sale Per Unit']
sales_analysis['Gross Profit % Per Unit'] = (sales_analysis['Gross Profit Per Unit'] / sales_analysis['Sales Price Per Unit']) * 100
display(sales_analysis)
%md
Price Elasticity of Demand
sales_analysis.plot(x='Date', y='Sales')
#Change to datetime date format
promotional_periods = [(pd.to_datetime('2014-02-27'), pd.to_datetime('2014-03-02')),
                       (pd.to_datetime('2014-08-28'), pd.to_datetime('2014-08-31')),
                       (pd.to_datetime('2015-03-30'), pd.to_datetime('2015-04-05')),]


def calculate_ped(sales_analysis, start_date, end_date):

    # Filter date period
    period_df = sales_analysis[
        (sales_analysis['Date'] >= start_date) &
        (sales_analysis['Date'] <= end_date)
    ]

    # Check if empty
    if period_df.empty:
        return {
            'start_date': start_date,
            'end_date': end_date,
            'error': 'No data available for this period'
        }

    # Extract initial and final values
    initial_price = period_df.iloc[0]['Sales Price Per Unit']
    final_price = period_df.iloc[-1]['Sales Price Per Unit']

    initial_quantity = period_df.iloc[0]['Quantity Sold']
    final_quantity = period_df.iloc[-1]['Quantity Sold']

    # Percentage changes
    price_change = (final_price - initial_price) / initial_price * 100
    quantity_change = (final_quantity - initial_quantity) / initial_quantity * 100

    # PED
    ped = quantity_change / price_change if price_change != 0 else float('inf')

    return {
        'start_date': start_date,
        'end_date': end_date,
        'initial_price': initial_price,
        'final_price': final_price,
        'initial_quantity': initial_quantity,
        'final_quantity': final_quantity,
        'price_change': price_change,
        'quantity_change': quantity_change,
        'ped': ped
    }

results = [calculate_ped(sales_analysis, start, end) for start, end in promotional_periods]


# Display results nicely
for result in results:
    display(result)

# Print analysis
for result in results:
    if 'error' in result:
        print(f"Period: {result['start_date']} to {result['end_date']}: {result['error']}")
        continue

    print(f"Period: {result['start_date']} to {result['end_date']}")
    print(f"PED: {result['ped']}")

    if result['ped'] > 1:
        print("→ Elastic demand (high sensitivity to price changes)")
    elif result['ped'] < 1:
        print("→ Inelastic demand (low sensitivity to price changes)")
    else:
        print("→ Unit elastic")
    print()



