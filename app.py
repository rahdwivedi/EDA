
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Vehicle Category Analysis", layout="wide")

# Hardcoded user credentials
USER_CREDENTIALS = {
    "admin": "admin123",
    "analyst": "veh2024"
}

# Login page function
def login_page():
    st.title("🔐 Login to Vehicle Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            # Streamlit will automatically rerun after the session state is updated
        else:
            st.error("❌ Invalid username or password")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('vehicle_maintenance_data.csv')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False

# Filter 1: Analysis Category
selected_filter = st.sidebar.selectbox(
    "Select Analysis Category:",
    ["All", "Vehicle Category Analysis", "Maintenance and Condition Analysis","Fuel and Engine Performance Analysis",
     "Reported Issue and Risk Analysis","Descriptive Analysis","Diagnostic Analysis"]
)

# Filter 2: Value Type
value_type = st.sidebar.radio(
    "Display Value As:",
    ["Show as Count", "Show as Percentage"]
)

# =============================== #
# 📊 Vehicle Category Analysis
# =============================== #
def vehicle_eda_page():
    st.title("Vehicle Maintenance - Exploratory Data Analysis")
    
    # --- Vehicle Category Analysis ---
    if selected_filter == "All" or selected_filter == "Vehicle Category Analysis":
        # --- KPIs Section ---
        st.header("📊 Key Performance Indicators")
    
        # KPIs based on Vehicle Model
        total_models = df['Vehicle_Model'].nunique()
        total_vehicles = df['Vehicle_Model'].count()
        most_common_model = df['Vehicle_Model'].mode()[0] if not df['Vehicle_Model'].isnull().all() else "N/A"
        avg_mileage = round(df['Mileage'].mean(), 2) if 'Mileage' in df.columns else "N/A"
        avg_issues = round(df['Reported_Issues'].mean(), 2) if 'Reported_Issues' in df.columns else "N/A"
    
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Vehicle Models", total_models)
        with col2:
            st.metric("Total Vehicles", total_vehicles)
        with col3:
            st.metric("Most Common Model", most_common_model)
        with col4:
            st.metric("Average Mileage", avg_mileage)
        with col5:
            st.metric("Average Reported Issues", avg_issues)
    
    # --- Vehicle Category Analysis ---
    if selected_filter == "All" or selected_filter == "Vehicle Category Analysis":
        st.header("🚙 Vehicle Category Analysis")
    
        # Row 1: Owner Type and Fuel Type
        col1, col2 = st.columns(2)
    
        with col1:
            st.subheader("Owner Type Distribution")
            owner_counts = df['Owner_Type'].value_counts().reset_index()
            owner_counts.columns = ['Owner_Type', 'Count']
    
            if value_type == "Show as Percentage":
                owner_counts['Percentage'] = round((owner_counts['Count'] / owner_counts['Count'].sum()) * 100, 2)
                fig_owner = px.pie(
                    owner_counts,
                    names='Owner_Type',
                    values='Percentage',
                    title='Owner Type (Percentage)',
                    hole=0.4
                )
            else:
                fig_owner = px.bar(
                    owner_counts,
                    x='Owner_Type',
                    y='Count',
                    color='Owner_Type',
                    title='Owner Type (Count)',
                    text='Count'
                )
            st.plotly_chart(fig_owner, use_container_width=True)
    
        with col2:
            st.subheader("Fuel Type Distribution")
            fuel_counts = df['Fuel_Type'].value_counts().reset_index()
            fuel_counts.columns = ['Fuel_Type', 'Count']
    
            if value_type == "Show as Percentage":
                fuel_counts['Percentage'] = round((fuel_counts['Count'] / fuel_counts['Count'].sum()) * 100, 2)
                fig_fuel = px.pie(
                    fuel_counts,
                    names='Fuel_Type',
                    values='Percentage',
                    title='Fuel Type (Percentage)',
                    hole=0.4
                )
            else:
                fig_fuel = px.bar(
                    fuel_counts,
                    x='Fuel_Type',
                    y='Count',
                    color='Fuel_Type',
                    title='Fuel Type (Count)',
                    text='Count'
                )
            st.plotly_chart(fig_fuel, use_container_width=True)
    
        # Row 2: Transmission Type and Top 10 Vehicle Models
        col3, col4 = st.columns(2)
    
        with col3:
            st.subheader("Transmission Type Distribution")
            transmission_counts = df['Transmission_Type'].value_counts().reset_index()
            transmission_counts.columns = ['Transmission_Type', 'Count']
    
            if value_type == "Show as Percentage":
                transmission_counts['Percentage'] = round((transmission_counts['Count'] / transmission_counts['Count'].sum()) * 100, 2)
                fig_transmission = px.pie(
                    transmission_counts,
                    names='Transmission_Type',
                    values='Percentage',
                    title='Transmission Type (Percentage)',
                    hole=0.4
                )
            else:
                fig_transmission = px.bar(
                    transmission_counts,
                    x='Transmission_Type',
                    y='Count',
                    color='Transmission_Type',
                    title='Transmission Type (Count)',
                    text='Count'
                )
            st.plotly_chart(fig_transmission, use_container_width=True)
    
        with col4:
            st.subheader("Vehicle Models by Count")
            model_counts = df['Vehicle_Model'].value_counts().head(10).reset_index()
            model_counts.columns = ['Vehicle_Model', 'Count']
    
            if value_type == "Show as Percentage":
                model_counts['Percentage'] = round((model_counts['Count'] / model_counts['Count'].sum()) * 100, 2)
                fig_model = px.pie(
                    model_counts,
                    names='Vehicle_Model',
                    values='Percentage',
                    title='Vehicle Models (Percentage)',
                    hole=0.4
                )
            else:
                fig_model = px.bar(
                    model_counts,
                    x='Vehicle_Model',
                    y='Count',
                    color='Vehicle_Model',
                    title='Vehicle Models (Count)',
                    text='Count'
                )
            st.plotly_chart(fig_model, use_container_width=True)
    
    # =============================== #
    # Maintenance and Condition Analysis
    # =============================== #
    
    # --- Maintenance and Condition Analysis ---
    if selected_filter == "All" or selected_filter == "Maintenance and Condition Analysis":
        st.header("📊 Key Performance Indicators")
    
        percent_needing_maintenance = round((df['Need_Maintenance'].sum() / len(df)) * 100, 2)
        bad_tire_condition = round((df[df['Tire_Condition'] == 'Worn Out'].shape[0] / len(df)) * 100, 2)
        poor_brake_condition = round((df[df['Brake_Condition'] == 'Worn Out'].shape[0] / len(df)) * 100, 2)
        weak_battery = round((df[df['Battery_Status'] == 'Weak'].shape[0] / len(df)) * 100, 2)
        avg_accident_history = round(df['Accident_History'].mean(), 2)
    
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("% Needing Maintenance", f"{percent_needing_maintenance}%")
        col2.metric("Bad Tire Condition (%)", f"{bad_tire_condition}%")
        col3.metric("Poor Brake Condition (%)", f"{poor_brake_condition}%")
        col4.metric("Weak Battery (%)", f"{weak_battery}%")
        col5.metric("Avg Accident History", avg_accident_history)
    
    if selected_filter == "All" or selected_filter == "Maintenance and Condition Analysis":
        st.header("🔧 Maintenance and Condition Analysis")
    
        # Row 1
        col1, col2 = st.columns(2)
    
        with col1:
            st.subheader("Maintenance History by Fuel Type")
            fuel_data = df['Fuel_Type'].value_counts().reset_index()
            fuel_data.columns = ['Fuel_Type', 'Count']
    
            if value_type == "Show as Count":
                fig = px.bar(
                    fuel_data,
                    x='Fuel_Type',
                    y='Count',
                    color='Fuel_Type',
                    text='Count',
                    title='Maintenance History by Fuel Type (Count)'
                )
            else:
                fig = px.pie(
                    fuel_data,
                    names='Fuel_Type',
                    values='Count',
                    title='Maintenance History by Fuel Type (Percentage)',
                    hole=0.4
                )
            st.plotly_chart(fig, use_container_width=True)
    
        with col2:
            st.subheader("Need Maintenance (Yes/No)")
            maintenance_data = df['Need_Maintenance'].value_counts().reset_index()
            maintenance_data.columns = ['Need_Maintenance', 'Count']
    
            if value_type == "Show as Count":
                fig = px.bar(
                    maintenance_data,
                    x='Need_Maintenance',
                    y='Count',
                    color='Need_Maintenance',
                    text='Count',
                    title='Vehicles Needing Maintenance (Count)'
                )
            else:
                fig = px.pie(
                    maintenance_data,
                    names='Need_Maintenance',
                    values='Count',
                    title='Vehicles Needing Maintenance (Percentage)',
                    hole=0.4
                )
            st.plotly_chart(fig, use_container_width=True)
    
        # Row 2
        col3, col4, col5 = st.columns(3)
    
        with col3:
            st.subheader("Tire Condition")
            tire_data = df['Tire_Condition'].value_counts().reset_index()
            tire_data.columns = ['Tire_Condition', 'Count']
    
            if value_type == "Show as Count":
                fig = px.bar(
                    tire_data,
                    x='Tire_Condition',
                    y='Count',
                    color='Tire_Condition',
                    text='Count',
                    title='Tire Condition (Count)'
                )
            else:
                fig = px.pie(
                    tire_data,
                    names='Tire_Condition',
                    values='Count',
                    title='Tire Condition (Percentage)',
                    hole=0.4
                )
            st.plotly_chart(fig, use_container_width=True)
    
        with col4:
            st.subheader("Brake Condition")
            brake_data = df['Brake_Condition'].value_counts().reset_index()
            brake_data.columns = ['Brake_Condition', 'Count']
    
            if value_type == "Show as Count":
                fig = px.bar(
                    brake_data,
                    x='Brake_Condition',
                    y='Count',
                    color='Brake_Condition',
                    text='Count',
                    title='Brake Condition (Count)'
                )
            else:
                fig = px.pie(
                    brake_data,
                    names='Brake_Condition',
                    values='Count',
                    title='Brake Condition (Percentage)',
                    hole=0.4
                )
            st.plotly_chart(fig, use_container_width=True)
    
        with col5:
            st.subheader("Battery Status")
            battery_data = df['Battery_Status'].value_counts().reset_index()
            battery_data.columns = ['Battery_Status', 'Count']
    
            if value_type == "Show as Count":
                fig = px.bar(
                    battery_data,
                    x='Battery_Status',
                    y='Count',
                    color='Battery_Status',
                    text='Count',
                    title='Battery Status (Count)'
                )
            else:
                fig = px.pie(
                    battery_data,
                    names='Battery_Status',
                    values='Count',
                    title='Battery Status (Percentage)',
                    hole=0.4
                )
            st.plotly_chart(fig, use_container_width=True)
    
    # =============================== #
    # Fuel and Engine Performance Analysis
    # =============================== #
    
    if selected_filter == "All" or selected_filter == "Fuel and Engine Performance Analysis":
        st.header("📊 Key Performance Indicators")
    
        # --- KPIs ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            high_engine = round((df[df['Engine_Size'] > df['Engine_Size'].mean()].shape[0] / df.shape[0]) * 100, 2)
            st.metric("% High Engine Size", f"{high_engine}")
        with col2:
            low_engine = round((df[df['Engine_Size'] < df['Engine_Size'].mean()].shape[0] / df.shape[0]) * 100, 2)
            st.metric("% Low Engine Size", f"{low_engine}")
        with col3:
            odometer_std = round(df['Odometer_Reading'].std(), 2)
            st.metric("STDEV of Odometer", f"{odometer_std/1000:.2f}K")
        with col4:
            fuel_eff_std = round(df['Fuel_Efficiency'].std(), 2)
            st.metric("STDEV of Fuel Efficiency", fuel_eff_std)
    
    
        st.header("⛽ Fuel and Engine Performance Analysis")
    
        # -------------------- #
        # Row 1: Tire & Combo
        # -------------------- #
        col1, col2 = st.columns(2)
    
        # --- Tire Condition Analysis ---
        with col1:
            st.subheader("Fuel Efficiency by Tire Condition")
            tire_df = df.groupby('Tire_Condition')['Fuel_Efficiency'].mean().reset_index()
            tire_df['Fuel_Efficiency'] = tire_df['Fuel_Efficiency'].round(3)
    
            if value_type == "Show as Percentage":
                total = tire_df['Fuel_Efficiency'].sum()
                tire_df['Percentage'] = (tire_df['Fuel_Efficiency'] / total) * 100
                tire_df['Percentage'] = tire_df['Percentage'].round(3)
                fig_tire = px.pie(
                    tire_df,
                    names='Tire_Condition',
                    values='Percentage',
                    hole=0.4,
                    title='Fuel Efficiency by Tire Condition (%)'
                )
                fig_tire.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.3%}')
            else:
                fig_tire = px.bar(
                    tire_df,
                    x='Tire_Condition',
                    y='Fuel_Efficiency',
                    color='Tire_Condition',
                    text='Fuel_Efficiency',
                    title='Fuel Efficiency by Tire Condition (Count)'
                )
                fig_tire.update_traces(textangle=0)
    
            st.plotly_chart(fig_tire, use_container_width=True)
    
        # --- Fuel vs Transmission Analysis ---
        with col2:
            st.subheader("Fuel Type vs Transmission Type")
            combo_df = df.groupby(['Fuel_Type', 'Transmission_Type'])['Fuel_Efficiency'].mean().reset_index()
            combo_df['Fuel_Efficiency'] = combo_df['Fuel_Efficiency'].round(3)
    
            if value_type == "Show as Percentage":
                total = combo_df['Fuel_Efficiency'].sum()
                combo_df['Percentage'] = (combo_df['Fuel_Efficiency'] / total) * 100
                combo_df['Percentage'] = combo_df['Percentage'].round(3)
                combo_df['Label'] = combo_df['Fuel_Type'] + " - " + combo_df['Transmission_Type']
    
                fig_combo = px.pie(
                    combo_df,
                    names='Label',
                    values='Percentage',
                    hole=0.4,
                    title='Fuel vs Transmission Type (%)'
                )
                fig_combo.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.3%}')
            else:
                fig_combo = px.bar(
                    combo_df,
                    x='Fuel_Type',
                    y='Fuel_Efficiency',
                    color='Transmission_Type',
                    barmode='group',
                    text='Fuel_Efficiency',
                    title='Fuel Type vs Transmission Type (Count)'
                )
                fig_combo.update_traces(textangle=0)
    
            st.plotly_chart(fig_combo, use_container_width=True)
    
        # ------------------------------- #
        # Row 2: Engine Size & Insurance
        # ------------------------------- #
        col3, col4 = st.columns(2)
    
        # --- Engine Size Analysis ---
        with col3:
            st.subheader("Fuel Efficiency by Engine Size")
            engine_df = df.groupby('Engine_Size')['Fuel_Efficiency'].mean().reset_index()
            engine_df['Fuel_Efficiency'] = engine_df['Fuel_Efficiency'].round(3)
    
            if value_type == "Show as Percentage":
                total = engine_df['Fuel_Efficiency'].sum()
                engine_df['Percentage'] = (engine_df['Fuel_Efficiency'] / total) * 100
                engine_df['Percentage'] = engine_df['Percentage'].round(3)
    
                fig_engine = px.pie(
                    engine_df,
                    names='Engine_Size',
                    values='Percentage',
                    hole=0.4,
                    title='Fuel Efficiency by Engine Size (%)'
                )
                fig_engine.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.3%}')
            else:
                fig_engine = px.bar(
                    engine_df,
                    x='Engine_Size',
                    y='Fuel_Efficiency',
                    color='Engine_Size',
                    text='Fuel_Efficiency',
                    title='Fuel Efficiency by Engine Size (Count)'
                )
                fig_engine.update_traces(textangle=0)
    
            st.plotly_chart(fig_engine, use_container_width=True)
    
        # --- Insurance Premium Analysis ---
        with col4:
            st.subheader("Average Insurance Premium by Fuel Type")
            insurance_df = df.groupby('Fuel_Type')['Insurance_Premium'].mean().reset_index()
            insurance_df['Insurance_Premium'] = insurance_df['Insurance_Premium'].round(3)
    
            if value_type == "Show as Percentage":
                total = insurance_df['Insurance_Premium'].sum()
                insurance_df['Percentage'] = (insurance_df['Insurance_Premium'] / total) * 100
                insurance_df['Percentage'] = insurance_df['Percentage'].round(3)
    
                fig_insurance = px.pie(
                    insurance_df,
                    names='Fuel_Type',
                    values='Percentage',
                    hole=0.4,
                    title='Insurance Premium by Fuel Type (%)'
                )
                fig_insurance.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.3%}')
            else:
                fig_insurance = px.bar(
                    insurance_df,
                    x='Fuel_Type',
                    y='Insurance_Premium',
                    color='Fuel_Type',
                    text='Insurance_Premium',
                    title='Insurance Premium by Fuel Type (Count)'
                )
                fig_insurance.update_traces(textangle=0)
    
            st.plotly_chart(fig_insurance, use_container_width=True)
    
    
    # =============================== #
    # Reported Issue and Risk Analysis
    # =============================== #
    
    if selected_filter == "All" or selected_filter == "Reported Issue and Risk Analysis":
        st.header("📊 Key Performance Indicators")
    
        # --- KPIs from Image & Additional ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            percent_reported_issues = round((df[df['Reported_Issues'] > 0].shape[0] / df.shape[0]), 2)
            st.metric("% Vehicles with Reported Issues", f"{percent_reported_issues * 100:.2f}%")
        with col2:
            percent_accident = round((df[df['Accident_History'] > 0].shape[0] / df.shape[0]), 2)
            st.metric("% Vehicles with Accident History", f"{percent_accident * 100:.2f}%")
        with col3:
            percent_both = round((df[(df['Reported_Issues'] > 0) & (df['Accident_History'] > 0)].shape[0] / df.shape[0]), 2)
            st.metric("% Vehicles with Both Issues & Accidents", f"{percent_both * 100:.2f}%")
        with col4:
            std_fuel_eff = round(df['Fuel_Efficiency'].std(), 2)
            st.metric("STDEV of Fuel Efficiency", std_fuel_eff)
    
        # -------------------------- #
        st.header("⚠️ Reported Issue and Risk Analysis")
        col1, col2 = st.columns(2)
    
        # -------------------------- #
        with col1:
            st.subheader("Average Insurance Premium by Reported Issue Count")
            premium_df = df.groupby('Reported_Issues')['Insurance_Premium'].mean().reset_index()
            premium_df['Insurance_Premium'] = premium_df['Insurance_Premium'].round(3)
    
            if value_type == "Show as Percentage":
                total = premium_df['Insurance_Premium'].sum()
                premium_df['Percentage'] = (premium_df['Insurance_Premium'] / total) * 100
                premium_df['Percentage'] = premium_df['Percentage'].round(3)
                fig_premium = px.pie(
                    premium_df,
                    names='Reported_Issues',
                    values='Percentage',
                    hole=0.4,
                    title='Avg Insurance Premium by Issue Count (%)'
                )
                fig_premium.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.2f}%')
            else:
                fig_premium = px.bar(
                    premium_df,
                    x='Reported_Issues',
                    y='Insurance_Premium',
                    text='Insurance_Premium',
                    title='Avg Insurance Premium by Issue Count'
                )
                fig_premium.update_traces(textangle=0)
    
            st.plotly_chart(fig_premium, use_container_width=True)
    
        # -------------------------- #
        with col2:
            st.subheader("Reported Issue Count by Vehicle Model")
            model_df = df.groupby('Vehicle_Model')['Reported_Issues'].sum().reset_index()
            model_df['Reported_Issues'] = model_df['Reported_Issues'].round(3)
    
            if value_type == "Show as Percentage":
                total = model_df['Reported_Issues'].sum()
                model_df['Percentage'] = (model_df['Reported_Issues'] / total) * 100
                model_df['Percentage'] = model_df['Percentage'].round(3)
                fig_model = px.pie(
                    model_df,
                    names='Vehicle_Model',
                    values='Percentage',
                    hole=0.4,
                    title='Reported Issues by Vehicle Model (%)'
                )
                fig_model.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.2f}%')
            else:
                fig_model = px.bar(
                    model_df,
                    x='Vehicle_Model',
                    y='Reported_Issues',
                    text='Reported_Issues',
                    title='Reported Issues by Vehicle Model'
                )
                fig_model.update_traces(textangle=0)
    
            st.plotly_chart(fig_model, use_container_width=True)
    
        # -------------------------- #
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Accident History vs Vehicle Age")
            age_df = df.groupby('Vehicle_Age')['Accident_History'].mean().reset_index()
            age_df['Accident_History'] = age_df['Accident_History'].round(3)
        
            if value_type == "Show as Percentage":
                total = age_df['Accident_History'].sum()
                age_df['Percentage'] = (age_df['Accident_History'] / total) * 100
                age_df['Percentage'] = age_df['Percentage'].round(3)
        
                fig_age = px.pie(
                    age_df,
                    names='Vehicle_Age',
                    values='Percentage',
                    hole=0.4,
                    title='Average Accident History by Vehicle Age (%)'
                )
                fig_age.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.2f}%')
            else:
                fig_age = px.bar(
                    age_df,
                    x='Vehicle_Age',
                    y='Accident_History',
                    text='Accident_History',
                    title='Average Accident History by Vehicle Age'
                )
                fig_age.update_traces(textangle=0)
        
            st.plotly_chart(fig_age, use_container_width=True)
    
        # -------------------------- #
        with col4:
            st.subheader("Engine Size Distribution")
            engine_df = df['Engine_Size'].value_counts().reset_index()
            engine_df.columns = ['Engine_Size', 'Count']
            engine_df['Count'] = engine_df['Count'].round(3)
    
            if value_type == "Show as Percentage":
                total = engine_df['Count'].sum()
                engine_df['Percentage'] = (engine_df['Count'] / total) * 100
                engine_df['Percentage'] = engine_df['Percentage'].round(3)
                fig_engine = px.pie(
                    engine_df,
                    names='Engine_Size',
                    values='Percentage',
                    hole=0.4,
                    title='Engine Size Distribution (%)'
                )
                fig_engine.update_traces(textinfo='label+percent', hovertemplate='%{label}: %{percent:.2f}%')
            else:
                fig_engine = px.bar(
                    engine_df,
                    x='Engine_Size',
                    y='Count',
                    text='Count',
                    title='Engine Size Distribution'
                )
                fig_engine.update_traces(textangle=0)
    
            st.plotly_chart(fig_engine, use_container_width=True)
    
    
    
    # =============================== #
    # Descriptive Analysis
    # =============================== #
    
    # --- KPIs Filter and Section ---
    if selected_filter == "All" or selected_filter == "Descriptive Analysis":
        st.header("📊 Key Performance Indicators")
    
        # Calculate the KPIs
        total_vehicles = df['Vehicle_Model'].nunique()
        avg_fuel_efficiency = round(df['Fuel_Efficiency'].mean(), 3)
        avg_accident_history = round(df['Accident_History'].mean(), 3)
        avg_mileage = round(df['Mileage'].mean(), 3)
        avg_reported_issues = round(df['Reported_Issues'].mean(), 3)
    
        # Display the KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Vehicles", total_vehicles)
        with col2:
            st.metric("Average Fuel Efficiency", avg_fuel_efficiency)
        with col3:
            st.metric("Average Accident History", avg_accident_history)
        with col4:
            st.metric("Average Mileage", avg_mileage)
        with col5:
            st.metric("Average Reported Issues", avg_reported_issues)
    
    # --- Descriptive Analysis Section ---
    if selected_filter == "All" or selected_filter == "Descriptive Analysis":
        st.header("📊 Descriptive Analysis")
    
        import plotly.graph_objects as go
    
        # --- Mileage Consumption by Vehicle Model and Owner Type ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Mileage Consumption by Vehicle Model and Owner Type")
            df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
            mileage_summary = df.groupby(['Vehicle_Model', 'Owner_Type'])['Mileage'].mean().reset_index()
            mileage_summary = mileage_summary.sort_values(by='Mileage', ascending=False)
    
            if value_type == "Show as Count":
                mileage_summary['Mileage'] = mileage_summary['Mileage'].round(3)
                fig_mileage = px.bar(
                    mileage_summary,
                    x='Vehicle_Model',
                    y='Mileage',
                    color='Owner_Type',
                    title='Avg Mileage by Vehicle Model & Owner Type (Count)',
                    labels={'Mileage': 'Avg Mileage (km)', 'Vehicle_Model': 'Vehicle Model'},
                    hover_data=['Mileage']
                )
            else:
                mileage_summary['Mileage_Percentage'] = (mileage_summary['Mileage'] / mileage_summary['Mileage'].max()) * 100
                fig_mileage = px.pie(
                    mileage_summary,
                    names='Vehicle_Model',
                    values='Mileage_Percentage',
                    title='Mileage by Vehicle Model (Percentage)',
                    hole=0.4
                )
            for data in fig_mileage.data:
                if isinstance(data, go.Bar):
                    data.update(text=data.y, textposition='outside')
            st.plotly_chart(fig_mileage, use_container_width=True)
    
        with col2:
            st.subheader("Maintenance Frequency by Vehicle Model")
            maintenance_freq = df.groupby('Vehicle_Model').size().reset_index(name='Maintenance_Count')
            maintenance_freq = maintenance_freq.sort_values(by='Maintenance_Count', ascending=False)
    
            if value_type == "Show as Count":
                maintenance_freq['Maintenance_Count'] = maintenance_freq['Maintenance_Count'].round(3)
                fig_maintenance = px.bar(
                    maintenance_freq.head(10),
                    x='Vehicle_Model',
                    y='Maintenance_Count',
                    title='Vehicle Models by Maintenance Count',
                    labels={'Maintenance_Count': 'Maintenance Count', 'Vehicle_Model': 'Vehicle Model'},
                    hover_data=['Maintenance_Count'],
                    color='Vehicle_Model'
                )
            else:
                maintenance_freq['Maintenance_Percentage'] = round((maintenance_freq['Maintenance_Count'] / maintenance_freq['Maintenance_Count'].sum()) * 100, 3)
                fig_maintenance = px.pie(
                    maintenance_freq.head(10),
                    names='Vehicle_Model',
                    values='Maintenance_Percentage',
                    title='Vehicle Models by Maintenance (%)',
                    hole=0.4
                )
            for data in fig_maintenance.data:
                if isinstance(data, go.Bar):
                    data.update(text=data.y, textposition='outside')
            st.plotly_chart(fig_maintenance, use_container_width=True)
    
        # --- Accident-Prone & Age vs Maintenance Charts Side-by-Side ---
        col3, col4 = st.columns(2)
    
        with col3:
            st.subheader("Accident-Prone Vehicle Identification")
            accident_prone = df.groupby('Vehicle_Model')['Accident_History'].mean().sort_values(ascending=False).reset_index()
    
            if value_type == "Show as Percentage":
                accident_prone['Accident_Percentage'] = round((accident_prone['Accident_History'] / accident_prone['Accident_History'].max()) * 100, 3)
                fig_accident = px.pie(
                    accident_prone.head(10),
                    names='Vehicle_Model',
                    values='Accident_Percentage',
                    title='Vehcile Models by Accident History (%)',
                    hole=0.4
                )
            else:
                accident_prone['Accident_History'] = accident_prone['Accident_History'].round(3)
                fig_accident = px.bar(
                    accident_prone.head(10),
                    x='Vehicle_Model',
                    y='Accident_History',
                    title='Vehicle Models by Avg Accident History (Count)',
                    color='Vehicle_Model'
                )
            for data in fig_accident.data:
                if isinstance(data, go.Bar):
                    data.update(text=data.y, textposition='outside')
            st.plotly_chart(fig_accident, use_container_width=True)
    
        with col4:
            st.subheader("Vehicle Age vs Maintenance Count")
            age_vs_maintenance = df.groupby('Vehicle_Age').size().reset_index(name='Maintenance_Count').sort_values('Vehicle_Age')
    
            if value_type == "Show as Percentage":
                age_vs_maintenance['Maintenance_Percentage'] = round((age_vs_maintenance['Maintenance_Count'] / age_vs_maintenance['Maintenance_Count'].max()) * 100, 3)
                fig_age = px.pie(
                    age_vs_maintenance,
                    names='Vehicle_Age',
                    values='Maintenance_Percentage',
                    title='Maintenance by Age (Percentage)',
                    hole=0.4
                )
            else:
                age_vs_maintenance['Maintenance_Count'] = age_vs_maintenance['Maintenance_Count'].round(3)
                fig_age = px.bar(
                    age_vs_maintenance,
                    x='Vehicle_Age',
                    y='Maintenance_Count',
                    title='Maintenance Count by Age (Count)',
                    color='Vehicle_Age'
                )
            for data in fig_age.data:
                if isinstance(data, go.Bar):
                    data.update(text=data.y, textposition='outside')
            st.plotly_chart(fig_age, use_container_width=True)
    
        # --- Issue Pattern Detection ---
        st.subheader("Issue Pattern Detection by Vehicle Model")
        issue_pattern = df.groupby(['Vehicle_Model', 'Reported_Issues']).size().reset_index(name='Issue_Count')
        top_models = issue_pattern.groupby('Vehicle_Model')['Issue_Count'].sum().sort_values(ascending=False).head(10).index
        filtered_issue_pattern = issue_pattern[issue_pattern['Vehicle_Model'].isin(top_models)]
    
        if value_type == "Show as Count":
            filtered_issue_pattern['Issue_Count'] = filtered_issue_pattern['Issue_Count'].round(3)
            fig_issue = px.bar(
                filtered_issue_pattern,
                x='Vehicle_Model',
                y='Issue_Count',
                color='Reported_Issues',
                title="Issue Pattern by Vehicle Model (Count)",
                labels={'Issue_Count': 'Issue Count', 'Vehicle_Model': 'Vehicle Model'},
                hover_data=['Issue_Count']
            )
        else:
            filtered_issue_pattern['Issue_Percentage'] = round((filtered_issue_pattern['Issue_Count'] / filtered_issue_pattern['Issue_Count'].sum()) * 100, 3)
            fig_issue = px.pie(
                filtered_issue_pattern,
                names='Vehicle_Model',
                values='Issue_Percentage',
                title="Issue Pattern by Vehicle Model (Percentage)",
                hole=0.4
            )
        for data in fig_issue.data:
            if isinstance(data, go.Bar):
                data.update(text=data.y, textposition='outside')
        st.plotly_chart(fig_issue, use_container_width=True)
    
        # --- Vehicle Part Condition Overview (Final Row with 3 Charts) ---
        st.subheader("Vehicle Part Condition Overview")
        part_conditions = {
            'Tire_Condition': 'Tire Condition',
            'Brake_Condition': 'Brake Condition',
            'Battery_Status': 'Battery Status'
        }
    
        col_tire, col_brake, col_battery = st.columns(3)
    
        for part, title, col in zip(part_conditions.keys(), part_conditions.values(), [col_tire, col_brake, col_battery]):
            condition_counts = df[part].value_counts().reset_index()
            condition_counts.columns = [part, 'Count']
    
            if value_type == "Show as Percentage":
                condition_counts['Percentage'] = round((condition_counts['Count'] / condition_counts['Count'].sum()) * 100, 3)
                fig_part = px.pie(
                    condition_counts,
                    names=part,
                    values='Percentage',
                    title=f'{title} (Percentage)',
                    hole=0.4
                )
            else:
                condition_counts['Count'] = condition_counts['Count'].round(3)
                fig_part = px.bar(
                    condition_counts,
                    x=part,
                    y='Count',
                    title=f'{title} (Count)',
                    color=part
                )
            for data in fig_part.data:
                if isinstance(data, go.Bar):
                    data.update(text=data.y, textposition='outside')
            col.plotly_chart(fig_part, use_container_width=True)
    
    # =============================== #
    # Diagnostic Analysis
    # =============================== #
    
    # --- KPI Section ---
    if selected_filter == "All" or selected_filter == "Diagnostic Analysis":
        st.header("📊 Key Performance Indicators")
    
        #Calculate KPIs
        vehicle_count = len(df)
    
        df['Mean_Time_Between_Failures'] = df['Mileage'] / (df['Reported_Issues'] + 1)
        mtbf = round(df['Mean_Time_Between_Failures'].mean(), 2)
    
        maintenance_rate = round((df[df['Need_Maintenance'] == 'Yes'].shape[0] / len(df)) * 100, 3)
    
        recurrent_issue_rate = round((df[df['Reported_Issues'] > 1].shape[0] / len(df)) * 100, 3)
    
        avg_mileage = round(df['Mileage'].mean(), 2)
    
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Vehicle Count", vehicle_count)
        with col2:
            st.metric("MTBF (km)", mtbf)
        with col3:
            st.metric("% Maintenance Rate", f"{maintenance_rate}%")
        with col4:
            st.metric("Avg Mileage", avg_mileage)
        with col5:
            st.metric("% Recurrent Issues", f"{recurrent_issue_rate}%")
    
    
    # --- Diagnostic Analysis Section ---
    if selected_filter == "All" or selected_filter == "Diagnostic Analysis":
        st.header("🔍 Diagnostic Analysis")
    
        # --- Avg Insurance Premium by Maintenance History ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Avg Insurance Premium by Maintenance History")
            df['Insurance_Premium'] = pd.to_numeric(df['Insurance_Premium'], errors='coerce')
            premium_df = df.groupby('Maintenance_History')['Insurance_Premium'].mean().reset_index()
    
            if value_type == "Show as Count":
                premium_df['Insurance_Premium'] = premium_df['Insurance_Premium'].round(3)
                fig1 = px.bar(
                    premium_df, 
                    x='Maintenance_History', 
                    y='Insurance_Premium',
                    color='Maintenance_History',
                    title='Avg Insurance Premium by Maintenance History (Count)',
                    labels={'Insurance_Premium': 'Avg Premium', 'Maintenance_History': 'Maintenance History'},
                    hover_data=['Insurance_Premium']
                )
                for trace in fig1.data:
                    trace.update(text=trace.y, textposition='outside', textangle=0, texttemplate='%{text:.3f}')
                st.plotly_chart(fig1, use_container_width=True)
            else:
                premium_df['Insurance_Premium_Percentage'] = (premium_df['Insurance_Premium'] / premium_df['Insurance_Premium'].max()) * 100
                premium_df['Insurance_Premium_Percentage'] = premium_df['Insurance_Premium_Percentage'].round(3)
                fig1_pie = px.pie(
                    premium_df, 
                    names='Maintenance_History', 
                    values='Insurance_Premium_Percentage',
                    title='Avg Insurance Premium by Maintenance History (Percentage)', 
                    hole=0.4
                )
                fig1_pie.update_traces(textinfo='percent+label')
                st.plotly_chart(fig1_pie, use_container_width=True)
    
        # --- Reported Issues Count ---
        with col2:
            st.subheader("Reported Issues Count")
            issue_df = df['Reported_Issues'].value_counts().reset_index()
            issue_df.columns = ['Reported_Issues', 'Count']
    
            if value_type == "Show as Count":
                issue_df['Count'] = issue_df['Count'].round(3)
                fig2 = px.bar(
                    issue_df, 
                    x='Reported_Issues', 
                    y='Count',
                    title='Reported Issues Distribution (Count)', 
                    labels={'Count': 'Reported Issues Count', 'Reported_Issues': 'Reported Issues'},
                    hover_data=['Count']
                )
                for trace in fig2.data:
                    trace.update(text=trace.y, textposition='outside', textangle=0, texttemplate='%{text:.3f}')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                issue_df['Percentage'] = (issue_df['Count'] / issue_df['Count'].sum()) * 100
                issue_df['Percentage'] = issue_df['Percentage'].round(3)
                fig2_pie = px.pie(
                    issue_df, 
                    names='Reported_Issues', 
                    values='Percentage',
                    title='Reported Issues Distribution (Percentage)', 
                    hole=0.4, 
                    color='Reported_Issues', 
                    labels={'Percentage': 'Reported Issues (%)'}
                )
                fig2_pie.update_traces(textinfo='percent+label', pull=[0.1] * len(issue_df))
                st.plotly_chart(fig2_pie, use_container_width=True)
    
        # --- Mileage by Vehicle Model & Owner Type ---
        col3_new, col4_new = st.columns(2)
    
        with col3_new:
            st.subheader("Mileage by Vehicle Model & Owner Type")
            mileage_df = df.groupby(['Vehicle_Model', 'Owner_Type'])['Mileage'].mean().reset_index()
    
            if value_type == "Show as Count":
                mileage_df['Mileage'] = mileage_df['Mileage'].round(3)
                fig_mileage = px.bar(
                    mileage_df,
                    x='Vehicle_Model',
                    y='Mileage',
                    color='Owner_Type',
                    title='Avg Mileage by Vehicle Model & Owner Type (Count)',
                    labels={'Mileage': 'Avg Mileage (km)', 'Vehicle_Model': 'Vehicle Model'},
                    hover_data=['Mileage']
                )
                for trace in fig_mileage.data:
                    trace.update(text=trace.y, textposition='outside', textangle=0, texttemplate='%{text:.3f}')
                st.plotly_chart(fig_mileage, use_container_width=True)
            else:
                mileage_df['Mileage_Percentage'] = (mileage_df['Mileage'] / mileage_df['Mileage'].max()) * 100
                mileage_df['Mileage_Percentage'] = mileage_df['Mileage_Percentage'].round(3)
                fig_mileage_pie = px.pie(
                    mileage_df,
                    names='Vehicle_Model',
                    values='Mileage_Percentage',
                    title='Mileage by Vehicle Model (Percentage)',
                    hole=0.4
                )
                fig_mileage_pie.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_mileage_pie, use_container_width=True)
    
        with col4_new:
            st.subheader("Maintenance Frequency by Vehicle Model")
            maintenance_freq = df.groupby('Vehicle_Model').size().reset_index(name='Maintenance_Count')
            maintenance_freq = maintenance_freq.sort_values(by='Maintenance_Count', ascending=False)
    
            if value_type == "Show as Count":
                maintenance_freq['Maintenance_Count'] = maintenance_freq['Maintenance_Count'].round(3)
                fig_maintenance = px.bar(
                    maintenance_freq.head(10),
                    x='Vehicle_Model',
                    y='Maintenance_Count',
                    title='Vehicle Models by Maintenance Count',
                    labels={'Maintenance_Count': 'Maintenance Count', 'Vehicle_Model': 'Vehicle Model'},
                    hover_data=['Maintenance_Count'],
                    color='Vehicle_Model'
                )
                for trace in fig_maintenance.data:
                    trace.update(text=trace.y, textposition='outside', textangle=0, texttemplate='%{text:.3f}')
                st.plotly_chart(fig_maintenance, use_container_width=True)
            else:
                maintenance_freq['Maintenance_Percentage'] = (maintenance_freq['Maintenance_Count'] / maintenance_freq['Maintenance_Count'].sum()) * 100
                maintenance_freq['Maintenance_Percentage'] = maintenance_freq['Maintenance_Percentage'].round(3)
                fig_maintenance_pie = px.pie(
                    maintenance_freq.head(10),
                    names='Vehicle_Model',
                    values='Maintenance_Percentage',
                    title='Vehicle Models by Maintenance (%)',
                    hole=0.4
                )
                fig_maintenance_pie.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_maintenance_pie, use_container_width=True)
    
        st.subheader("Fuel Inefficiency Triggers")
        df['Fuel_Efficiency'] = pd.to_numeric(df['Fuel_Efficiency'], errors='coerce')
        fuel_df = df.groupby(['Tire_Condition', 'Engine_Size'])['Fuel_Efficiency'].mean().reset_index()
    
        if value_type == "Show as Count":
            fuel_df['Fuel_Efficiency'] = fuel_df['Fuel_Efficiency'].round(3)
            fig3 = px.bar(
                fuel_df, 
                x='Tire_Condition', 
                y='Fuel_Efficiency', 
                color='Engine_Size',
                title='Fuel Efficiency by Tire Condition & Engine Size (Count)'
            )
            for trace in fig3.data:
                trace.update(text=trace.y, textposition='outside', textangle=0, texttemplate='%{text:.3f}')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            fuel_df['Fuel_Efficiency_Percentage'] = (fuel_df['Fuel_Efficiency'] / fuel_df['Fuel_Efficiency'].max()) * 100
            fuel_df['Fuel_Efficiency_Percentage'] = fuel_df['Fuel_Efficiency_Percentage'].round(3)
            fig3_pie = px.pie(
                fuel_df, 
                names='Tire_Condition', 
                values='Fuel_Efficiency_Percentage',
                title='Fuel Efficiency by Tire Condition & Engine Size (Percentage)', 
                hole=0.4
            )
            fig3_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig3_pie, use_container_width=True)
    
# --- Session Control ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    vehicle_eda_page()  # Show the EDA page after successful login
else:
    login_page()  # Show the login page if not logged in
