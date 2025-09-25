#!/usr/bin/env python3
"""
NodeGoat Setup Script for Pasifika Database Project
This script sets up a local development environment for NodeGoat
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🐐 Setting up NodeGoat for Pasifika Database Project")
    print("=" * 60)
    
    # Check if we have the required directories
    base_dir = Path(__file__).parent
    nodegoat_dir = base_dir / "nodegoat"
    cc1100_dir = base_dir / "1100CC"
    
    if not nodegoat_dir.exists():
        print("❌ NodeGoat directory not found. Please ensure you've cloned the repository.")
        return False
    
    if not cc1100_dir.exists():
        print("❌ 1100CC directory not found. Please ensure you've cloned the repository.")
        return False
    
    print("✅ Found NodeGoat and 1100CC directories")
    
    # Create a simple PHP server setup
    setup_php_server(base_dir)
    
    # Create a simple data import script
    create_data_import_script(base_dir)
    
    print("\n🎉 NodeGoat setup complete!")
    print("\nNext steps:")
    print("1. Install PHP and MySQL/MariaDB on your system")
    print("2. Set up the databases as described in the SETUP.md files")
    print("3. Configure your web server to point to the 1100CC/APP directory")
    print("4. Access NodeGoat at http://localhost/nodegoat")
    
    return True

def setup_php_server(base_dir):
    """Create a simple PHP development server setup"""
    print("\n📁 Setting up PHP development environment...")
    
    # Create a simple start script
    start_script = base_dir / "start-nodegoat.sh"
    with open(start_script, 'w') as f:
        f.write("""#!/bin/bash
echo "🐐 Starting NodeGoat Development Server"
echo "Make sure you have PHP and MySQL installed"
echo "Starting PHP development server on http://localhost:8080"
cd 1100CC/APP
php -S localhost:8080
""")
    
    # Make it executable
    os.chmod(start_script, 0o755)
    print(f"✅ Created start script: {start_script}")

def create_data_import_script(base_dir):
    """Create a script to import Pasifika data into NodeGoat"""
    print("\n📊 Creating data import script...")
    
    import_script = base_dir / "import-pasifika-data.py"
    with open(import_script, 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Pasifika Data Import Script for NodeGoat
This script prepares your Pasifika data for import into NodeGoat
\"\"\"

import json
import csv
import os
from pathlib import Path

def import_film_data():
    \"\"\"Import film data from CSV files\"\"\"
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
    \"\"\"Import geospatial data from GeoJSON files\"\"\"
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
    
    print(f"\\n🎉 Import complete!")
    print(f"📊 Films: {len(films)}")
    print(f"🗺️  GeoJSON files: {len(geojson_files)}")
    print("\\nNext: Import the generated JSON files into NodeGoat")

if __name__ == "__main__":
    main()
""")
    
    # Make it executable
    os.chmod(import_script, 0o755)
    print(f"✅ Created import script: {import_script}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
