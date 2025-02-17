import streamlit as st
import matplotlib.colors as mcolors
import plotly.express as px
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from sidebar import create_sidebar_filters

def display_overview():

    # Centered and styled main title using inline styles
    st.markdown('''
        <style>
            .main-title {
                color: #e66c37; /* Title color */
                text-align: center; /* Center align the title */
                font-size: 3rem; /* Title font size */
                font-weight: bold; /* Title font weight */
                margin-bottom: .5rem; /* Space below the title */
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
            }
            div.block-container {
                padding-top: 2rem; /* Padding for main content */
            }
        </style>
    ''', unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">OVERVIEW</h1>', unsafe_allow_html=True)



    filepath_visits = "Claims.xlsx"
    sheet_name1 = "2023 claims"
    sheet_name2 = "2024 claims"

    # Read the Claims data
    dfc_2023 = pd.read_excel(filepath_visits, sheet_name=sheet_name1)
    dfc_2024 = pd.read_excel(filepath_visits, sheet_name=sheet_name2)

    # Read the visit logs
    df = pd.concat([dfc_2023, dfc_2024])


    df['Claim Created Date'] = pd.to_datetime(df['Claim Created Date'], errors='coerce')

    df["Employer Name"] = df["Employer Name"].str.upper()
    df["Provider Name"] = df["Provider Name"].str.upper()

    # Inspect the merged DataFrame

    # Sidebar styling and logo
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .sidebar .sidebar-content h2 {
            color: #007BFF; /* Change this color to your preferred title color */
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-title {
            color: #e66c37;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-header {
            color: #e66c37; /* Change this color to your preferred header color */
            font-size: 2.5em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-multiselect {
            margin-bottom: 15px;
        }
        .sidebar .sidebar-content .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content .logo img {
            max-width: 80%;
            height: auto;
            border-radius: 50%;
        }
                
        </style>
        """, unsafe_allow_html=True)




    # Dictionary to map month names to their order
    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4, 
        "May": 5, "June": 6, "July": 7, "August": 8, 
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    df = df[df['Month'].isin(month_order)]


    # Sort months based on their order
    sorted_months = sorted(df['Month'].dropna().unique(), key=lambda x: pd.to_datetime(x, format='%B').month)

    df['Source'] =df['Source'].astype(str)

    df['Quarter'] = "Q" + df['Claim Created Date'].dt.quarter.astype(str)

    # Create filters (only once per app run)
    if 'filters' not in st.session_state:
        create_sidebar_filters(df)

    # Apply filters
    filters = st.session_state.filters
    if 'Product' in df.columns and filters["product"]:
        df = df[df['Product'].isin(filters["product"])]

    if 'Claim Type' in df.columns and filters["claim_type"]:
        df = df[df['Claim Type'].isin(filters["claim_type"])]

    if 'Claim Status' in df.columns and filters["status"]:
        df = df[df['Claim Status'].isin(filters["status"])]

    if 'Source' in df.columns and filters["source"]:
        df = df[df['Source'].isin(filters["source"])]

    if 'ICD-10 Code' in df.columns and filters["code"]:
        df = df[df['ICD-10 Code'].isin(filters["code"])]

    if 'Employer Name' in df.columns and filters["client_name"]:
        df = df[df['Employer Name'].isin(filters["client_name"])]

    if 'Provider Name' in df.columns and filters["prov_name"]:
        df = df[df['Provider Name'].isin(filters["prov_name"])]

    # Determine the filter description
    filter_description = ""

    # Check if claim_type is defined and not empty
    if 'claim_type' in locals() and claim_type:  # Renamed 'type' to 'claim_type'
        filter_description += f"Claim Types: {', '.join(map(str, claim_type))} | "

    # Check if product is defined and not empty
    if 'product' in locals() and product:
        filter_description += f"Products: {', '.join(map(str, product))} | "

    # If no filters are applied, set a default description
    if not filter_description.strip():
        filter_description = "All data"
    else:
        # Remove the trailing " | " for better formatting
        filter_description = filter_description.rstrip(" | ")


    # Define the mapping of months to quarters
    month_to_quarter = {
        "January": "Q1", "February": "Q1", "March": "Q1",
        "April": "Q2", "May": "Q2", "June": "Q2",
        "July": "Q3", "August": "Q3", "September": "Q3",
        "October": "Q4", "November": "Q4", "December": "Q4"
    }

    # Create a three-column layout
    col1, col2, col3, col4 = st.columns(4)

    # Year selector (allow multiple selections)
    with col1:
        years = sorted(df['Year'].dropna().unique())
        selected_years = st.multiselect(
            "Select Years",
            options=years,
            default=[years[-1]]  # Default to the most recent year
        )
        if selected_years:
            df = df[df['Year'].isin(selected_years)]

    # Month selector (allow multiple selections)
    with col2:
        sorted_months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        selected_months = st.multiselect(
            "Select Months",
            options=sorted_months,
            default=["January"]  # Default to January
        )

        # Dynamically calculate the quarters based on selected months
        if selected_months:
            suggested_quarters = list(set(month_to_quarter[month] for month in selected_months))
        else:
            suggested_quarters = sorted(df['Quarter'].dropna().unique())  # Default to all quarters

    # Quarter selector (allow manual selection, with dynamic suggestions)
    with col3:
        quarters = sorted(df['Quarter'].dropna().unique())
        selected_quarters = st.multiselect(
            "Select Quarters",
            options=quarters,
            default=suggested_quarters  # Pre-select quarters based on selected months
        )
        if selected_quarters:
            df = df[df['Quarter'].isin(selected_quarters)]

    # Business Line selector (pre-select all options by default)
    with col4:
        business_lines = sorted(df['Product'].dropna().unique())
        selected_business_lines = st.multiselect(
            "Select Business Lines",
            options=business_lines,
            default=business_lines  # Pre-select all business lines by default
        )
        if selected_business_lines:
            df = df[df['Product'].isin(selected_business_lines)]



    # Get minimum and maximum dates for the date input
    startDate = df["Claim Created Date"].min()
    endDate = df["Claim Created Date"].max()


    # Define CSS for the styled date input boxes
    st.markdown("""
        <style>
        .date-input-box {
            border-radius: 10px;
            text-align: left;
            margin: 5px;
            font-size: 1.2em;
            font-weight: bold;
        }
        .date-input-title {
            font-size: 1em;
            margin-bottom: 2px;
        }
        .date-range-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #e66c37; /* Orange color for emphasis */
            margin-bottom: 10px;
            text-align: center;
            
        }
        </style>
        """, unsafe_allow_html=True)

    # Add a title for the date range selection
    st.markdown('<div class="date-range-title">Select Claim Date Range</div>', unsafe_allow_html=True)


    # Create 2-column layout for date inputs
    col1, col2 = st.columns(2)


    # Function to display date input in styled boxes
    def display_date_input(col, title, default_date, min_date, max_date):
        col.markdown(f"""
            <div class="date-input-box">
                <div class="date-input-title">{title}</div>
            </div>
            """, unsafe_allow_html=True)
        return col.date_input("", default_date, min_value=min_date, max_value=max_date)


    # Display date inputs
    with col1:
        date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate))

    with col2:
        date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate))



    # Filter data by product type and claim status
    df_health = df[df['Product'] == 'Health Insurance']
    df_proactiv = df[df['Product'] == 'ProActiv']
    df_app = df[df['Claim Status'] == 'Approved']
    df_dec = df[df['Claim Status'] == 'Declined']

    if not df.empty:
        scale = 1_000_000  # For millions
        scaling = 1000  # For thousands

        # Calculate key metrics
        total_claim_amount = (df["Claim Amount"].sum()) / scale
        average_amount = (df["Claim Amount"].mean()) / scaling
        average_app_amount = (df["Approved Claim Amount"].mean()) / scaling

        total_app_claim_amount = (df_app["Approved Claim Amount"].sum()) / scale
        total_dec_claim_amount = (df_dec["Claim Amount"].sum()) / scaling

        total_app = df_app["Claim ID"].nunique()
        total_dec = df_dec["Claim ID"].nunique()

        total_health_claim_amount = (df_health["Claim Amount"].sum()) / scale
        total_pro_claim_amount = (df_proactiv["Claim Amount"].sum()) / scale

        total_health = df_health["Claim ID"].nunique()
        total_proactiv = df_proactiv["Claim ID"].nunique()

        total_clients = df["Employer Name"].nunique()
        total_claims = df["Claim ID"].nunique()

        # Approval and Denial Rates
        total_app_per = (total_app / total_claims) * 100 if total_claims > 0 else 0
        total_dec_per = (total_dec / total_claims) * 100 if total_claims > 0 else 0

        # Approval Rate (Claims Approved / Total Claims)
        approval_rate = (total_app / total_claims) * 100 if total_claims > 0 else 0

        # Denial Rate (Claims Declined / Total Claims)
        denial_rate = (total_dec / total_claims) * 100 if total_claims > 0 else 0

        percent_app = (total_app_claim_amount / total_claim_amount) * 100 if total_claim_amount > 0 else 0

        # Define CSS for styled boxes and tooltips
        st.markdown("""
            <style>
            .custom-subheader {
                color: #e66c37;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 5px;
                display: inline-block;
            }
            .metric-box {
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                margin: 10px;
                font-size: 1.2em;
                font-weight: bold;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                border: 1px solid #ddd;
                position: relative;
            }
            .metric-title {
                color: #e66c37; /* Change this color to your preferred title color */
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .metric-value {
                color: #009DAE;
                font-size: 1em;
            }
            </style>
            """, unsafe_allow_html=True)

        # Function to display metrics in styled boxes with tooltips
        def display_metric(col, title, value):
            col.markdown(f"""
                <div class="metric-box">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # Display client and claim metrics
        st.markdown('<h2 class="custom-subheader">For Health Insurance or ProActiv Claims in Numbers</h2>', unsafe_allow_html=True)
        cols1, cols2, cols3 = st.columns(3)
        display_metric(cols1, "Number of Clients", total_clients)
        display_metric(cols2, "Number of Claims", f"{total_claims:,}")
        display_metric(cols3, "Number of Approved Claims", f"{total_app:,}")
        display_metric(cols1, "Number of Declined Claims", total_dec)
        display_metric(cols2, "Approval Rate", f"{approval_rate:.2f} %")
        display_metric(cols3, "Denial Rate", f"{denial_rate:.2f} %")

        # Display claim amount metrics
        st.markdown('<h2 class="custom-subheader">For Health Insurance or ProActiv Claim Amounts </h2>', unsafe_allow_html=True)
        cols1, cols2, cols3 = st.columns(3)
        display_metric(cols1, "Total Claims", total_claims)
        display_metric(cols2, "Total Claim Amount", f"{total_claim_amount:,.0f} M")
        display_metric(cols3, "Total Approved Claim Amount", f"{total_app_claim_amount:,.0f} M")
        display_metric(cols1, "Total Declined Claim Amount", f"{total_dec_claim_amount:,.0f} K")
        display_metric(cols2, "Average Claim Amount", f"{average_amount:,.1f} K")
        display_metric(cols3, "Average Approved Claim Amount", f"{average_app_amount:,.1f} K")