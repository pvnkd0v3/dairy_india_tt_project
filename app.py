import streamlit as st
import pandas as pd 
import plotly.express as px



#Read and prepare dataset
url = 'https://raw.githubusercontent.com/pvnkd0v3/dairy_india_tt_project/main/dairy_dataset.csv'
dairy_df = pd.read_csv(url)
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
st.markdown('**From a dataset containing 4325 dairy sales across India from 2019 to 2022, we looked at how the quanity of dairy sold, the prices, and total revenue made from dairy sales in India might have been affected by the onset of the COVID-19 lockdowns. Below are visualizations and statistical info condensed from the full Jupyter Notebook project exploring the data.**')
st.divider()

#Plot a histogram of dairy volume purchased by year that is overlaid by default unless the 'stacked' checkbox is ticked
st.markdown('**Let\'s look at out first chart. Below is the distribution of the volume of dairy purchased in India for each year represented in the data. For a closer look at each year\'s distribution, check the box below to stack the data:**')
volume_stacked = st.checkbox('Stack the dairy volume data?')

if volume_stacked:
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
    st.plotly_chart(fig)

st.write('It appears that the volume of dairy sold by year is distributed similarly with a right skew initially indicating that there may not be a correlation between the amount of dairy sold in India and COVID-19 lockdowns.')
st.write('T-tests performed on the 2019 and 2020 data proves this initial impression right as there was:')
st.write('- A 51.7 percent likelihood that dairy volume sold in 2019 differing from the following 3 years is simply by chance')
st.write('- A 49.6 percent likelihood that dairy volume sold in 2020 differing from 2019, 2021, and 2022 is simply by chance')
st.write('Both percentages are too high to make a concrete correlation between the volume of dairy sold in India and the onset of the COVID-19 lockdowns.')
st.divider()

#Plot a histogram of prices of dairy unit sold by year that is overlaid by default unless the 'stacked' checkbox in ticked
st.markdown('**Below is a distribution of the dairy prices in India per unit sold in each year represented by the data. For a closer look at each year\'s distribution, check the box below to stack the data:**')

prices_stacked = st.checkbox('Stack the dairy prices data?')
if prices_stacked:
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
    st.plotly_chart(fig)

else:
    fig = px.histogram(dairy,
                   x='price_per_unit_sold', 
                   color='year',
                   title='Dairy Prices in India 2019-2022 (Years Overlaid)',
                   color_discrete_map={2019: 'red', 2020: 'orange', 2021: 'green', 2022: 'blue'},
                   opacity=0.5,
                   barmode='overlay',
                   category_orders=sequential_years,
                   nbins=40)

    fig.update_xaxes(title_text='Price per Unit')
    fig.update_yaxes(title_text='Count')
    st.plotly_chart(fig)

st.write('The prices of dairy per unit in India by year from 2019-2022 appear to be similarly distributed.')
st.write('T-tests performed on the 2019 and 2020 data proves this initial impression right as there was:')
st.write('- A 14.7 percent likelihood that dairy prices in India in 2019 differing from that of the following 3 years is simply by chance')
st.write('- A 71.8 percent likelihood that dairy prices in India in 2020 differing from 2019, 2021, and 2022 is simply by chance')
st.write('Both percentages are too high to make a concrete correlation between dairy prices in India and the onset of the COVID-19 lockdowns.')
st.divider()

# Plot a scatter chart that shows the total revenue per month from dairy sales in India over the 4 years represesnted in the data
st.markdown('**Lastly, below is a scatter plot depicting the total revenue from dairy sales in India each month from 2019-2022:**')

fig = px.scatter(monthly_rev,
              x='month_year',
              y='approx_revenue_inr',
              title='Approximate Dairy Revenue in India (2019-2022)',
              trendline='ols')
fig.update_xaxes(title_text='Month')
fig.update_yaxes(title_text='Approximate Revenue (INR)')
st.plotly_chart(fig)

st.write('The month with the highest revenue was January 2021 with the lowest in August 2022. The line of best fit indicates a very general decline in revenue from before to after the COVID-19 lockdowns.')
st.write('T-tests performed on the 2019 and 2020 data proves this initial impression right as there was:')
st.write('- A 67.2 percent likelihood that dairy revenue in India in 2019 differing from that of the following 3 years is simply by chance')
st.write('- A 29.3 percent likelihood that dairy revenue in India in 2020 differing from 2019, 2021, and 2022 is simply by chance')
st.write('Both percentages are too high to make a concrete correlation between the total revenue from dairy sales in India and the onset of the COVID-19 lockdowns.')
st.divider()


st.header('The Answer')
st.markdown('**From the data available, it does not appear that the COVID-19 lockdowns had any significant affect on the volume of dairy purchased, the retail prices of dairy, nor the revenue made from the dairy industry in India. All t-tests performed on these variables in regaurds to their values before and after the lockdowns resulted in p-values larger than the significace threshhold of 5%. This means that the likelihood of any correlation between the COVID-19 lockdowns and any changes in India\'s dairy industry being simply by chance is too high to state those correlations as fact. The dataset provided spans one year before the lockdowns began, and three years after they began. In order to get a more solid understanding on any affects the lockdowns could have had on India\'s dairy industry, a bigger sample size spanning across a longer period surrounding the COVID-19 lockdowns is recommended. Specifically, data that spans an equal amount of years before and after 2020 would be ideal.**')