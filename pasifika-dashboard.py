#!/usr/bin/env python3
"""
Pasifika Database Dashboard
A Streamlit-based alternative to BaseRow for viewing and managing Pasifika data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from pathlib import Path
import glob

# Page configuration
st.set_page_config(
    page_title="Pasifika Database Dashboard",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .island-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_film_data():
    """Load and cache film data from CSV files"""
    film_files = glob.glob("pasifikafilm/**/*.csv", recursive=True)
    film_data = []
    
    for file in film_files:
        try:
            df = pd.read_csv(file)
            if not df.empty:
                film_data.append(df)
        except Exception as e:
            st.warning(f"Could not load {file}: {e}")
    
    if film_data:
        return pd.concat(film_data, ignore_index=True)
    return pd.DataFrame()

@st.cache_data
def load_geojson_data():
    """Load and cache GeoJSON data"""
    geojson_files = glob.glob("**/*.geojson", recursive=True)
    geojson_data = []
    
    for file in geojson_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                geojson_data.append({
                    'file': file,
                    'type': data.get('type', 'Unknown'),
                    'features': len(data.get('features', [])),
                    'properties': list(data.get('features', [{}])[0].get('properties', {}).keys()) if data.get('features') else []
                })
        except Exception as e:
            st.warning(f"Could not load {file}: {e}")
    
    return pd.DataFrame(geojson_data)

@st.cache_data
def get_data_summary():
    """Get summary statistics of the dataset"""
    total_size = 0
    file_counts = {}
    
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                ext = os.path.splitext(file)[1].lower()
                file_counts[ext] = file_counts.get(ext, 0) + 1
            except:
                pass
    
    return {
        'total_size_gb': total_size / (1024**3),
        'file_counts': file_counts,
        'total_files': sum(file_counts.values())
    }

def main():
    # Header
    st.markdown('<h1 class="main-header">🌺 Pasifika Database Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📊 Overview",
        "🎬 Film Database",
        "🗺️ Geospatial Data",
        "📈 Analytics",
        "🔧 Data Management"
    ])
    
    # Load data
    summary = get_data_summary()
    film_data = load_film_data()
    geojson_data = load_geojson_data()
    
    if page == "📊 Overview":
        st.header("Dataset Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Size", f"{summary['total_size_gb']:.1f} GB")
        
        with col2:
            st.metric("Total Files", f"{summary['total_files']:,}")
        
        with col3:
            st.metric("Film Records", f"{len(film_data):,}" if not film_data.empty else "0")
        
        with col4:
            st.metric("GeoJSON Files", f"{len(geojson_data):,}")
        
        # File type distribution
        st.subheader("File Type Distribution")
        if summary['file_counts']:
            file_df = pd.DataFrame(list(summary['file_counts'].items()), columns=['Extension', 'Count'])
            fig = px.pie(file_df, values='Count', names='Extension', title="File Types in Dataset")
            st.plotly_chart(fig, use_container_width=True)
        
        # Directory structure
        st.subheader("Directory Structure")
        st.code("""
        pasifika-database/
        ├── pasifikafilm/ (9.3 GB)
        │   ├── Island Files/ (4.2 GB)
        │   ├── Cartographic Design Elements/ (3.5 GB)
        │   ├── join-geojson/ (1.6 GB)
        │   └── Other files/
        └── pasifikageo/ (11 GB)
            ├── eez-shapes.gdb/ (8.5 GB)
            ├── national_waters_individual/ (2.5 GB)
            └── Other files/
        """)
    
    elif page == "🎬 Film Database":
        st.header("Film Database")
        
        if not film_data.empty:
            st.subheader("Film Data Preview")
            st.dataframe(film_data.head(10), use_container_width=True)
            
            # Film statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Film Statistics")
                st.write(f"Total Films: {len(film_data)}")
                if 'Release Date' in film_data.columns:
                    st.write(f"Date Range: {film_data['Release Date'].min()} - {film_data['Release Date'].max()}")
            
            with col2:
                st.subheader("Data Quality")
                missing_data = film_data.isnull().sum()
                if not missing_data.empty:
                    fig = px.bar(x=missing_data.index, y=missing_data.values, title="Missing Data by Column")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No film data found. Please check your CSV files.")
    
    elif page == "🗺️ Geospatial Data":
        st.header("Geospatial Data")
        
        if not geojson_data.empty:
            st.subheader("GeoJSON Files Overview")
            st.dataframe(geojson_data, use_container_width=True)
            
            # Geospatial statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("File Types")
                type_counts = geojson_data['type'].value_counts()
                fig = px.pie(values=type_counts.values, names=type_counts.index, title="GeoJSON Types")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Feature Counts")
                fig = px.histogram(geojson_data, x='features', title="Features per File")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No GeoJSON data found.")
    
    elif page == "📈 Analytics":
        st.header("Data Analytics")
        
        # FAIR CARE Analysis
        st.subheader("FAIR CARE Principles Analysis")
        
        fair_metrics = {
            "Findable": "✅ Data is well-organized with clear file structure",
            "Accessible": "✅ Data is stored locally and accessible",
            "Interoperable": "⚠️ Multiple formats (CSV, GeoJSON, NetCDF) need standardization",
            "Reusable": "✅ Data includes metadata and documentation",
            "Collective Benefit": "✅ Data serves Pacific Island communities",
            "Authority to Control": "✅ Data ownership is clearly defined",
            "Responsibility": "✅ Data collection methods are documented",
            "Ethics": "✅ Indigenous data sovereignty principles applied"
        }
        
        for principle, status in fair_metrics.items():
            st.write(f"**{principle}**: {status}")
        
        # 5 Vs Analysis
        st.subheader("5 Vs of Data Science")
        
        vs_analysis = {
            "Volume": f"{summary['total_size_gb']:.1f} GB across {summary['total_files']:,} files",
            "Velocity": "Static dataset with periodic updates",
            "Variety": f"{len(summary['file_counts'])} different file formats",
            "Veracity": "High quality data with documented collection methods",
            "Value": "High value for Pacific Island research and cultural preservation"
        }
        
        for v, description in vs_analysis.items():
            st.write(f"**{v}**: {description}")
    
    elif page == "🔧 Data Management":
        st.header("Data Management Tools")
        
        st.subheader("Airtable Integration (Coming Soon)")
        st.info("Once you provide the Airtable API key, we'll be able to:")
        st.write("• Export all data from Airtable")
        st.write("• Set up a BaseRow instance")
        st.write("• Import Airtable data into BaseRow")
        st.write("• Create a unified database interface")
        
        st.subheader("Current Data Export Options")
        if not film_data.empty:
            csv = film_data.to_csv(index=False)
            st.download_button(
                label="Download Film Data as CSV",
                data=csv,
                file_name="pasifika_films.csv",
                mime="text/csv"
            )
        
        if not geojson_data.empty:
            json_data = geojson_data.to_json(orient='records')
            st.download_button(
                label="Download GeoJSON Metadata as JSON",
                data=json_data,
                file_name="geojson_metadata.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
