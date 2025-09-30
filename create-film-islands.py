#!/usr/bin/env python3
"""
Create a focused GeoJSON file with only the islands mentioned in our film data,
plus some key Pacific islands for geographic context.
"""

import json
from pathlib import Path

def load_geojson(file_path):
    """Load a GeoJSON file and return the data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def load_film_data():
    """Load the film data to get the list of islands mentioned."""
    try:
        with open('nodegoat-film-data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading film data: {e}")
        return []

def get_film_islands():
    """Get the set of islands mentioned in the film data."""
    films = load_film_data()
    islands = set()
    
    for film in films:
        if film.get('island'):
            island = film['island'].strip()
            if island:
                islands.add(island)
    
    return islands

def normalize_island_name(name):
    """Normalize island names for matching."""
    name = name.lower().strip()
    
    # Handle common variations
    variations = {
        'big island': ['hawaii', 'hawaii island'],
        'oahu': ['o\'ahu', 'oahu'],
        'rapa nui': ['easter island'],
        'papua new guinea': ['new guinea'],
        'aotearoa': ['new zealand', 'north island', 'south island'],
        'te ika-a-māui': ['north island', 'te ika-a-maui'],
        'manono island': ['manono'],
        'upolu island': ['upolu'],
        'tanna island': ['tanna'],
        'bougainville island': ['bougainville'],
        'goulburn islands': ['goulburn'],
        'satawal': ['satawal island']
    }
    
    for standard, variants in variations.items():
        if name in variants or name == standard:
            return standard
    
    return name

def is_relevant_island(feature, film_islands, key_islands):
    """Check if an island is relevant to our film data or is a key Pacific island."""
    name = feature.get('properties', {}).get('name', '').lower().strip()
    normalized_name = normalize_island_name(name)
    
    # Check if it's mentioned in film data
    for film_island in film_islands:
        if normalize_island_name(film_island) == normalized_name:
            return True
    
    # Check if it's a key Pacific island
    for key_island in key_islands:
        if key_island.lower() in name or name in key_island.lower():
            return True
    
    return False

def create_film_islands_geojson():
    """Create a GeoJSON file with islands relevant to our film data."""
    print("Loading major Pacific islands dataset...")
    islands_data = load_geojson('major-pacific-islands.geojson')
    
    if not islands_data:
        print("Failed to load major Pacific islands data")
        return
    
    print(f"Loaded {len(islands_data['features'])} major Pacific islands")
    
    # Get islands mentioned in film data
    film_islands = get_film_islands()
    print(f"Found {len(film_islands)} islands mentioned in film data:")
    for island in sorted(film_islands):
        print(f"  - {island}")
    
    # Key Pacific islands for geographic context
    key_islands = [
        'Fiji', 'Samoa', 'Tonga', 'Tahiti', 'New Caledonia', 'Vanuatu',
        'Solomon Islands', 'Palau', 'Marshall Islands', 'Kiribati',
        'Tuvalu', 'Nauru', 'Cook Islands', 'French Polynesia',
        'American Samoa', 'Guam', 'Northern Mariana Islands',
        'Federated States of Micronesia', 'Niue', 'Tokelau',
        'Wallis and Futuna', 'Pitcairn', 'Norfolk Island'
    ]
    
    # Filter for relevant islands
    relevant_islands = []
    for feature in islands_data['features']:
        if is_relevant_island(feature, film_islands, key_islands):
            # Update the properties to include film relevance
            props = feature['properties'].copy()
            props['film_relevant'] = True
            props['mentioned_in_films'] = any(
                normalize_island_name(film_island) == normalize_island_name(props['name'])
                for film_island in film_islands
            )
            
            feature_copy = feature.copy()
            feature_copy['properties'] = props
            relevant_islands.append(feature_copy)
    
    print(f"Filtered to {len(relevant_islands)} relevant islands")
    
    # Create the output GeoJSON
    output_data = {
        "type": "FeatureCollection",
        "features": relevant_islands
    }
    
    # Save to file
    output_file = "film-relevant-islands.geojson"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Saved {len(relevant_islands)} relevant islands to {output_file}")
    
    # Print some statistics
    film_mentioned = [f for f in relevant_islands if f['properties'].get('mentioned_in_films')]
    print(f"\nIslands mentioned in films: {len(film_mentioned)}")
    for feature in film_mentioned:
        name = feature['properties']['name']
        region = feature['properties']['region']
        area = feature['properties']['area']
        print(f"  - {name} ({area:.1f} km²) - {region}")
    
    return output_file

if __name__ == "__main__":
    create_film_islands_geojson()

