import streamlit as st

def create_sidebar_filters(df):
    if 'filters' not in st.session_state:
        st.session_state.filters = {}

    # Product filter
    st.session_state.filters["product"] = st.sidebar.multiselect(
        "Select Product",
        options=df['Product'].unique(),
        key="sidebar_product_multiselect"
    )

    # Claim Type filter
    st.session_state.filters["claim_type"] = st.sidebar.multiselect(
        "Select Claim Type",
        options=sorted(df['Claim Type'].unique()),
        key="sidebar_claim_type_multiselect"
    )

    # Claim Status filter
    st.session_state.filters["status"] = st.sidebar.multiselect(
        "Select Claim Status",
        options=df['Claim Status'].unique(),
        key="sidebar_claim_status_multiselect"
    )

    # Source filter
    st.session_state.filters["source"] = st.sidebar.multiselect(
        "Select Claim Provider Type",
        options=sorted(df['Source'].unique()),
        key="sidebar_source_multiselect"
    )

    # Diagnosis Code filter
    st.session_state.filters["code"] = st.sidebar.multiselect(
        "Select Diagnosis Code",
        options=df['ICD-10 Code'].unique(),
        key="sidebar_diagnosis_code_multiselect"
    )

    # Employer Name filter
    st.session_state.filters["client_name"] = st.sidebar.multiselect(
        "Select Employer Name",
        options=sorted(df['Employer Name'].dropna().unique()),
        key="sidebar_employer_name_multiselect"
    )

    # Provider Name filter
    st.session_state.filters["prov_name"] = st.sidebar.multiselect(
        "Select Provider Name",
        options=sorted(df['Provider Name'].dropna().unique()),
        key="sidebar_provider_name_multiselect"
    )

    return st.session_state.filters