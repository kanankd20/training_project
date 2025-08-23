import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np


st.set_page_config(
    page_title="Cybersecurity Attacks Dashboard",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Create sample data for demonstration

def load_sample_data():
    
    years = list(range(2015, 2025))
    attack_types = [
        'Phishing', 'Ransomware', 'DDoS', 'Malware', 
        'SQL Injection', 'XSS', 'Brute Force', 'Zero-day'
    ]
    
    data = []
    for year in years:
        for attack in attack_types:
            for _ in range(np.random.randint(5, 20)):
                data.append({
                    'year': year,
                    'attack_type': attack,
                    'date': f"{year}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 28):02d}",
                    'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], p=[0.3, 0.4, 0.2, 0.1]),
                    'target_sector': np.random.choice(['Finance', 'Healthcare', 'Education', 'Government', 'Retail']),
                    'affected_users': np.random.randint(100, 10000),
                    'financial_loss': np.random.randint(10000, 1000000)
                })
    
    return pd.DataFrame(data)


df = load_sample_data()


df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Year range
year_range = st.sidebar.slider(
    "Select Year Range:",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=(int(df['year'].min()), int(df['year'].max()))
)

# Attack type 
attack_types = st.sidebar.multiselect(
    "Select Attack Types:",
    options=df['attack_type'].unique(),
    default=df['attack_type'].unique()
)

# level of attack range
severity_levels = st.sidebar.multiselect(
    "Select Severity Levels:",
    options=df['severity'].unique(),
    default=df['severity'].unique()
)

filtered_df = df[
    (df['year'] >= year_range[0]) & 
    (df['year'] <= year_range[1]) &
    (df['attack_type'].isin(attack_types)) &
    (df['severity'].isin(severity_levels))
]

# Main dashboard
st.title("🛡 Cybersecurity Attacks Dashboard")
st.text("Welcome to  the world of Information on Cybersecurity technology.As, we all know , as the Technology increases rapidly ,there is tremendous use of networks all over the world. This information is related to cybersecurity attacks which happened in last few years i.e from 2015-2024.It helps to identify and analyze the attacks like phishing, malware, man in the middle etc. with help of their introduction and some visualisations.This report is mainly used to gather information for awareness among people and help governments and other campaign awareness people to know about which country suffers a lot and how their income and gdp rates decreases due to these kinds of cybersecurity attacks to promote awareness and by making policies for welfare of society.")
st.markdown("### Comprehensive analysis of cybersecurity incidents over time")
#col creation
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_attacks = len(filtered_df)
    st.metric("Total Attacks", f"{total_attacks:,}")

with col2:
    avg_severity = filtered_df['severity'].value_counts().idxmax()
    st.metric("Most Common Severity", avg_severity)

with col3:
    total_users = filtered_df['affected_users'].sum()
    st.metric("Total Affected Users", f"{total_users:,}")

with col4:
    total_loss = filtered_df['financial_loss'].sum()
    st.metric("Total Financial Loss", f"${total_loss:,}")

# Tab layout 
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview", "🔍 Attack Details", "📊 Sector Analysis", "📅 Timeline"
])

with tab1:
    st.header("Attack Trends by Year")
    
    # Attacks by year and type
    yearly_attacks = filtered_df.groupby(['year', 'attack_type']).size().reset_index(name='count')
    
    fig1 = px.bar(
        yearly_attacks,
        x='year',
        y='count',
        color='attack_type',
        title='Number of Attacks by Year and Type',
        labels={'count': 'Number of Attacks', 'year': 'Year'}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Severity distribution
    col1, col2 = st.columns(2)
    
    with col1:
        severity_dist = filtered_df['severity'].value_counts()
        fig2 = px.pie(
            values=severity_dist.values,
            names=severity_dist.index,
            title='Attack Severity Distribution'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        sector_attacks = filtered_df['target_sector'].value_counts().head(10)
        fig3 = px.bar(
            x=sector_attacks.values,
            y=sector_attacks.index,
            orientation='h',
            title='Top 10 Targeted Sectors',
            labels={'x': 'Number of Attacks', 'y': 'Sector'}
        )
        st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.header("Detailed Attack Analysis")
    selected_attack = st.selectbox(
        "Select Attack Type for Detailed Analysis:",
        options=filtered_df['attack_type'].unique()
    )
    
    attack_data = filtered_df[filtered_df['attack_type'] == selected_attack]
    
    if not attack_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Yearly trend for selected attack
            attack_trend = attack_data.groupby('year').size().reset_index(name='count')
            fig4 = px.line(
                attack_trend,
                x='year',
                y='count',
                title=f'{selected_attack} Attacks Over Time',
                markers=True
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            # Severity distribution for selected attack
            attack_severity = attack_data['severity'].value_counts()
            fig5 = px.pie(
                values=attack_severity.values,
                names=attack_severity.index,
                title=f'{selected_attack} Severity Distribution'
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        # Show detailed data
        st.subheader(f"Detailed {selected_attack} Attack Records")
        st.dataframe(
            attack_data[['date', 'severity', 'target_sector', 'affected_users', 'financial_loss']]
            .sort_values('date', ascending=False)
            .head(20)
        )

with tab3:
    st.header("Sector-wise Analysis")
    
    # Select sector for analysis
    selected_sector = st.selectbox(
        "Select Sector for Analysis:",
        options=filtered_df['target_sector'].unique()
    )
    
    sector_data = filtered_df[filtered_df['target_sector'] == selected_sector]
    
    if not sector_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Attack types in selected sector
            sector_attacks = sector_data['attack_type'].value_counts()
            fig6 = px.bar(
                x=sector_attacks.values,
                y=sector_attacks.index,
                orientation='h',
                title=f'Attack Types in {selected_sector} Sector',
                labels={'x': 'Number of Attacks', 'y': 'Attack Type'}
            )
            st.plotly_chart(fig6, use_container_width=True)
        
        with col2:
            # Yearly trend for selected sector
            sector_trend = sector_data.groupby('year').size().reset_index(name='count')
            fig7 = px.line(
                sector_trend,
                x='year',
                y='count',
                title=f'{selected_sector} Sector Attacks Over Time',
                markers=True
            )
            st.plotly_chart(fig7, use_container_width=True)
        
        # Financial impact analysis
        st.subheader("Financial Impact Analysis")
        financial_data = sector_data.groupby('year')['financial_loss'].sum().reset_index()
        fig8 = px.area(
            financial_data,
            x='year',
            y='financial_loss',
            title=f'Total Financial Loss in {selected_sector} Sector',
            labels={'financial_loss': 'Total Loss ($)', 'year': 'Year'}
        )
        st.plotly_chart(fig8, use_container_width=True)

with tab4:
    st.header("Timeline Analysis")
    
    # Monthly timeline
    monthly_data = filtered_df.groupby([filtered_df['date'].dt.to_period('M')]).size()
    monthly_data.index = monthly_data.index.astype(str)
    
    fig9 = px.line(
        x=monthly_data.index,
        y=monthly_data.values,
        title='Monthly Attack Timeline',
        labels={'x': 'Month', 'y': 'Number of Attacks'}
    )
    fig9.update_xaxes(tickangle=45)
    st.plotly_chart(fig9, use_container_width=True)
    
    # Heatmap of attacks by month and year
    heatmap_data = filtered_df.copy()
    heatmap_data['month'] = heatmap_data['date'].dt.month_name()
    heatmap_data['year'] = heatmap_data['year'].astype(str)
    
    pivot_data = heatmap_data.groupby(['year', 'month']).size().reset_index(name='count')
    
    fig10 = px.density_heatmap(
        pivot_data,
        x='year',
        y='month',
        z='count',
        title='Attack Density Heatmap (Year vs Month)',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig10, use_container_width=True)




st.markdown("---")