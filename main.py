import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine

# Load the dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Load the data (replace 'Airbnb.csv' with your actual dataset file path)
df = load_data("D:\Jupyter\Airbnb.csv")

# Display the first few rows of the dataset
st.write("### Airbnb Dataset")
st.write(df.head())

# Step 1: Display the world map
st.header("World Map of Airbnb Listings")

# Group the data by country and count the number of listings
country_counts = df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

# Create the Plotly choropleth map for world view
fig_world = px.choropleth(
    country_counts,
    locations="country",
    locationmode='country names',
    color="count",
    hover_name="country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Airbnb Listings by Country'
)

# Update the layout of the world map
fig_world.update_layout(
    height=600,
    margin={"r":0,"t":50,"l":0,"b":0}
)

# Display the world map
st.plotly_chart(fig_world)

# visualization
country_list = ['United States', 'Turkey', 'Hong Kong', 'Australia', 'Portugal','Brazil', 'Canada', 'Spain', 'China']
selected_country = st.selectbox("Select a country:", country_list)
market_list = df["market"][df["country"] == selected_country].unique()
selected_market = st.selectbox("Select a market:", market_list)

# Filter the data based on the selected country and market
filtered_data = df[(df["country"] == selected_country) & (df["market"] == selected_market)]

# Display the filtered data
st.write(f"### Airbnb Listings in {selected_market}, {selected_country}")
st.write(filtered_data.head())

availability_data  = {}
df_1 = df[(df['country'] == selected_country) & (df['market'] == selected_market)]

df_availability_30 = df_1[df_1["availability_30"]!=0]
df_availability_60 = df_1[df_1["availability_60"]!=0]
df_availability_90 = df_1[df_1["availability_90"]!=0]
df_availability_365 = df_1[df_1["availability_365"]!=0]

availability_data ["availability_30"]=df_availability_30["availability_30"].count()
availability_data ["availability_60"]=df_availability_60["availability_60"].count()
availability_data ["availability_90"]=df_availability_90["availability_90"].count()
availability_data ["availability_365"]=df_availability_365["availability_365"].count()

# Convert the dictionary to a DataFrame
availability_df = pd.DataFrame(list(availability_data.items()), columns=['Availability', 'Count'])

# Create the pie chart
fig_pie = px.pie(
    availability_df, 
    names='Availability', 
    values='Count', 
    title='Availability Distribution',
    hole = 0.5
)

# Display the pie chart in Streamlit
st.plotly_chart(fig_pie)

# Create the scatter plot
fig_scatter = px.scatter(
    filtered_data,
    x='host_neighbourhood',
    y='price',
    # size='review_scores',  # Use review scores for size
    color='review_scores',  # Use price for color
    color_continuous_scale=px.colors.sequential.Viridis,
    hover_name='host_neighbourhood',
    hover_data={
        'price': True,
        'review_scores': True,
        'host_name': True
    },
    title=f'Listings in {selected_market}, {selected_country}'
)

# Display the scatter plot in Streamlit
st.plotly_chart(fig_scatter)

# Group by property type and calculate mean price
mean_price_by_property_type = filtered_data.groupby("property_type")[["price"]].mean().reset_index()

# Create the line plot
fig_line = px.line(
    mean_price_by_property_type,
    x='property_type',
    y='price',
    title=f'Mean Price by Property Type in {selected_market}, {selected_country}',
    labels={'property_type': 'Property Type', 'price': 'Mean Price'}
)

# Display the line plot in Streamlit
st.plotly_chart(fig_line)

count_by_property_type = df_1.groupby("property_type")[["_id"]].count().reset_index()

# Create the line plot
fig_bar = px.bar(
    count_by_property_type,
    x='property_type',
    y='_id',
    title=f'Count by Property Type in {selected_market}, {selected_country}',
    labels={'property_type': 'Property Type', '_id': 'Count'}
)

# Display the line plot in Streamlit
st.plotly_chart(fig_bar)

# Function to execute SQL query and return DataFrame
def execute_query(query):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1234',
        db='airbnb'
    )
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  password = "1234",
  auth_plugin = "mysql_native_password"
)

# Create a new database and use
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS airbnb")

# Close the cursor and database connection
mycursor.close()
mydb.close()

# Connect to the newly created database
engine = create_engine('mysql+mysqlconnector://root:1234@127.0.0.1/airbnb', echo=False)