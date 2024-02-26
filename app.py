import streamlit as st
import pandas as pd 
import plotly.express as px

#Read and prepare dataset
dairy_df = pd.read_csv('/home/kt/coding/tripleten_projects/dairy_india/dairy_dataset.csv')
dairy = dairy_df.iloc[:, [4,5,15,16,17,22]].copy()

    ##Convert columns to snakecase
def to_snake_case(column_name):
        ### Converting each column name to snakcase by splitting them by spaces and join using underscores
    return '_'.join(column_name.lower().split())


        ### Apply the to_snake_case function to each column
dairy.columns = [to_snake_case(col) for col in dairy.columns]


    ##Rename columns
dairy.rename(columns={'quantity_sold_(liters/kg)': 'l/kg_sold',
                      'price_per_unit_(sold)': 'price_per_unit_sold',
                      'approx._total_revenue(inr)': 'approx_revenue_inr',
                      'reorder_quantity_(liters/kg)': 'l/kg_reordered'},
            inplace=True)


    ##Change date column to datetime type
dairy['date'] = pd.to_datetime(dairy['date'], format='%Y-%m-%d')


#Define any needed variables or columns from the dairy.ipynb notebook
dairy['year'] = dairy['date'].dt.year
dairy['year'] = pd.Categorical(dairy['year'], categories=[2019, 2020, 2021, 2022], ordered=True)
sequential_years = {'year': [2019, 2020, 2021, 2022]}
dairy['month_year'] = dairy['date'].dt.to_period('M').astype(str)
dairy['month_year'] = pd.to_datetime(dairy['month_year'])
monthly_volume = dairy.groupby('month_year')['l/kg_sold'].sum().reset_index()
monthly_rev = dairy.groupby('month_year')['approx_revenue_inr'].sum().reset_index()


#Title and app description
st.header('Has COVID-19 Affected Dairy Sales in India?')
st.write('From a dataset containing xxx dairy sales in India from 2019 to 2022, we looked at how the quanity of dairy sold, the prices, and total revenue made might have been affected by the onset of the COVID-19 lockdowns.')


#Plot a histogram of dairy volume purchased by year that is overlaid by default unless the 'stacked' checkbox is ticked
st.write('Below is the distribution of the volume of dairy purchased in India for each year represented in the data. For a better look at each year\'s distribution, check the box below to stack the data.')
stacked = st.checkbox('Stack the data?')

if stacked:
    fig = px.histogram(dairy,
                   x='l/kg_sold', 
                   color='year',
                   title='Dairy Sold in India 2019-2022',
                  color_discrete_map={2019: 'red', 2020: 'orange', 2021: 'green', 2022: 'blue'},
                   opacity=0.5,
                  category_orders=sequential_years,
                  nbins=40)

    fig.update_xaxes(title_text='Dairy Sold (l/kg)')
    fig.update_yaxes(title_text='Count')
    fig.show()
    st.plotly_chart(fig)

else:
    fig = px.histogram(dairy,
                   x='l/kg_sold', 
                   color='year',
                   title='Dairy Sold in India 2019-2022',
                  color_discrete_map={2019: 'red', 2020: 'orange', 2021: 'green', 2022: 'blue'},
                   opacity=0.5,
                  barmode='overlay',
                  category_orders=sequential_years,
                  nbins=40)

    fig.update_xaxes(title_text='Dairy Sold (l/kg)')
    fig.update_yaxes(title_text='Count')
    fig.show()
    st.plotly_chart(fig)

#WRITE SOMETHING HERE ABOUT DAIRY VOLUME HISTOGRAM

#Plot a histogram of prices of dairy unit sold by year that is overlaid by default unless the 'stacked' checkbox in ticked
st.write('Below is the distribution of the dairy prices in India per unit sold in each year represented by the data.')

st.write(stacked)
i
f stacked:
    fig = px.histogram(dairy,
                   x='price_per_unit_sold', 
                   color='year',
                   title='Dairy Prices in India 2019-2022 (Years Overlaid)',
                   color_discrete_map={2019: 'red', 2020: 'orange', 2021: 'green', 2022: 'blue'},
                   opacity=0.5,
                  category_orders=sequential_years,
                  nbins=40)

    fig.update_xaxes(title_text='Price per Unit')
    fig.update_yaxes(title_text='Count')
    fig.show()
    st.plotly_chart(fig)

else:
    fig = px.histogram(dairy,
                   x='price_per_unit_sold', 
                   color='year',
                   title='Dairy Prices in India 2019-2022 (Years Overlaid)',
                   color_discrete_map={2019: 'red', 2020: 'orange', 2021: 'green', 2022: 'blue'},
                   opacity=0.5,
                   barmode='overlay'
                  category_orders=sequential_years,
                  nbins=40)

    fig.update_xaxes(title_text='Price per Unit')
    fig.update_yaxes(title_text='Count')
    fig.show()
    st.plotly_chart(fig)

#WRITE SOMETHING HERE ABOUT DAIRY PRICES HISTOGRAM

# Plot a scatter chart that shows the total revenue per month from dairy sales in India over the 4 years represesnted in the data
st.write('Below is a scatter plot depicting the total revenue from dairy sales in India each month from 2019-2022.')

fig = px.scatter(monthly_rev,
              x='month_year',
              y='approx_revenue_inr',
              title='Approximate Dairy Revenue in India (2019-2022)',
              trendline='ols')
fig.update_xaxes(title_text='Month')
fig.update_yaxes(title_text='Approximate Revenue (INR)')
fig.show()
st.plotly_chart(fig)

#WRITE SOMETHING HERE ABOUT THE MONTHLY REVENUE SCATTER PLOT


#WRITE SOMETHING HERE WITH CONCLUSIONS ABOUT THE PROJECT