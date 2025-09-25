#!/usr/bin/env python3
"""
Pasifika Data Import Script for NodeGoat
This script prepares your Pasifika data for import into NodeGoat
"""

import json
import csv
import os
from pathlib import Path

def import_film_data():
    """Import film data from CSV files"""
    print("🎬 Importing film data...")
    
    # Read the film database CSV
    film_csv = Path("pasifikafilm/join-geojson/Pasifika_Film_Database.csv")
    if film_csv.exists():
        with open(film_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            films = list(reader)
        
        print(f"✅ Found {len(films)} films in database")
        
        # Convert to NodeGoat format
        nodegoat_films = []
        for film in films:
            nodegoat_film = {
                "name": film.get("filmName", ""),
                "release_date": film.get("First Release Date", ""),
                "budget": film.get("budgetTot", ""),
                "country": film.get("countryAffil 1", ""),
                "island": film.get("island 1", ""),
                "language": film.get("lang", ""),
                "status": film.get("filmStatus", ""),
                "indigenous_leadership": film.get("Indigenous leadership in team?", ""),
                "streaming_platform": film.get("streamingPlatform", ""),
                "summary": film.get("summary", ""),
                "logline": film.get("logline", "")
            }
            nodegoat_films.append(nodegoat_film)
        
        # Save as JSON for NodeGoat import
        output_file = Path("nodegoat-film-data.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(nodegoat_films, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(nodegoat_films)} films to {output_file}")
        return nodegoat_films
    
    return []

def import_geospatial_data():
    """Import geospatial data from GeoJSON files"""
    print("🗺️  Importing geospatial data...")
    
    geojson_files = list(Path("pasifikageo").glob("**/*.geojson"))
    print(f"✅ Found {len(geojson_files)} GeoJSON files")
    
    # Process each GeoJSON file
    for geojson_file in geojson_files:
        print(f"  📄 Processing {geojson_file.name}")
        # Here you would add logic to process each GeoJSON file
        # and convert it to NodeGoat's expected format
    
    return geojson_files

def main():
    print("🐐 Pasifika Data Import for NodeGoat")
    print("=" * 40)
    
    # Import film data
    films = import_film_data()
    
    # Import geospatial data
    geojson_files = import_geospatial_data()
    
    print(f"\n🎉 Import complete!")
    print(f"📊 Films: {len(films)}")
    print(f"🗺️  GeoJSON files: {len(geojson_files)}")
    print("\nNext: Import the generated JSON files into NodeGoat")

if __name__ == "__main__":
    main()
