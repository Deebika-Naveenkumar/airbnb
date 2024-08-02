import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Streamlit page configuration
st.set_page_config(layout="wide")

# Function to load data
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

df = load_data("file_path.csv")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Features", "Data Analysis"],
        icons=["house-door", "globe2", "patch-question"],
        menu_icon="emoji-smile",
        default_index=0
    )

# Home menu
if selected == "Home":
    st.title(":red[AIRBNB ANALYSIS]") 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(':blue[ABOUT AIRBNB]')
        st.write("""
        - Airbnb is an American company well-known for short-term housing rentals. The company acts as a broker and charges a commission from each booking.
        - The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. It is a shortened version of AirBedandBreakfast.com. 
        - **Mission**: “To create a world where anyone can belong anywhere.”
        - **Vision**: “Belong Anywhere.”
        """)
    with col2:
        st.image(Image.open("file_path.jpg"), width=400)
    
    st.subheader(':blue[TECHNOLOGIES USED]')
    st.write("""
    - Plotly: To plot and visualize the data
    - Pandas: To Clean and manipulate the data
    - Streamlit: To Create Graphical User Interface
    - Power BI: To Create Dashboard
    """)

# Features menu
elif selected == "Features":
    st.subheader(':blue[FEATURE DESCRIPTION]')
    st.write("""
    - ID: Unique identifier for each listing.
    - Property Type: The type of property being listed (e.g., apartment, house, villa, etc.).
    - Room Type: The type of room available for rent (e.g., entire home/apt, private room, shared room).
    - Bed Type: The type of bed available in the listing (e.g., real bed, futon, pull-out sofa).
    - Cancellation Policy: The policy regarding cancellations (e.g., flexible, moderate, strict).
    - Number of Reviews: The total number of reviews the listing has received.
    - Price: The price to rent the listing.
    - Review Scores: Scores given by guests.
    - Host ID: Unique identifier for the host of the listing.
    - Host Name: The name of the host.
    - Host Location: The location of the host.
    - Host Neighbourhood: The specific neighborhood where the host is located.
    - Street: The street address of the listing.
    - Suburb: The suburb or district where the listing is located.
    - Government: The governing authority or administrative division (this might be the state, province, or local government area).
    - Market: The market or region where the listing is located.
    - Country: The country where the listing is located.
    - Country Code: Code for the country.
    - Latitude: The latitude coordinate of the listing's location.
    - Longitude: The longitude coordinate of the listing's location.
    - Is Location Exact: Tells whether the provided latitude and longitude coordinates are exact or approximate.
    - Availability 30: The number of days the listing is available for booking within the next 30 days.
    - Availability 60: The number of days the listing is available for booking within the next 60 days.
    - Availability 90: The number of days the listing is available for booking within the next 90 days.
    - Availability 365: The number of days the listing is available for booking within the next 365 days.
    """)

# Data Analysis menu
elif selected == "Data Analysis":
    st.subheader(':blue[SAMPLE AIRBNB DATASET]')
    st.write(df.head())

    st.subheader(':blue[WORLD MAP OF AIRBNB LISTINGS]')
    country_counts = df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']

    fig_world = px.choropleth(
        country_counts,
        locations="country",
        locationmode='country names',
        color="count",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig_world.update_layout(
        height=500,
        margin={"r":0,"t":50,"l":0,"b":0},
        title_text="AIRBNB LISTINGS COUNT BY COUNTRY",
        title_x=0.4
    )
    st.plotly_chart(fig_world)

    st.markdown(' ')
    st.markdown(' ')
    st.subheader(':blue[ANALYSIS BASED ON COUNTRY AND MARKET]')
    col1, col2 = st.columns(2)
    country_list = df['country'].unique()
    selected_country = col1.selectbox("Select a country:", country_list)
    market_list = df["market"][df["country"] == selected_country].unique()
    selected_market = col2.selectbox("Select a market:", market_list)

    filtered_data = df[(df["country"] == selected_country) & (df["market"] == selected_market)]

    # Sunburst chart for availability
    def create_sunburst(data):
        availability_categories = ['availability_30', 'availability_60', 'availability_90', 'availability_365']
        sunburst_data_list = []
        for category in availability_categories:
            temp_data = data[data[category] > 0].copy()
            temp_data['availability'] = category
            sunburst_data_list.append(temp_data[['_id', 'property_type', 'room_type', 'availability']])
        sunburst_data = pd.concat(sunburst_data_list)
        sunburst_data_grouped = sunburst_data.groupby(['property_type', 'room_type', 'availability']).size().reset_index(name='count')
        fig_sunburst = px.sunburst(
            sunburst_data_grouped,
            path=['property_type', 'room_type', 'availability'],
            values='count',
            title=f'AVAILABILTY OF ROOMS IN {selected_market.upper()}, {selected_country.upper()}',
            color="count",
            color_continuous_scale='RdBu',
            height=500
        )
        st.plotly_chart(fig_sunburst)

    create_sunburst(filtered_data)

    # Scatter plot for neighborhood price and review scores
    fig_scatter = px.scatter(
        filtered_data,
        x='host_neighbourhood',
        y='price',
        color='review_scores',
        color_continuous_scale="sunsetdark",
        hover_name='host_neighbourhood',
        hover_data={'price': True, 'review_scores': True, 'host_name': True},
        title=f'LISTINGS IN {selected_market.upper()}, {selected_country.upper()}',
        labels={'host_neighbourhood': 'Host Neighbourhood', 'price': 'Price'}
    )
    fig_scatter.update_layout(title_x=0.4)
    st.plotly_chart(fig_scatter)

    # Mean price by property type
    def plot_mean_price_by_property_type(data, title):
        mean_price_by_property_type = data.groupby("property_type")[["price"]].mean().reset_index()
        fig = px.line(
            mean_price_by_property_type,
            x='property_type',
            y='price',
            title=title,
            labels={'property_type': 'Property Type', 'price': 'Mean Price'}
        )
        fig.update_layout(title_x=0.4)
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_mean_price_by_property_type(filtered_data, f'MEAN PRICE BY PROPERTY TYPE IN {selected_market.upper()}, {selected_country.upper()}'))
    with col2:
        st.plotly_chart(plot_mean_price_by_property_type(df, 'MEAN PRICE BY PROPERTY TYPE COUNTRYWIDE'))

    # Count by property type
    def plot_count_by_property_type(data, title):
        count_by_property_type = data.groupby("property_type")[["_id"]].count().reset_index()
        fig = px.bar(
            count_by_property_type,
            x='property_type',
            y='_id',
            title=title,
            labels={'property_type': 'Property Type', '_id': 'Count of Listings'}
        )
        fig.update_layout(title_x=0.4)
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_count_by_property_type(filtered_data, f'COUNT BY PROPERTY TYPE IN {selected_market.upper()}, {selected_country.upper()}'))
    with col2:
        st.plotly_chart(plot_count_by_property_type(df, 'COUNTRY WIDE COUNT BASED ON PROPERTY TYPE'))

    # Price analysis by bed and room type
    def plot_price_analysis_by_bed_and_room_type(data, title):
        price_analysis = data.groupby(["bed_type", "room_type"])[["price"]].mean().reset_index()
        fig = px.bar(
            price_analysis,
            x="room_type", y="price",
            title=title,
            color="bed_type", barmode="group",
            labels={'room_type': 'Room Type', 'price': 'Average Price'}
        )
        fig.update_layout(title_x=0.3)
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_price_analysis_by_bed_and_room_type(filtered_data, f"PRICE ANALYSIS BY BED AND ROOM TYPE IN {selected_market.upper()}, {selected_country.upper()}"))
    with col2:
        st.plotly_chart(plot_price_analysis_by_bed_and_room_type(df, "COUNTRYWIDE PRICE ANALYSIS BY BED AND ROOM TYPE"))

    # Top 10 hosts by number of reviews
    def plot_top_10_hosts(data, title):
        top_10_reviews = data.sort_values(["number_of_reviews"], ascending=False).head(10)
        fig = px.bar(
            top_10_reviews,
            x="host_name", y="number_of_reviews",
            title=title,
            color="room_type",
            barmode="group",
            labels={'host_name': 'Host Name', 'number_of_reviews': 'Number of Reviews'}
        )
        fig.update_layout(title_x=0.2)
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_top_10_hosts(df, "TOP 10 HOSTS BASED ON NUMBER OF REVIEWS (COUNTRYWIDE)"))
    with col2:
        st.plotly_chart(plot_top_10_hosts(filtered_data, f"TOP 10 HOSTS BASED ON NUMBER OF REVIEWS IN {selected_market.upper()}, {selected_country.upper()}"))

    # Pie charts for bed type and cancellation policy
    def plot_pie_chart(data, column, title):
        count_data = data.groupby([column])[["_id"]].count().reset_index()
        fig = px.pie(
            count_data,
            names=column,
            values='_id',
            title=title,
            labels={column: column.capitalize(), '_id': 'Count'},
            hole=0.5
        )
        fig.update_traces(textinfo='none')
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_pie_chart(df, "bed_type", 'OVERALL COUNT OF BED TYPE'))
    with col2:
        st.plotly_chart(plot_pie_chart(df, "cancellation_policy", 'CANCELLATION TYPE'))

    # Neighborhood analysis
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_country = st.selectbox("Select a country:", country_list, key=1)
    market_list = df["market"][df["country"] == selected_country].unique()
    with col2:
        selected_market = st.selectbox("Select a market:", market_list, key=2)
    neighbourhood_list = sorted(list(df["suburb"][(df["country"] == selected_country) & (df["market"] == selected_market)].unique()))
    with col3:
        selected_neighbourhood = st.selectbox("Select a neighbourhood:", neighbourhood_list)

    filtered_df = df[(df["country"] == selected_country) & (df["market"] == selected_market) & (df["suburb"] == selected_neighbourhood)]

    # Calculate average price for each room type and property type
    avg_price_df = filtered_df.groupby(['property_type', 'room_type'])['price'].mean().reset_index()

    # Create bar chart
    fig_bar = px.bar(
        avg_price_df,
        x="property_type", y="price",
        title="PROPERTY AND ROOM PRICE ANALYSIS BY NEIGHBOURHOOD",
        color="room_type", barmode="group",
        labels={'property_type': 'Property Type', 'price': 'Average Price'}
    )
    fig_bar.update_layout(title_x=0.4)

    st.plotly_chart(fig_bar)
