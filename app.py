# start project with "streamlit run app.py"
import pandas as pd
import plotly.express as px
import streamlit as st

# Browser Tab Header
st.set_page_config (
  page_title="Sales Dashboard",
  page_icon=":bar_chart:",
  layout="wide"
)

# Create dataframe
@st.cache
def get_data_from_excel():
    df_sales = pd.read_excel(
        io="supermarket_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df_sales["hour"] = pd.to_datetime(df_sales["Time"], format="%H:%M:%S").dt.hour
    return df_sales

df_sales = get_data_from_excel()

# Sidebar
st.sidebar.header("Please Filter Here:")

city = st.sidebar.multiselect(
    "Select a City:",
    options=df_sales["City"].unique(),
    default=df_sales["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select a Customer Membership Type:",
    options=df_sales["Customer_type"].unique(),
    default=df_sales["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Filter Customer by Gender:",
    options=df_sales["Gender"].unique(),
    default=df_sales["Gender"].unique()
)

df_with_filters = df_sales.query("City == @city & Customer_type == @customer_type & Gender == @gender")

st.dataframe(df_with_filters)

# Mainpage
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# Top KPIs
total_sales = int(df_with_filters["Total"].sum())
average_rating = round(df_with_filters["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_with_filters["Total"].mean(), 2)

left, middle, right = st.columns(3)

with left:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# Sales by Product Line
sales_by_product_line = (
  df_with_filters.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

product_sales_figure = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

product_sales_figure.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

product_sales_figure.update_xaxes(range=[45000, 50000])

# Sales by Hour
sales_by_hour = df_with_filters.groupby(by=["hour"]).sum()[["Total"]]
hourly_sales_figure = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

hourly_sales_figure.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

hourly_sales_figure.update_yaxes(range=[20000,40000])

left, right = st.columns(2)
left.plotly_chart(hourly_sales_figure, use_container_width=True)
right.plotly_chart(product_sales_figure, use_container_width=True)


# Hide Streamlit Style
hide_st_style = """
  <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
  </style>
   """
st.markdown(hide_st_style, unsafe_allow_html=True)
