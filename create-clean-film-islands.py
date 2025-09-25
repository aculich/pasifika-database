#!/usr/bin/env python3
"""
Create a clean, focused GeoJSON file with the major islands mentioned in our film data.
This will remove duplicates and focus on the most relevant islands.
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
    
    # Handle common variations and mappings
    name_mappings = {
        'big island': 'hawaii',
        'o\'ahu': 'oahu',
        'oahu': 'oahu',
        'rapa nui': 'easter island',
        'papua new guinea': 'new guinea',
        'aotearoa': 'new zealand',
        'te ika-a-māui': 'north island',
        'te ika-a-māui / north island': 'north island',
        'manono island': 'manono',
        'upolu island': 'upolu',
        'tanna island': 'tanna',
        'bougainville island': 'bougainville',
        'goulburn islands': 'goulburn',
        'satawal': 'satawal',
        'satawal ': 'satawal',
        'rapa nui ': 'easter island',
        'honolulu': 'oahu',  # Honolulu is on Oahu
        'jarvis': 'jarvis island',
        'kosrae': 'kosrae',
        'rotuma': 'rotuma',
        'saipan': 'saipan',
        'tongatapu': 'tongatapu',
        'tuvalu': 'tuvalu',
        'kiribati': 'kiribati',
        'guam': 'guam',
        'maui': 'maui',
        'molokai': 'molokai',
        'hawaii': 'hawaii',
        'north island': 'north island',
        'australia': 'australia'
    }
    
    return name_mappings.get(name, name)

def is_target_island(feature, target_islands):
    """Check if an island matches our target list."""
    name = feature.get('properties', {}).get('name', '').lower().strip()
    normalized_name = normalize_island_name(name)
    
    # Check if it matches any of our target islands
    for target in target_islands:
        if normalize_island_name(target) == normalized_name:
            return True
    
    return False

def create_clean_film_islands():
    """Create a clean GeoJSON file with islands relevant to our film data."""
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
    
    # Create a set of target islands (normalized)
    target_islands = set()
    for island in film_islands:
        target_islands.add(normalize_island_name(island))
    
    print(f"\nTarget islands (normalized): {sorted(target_islands)}")
    
    # Filter for target islands, keeping only the largest version of each
    island_groups = {}
    
    for feature in islands_data['features']:
        if is_target_island(feature, film_islands):
            name = feature.get('properties', {}).get('name', '').lower().strip()
            normalized_name = normalize_island_name(name)
            area = feature.get('properties', {}).get('area', 0)
            
            # Keep the largest version of each island
            if normalized_name not in island_groups or area > island_groups[normalized_name]['area']:
                island_groups[normalized_name] = {
                    'feature': feature,
                    'area': area,
                    'original_name': name
                }
    
    print(f"\nFound {len(island_groups)} unique target islands")
    
    # Create the final list of features
    final_features = []
    for normalized_name, data in island_groups.items():
        feature = data['feature']
        props = feature['properties'].copy()
        props['film_relevant'] = True
        props['normalized_name'] = normalized_name
        props['original_film_name'] = data['original_name']
        
        feature_copy = feature.copy()
        feature_copy['properties'] = props
        final_features.append(feature_copy)
    
    # Sort by area (largest first)
    final_features.sort(key=lambda x: x['properties']['area'], reverse=True)
    
    # Create the output GeoJSON
    output_data = {
        "type": "FeatureCollection",
        "features": final_features
    }
    
    # Save to file
    output_file = "clean-film-islands.geojson"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Saved {len(final_features)} clean film islands to {output_file}")
    
    # Print the final list
    print("\nFinal islands (sorted by area):")
    for i, feature in enumerate(final_features):
        props = feature['properties']
        name = props['name']
        area = props['area']
        region = props['region']
        original_name = props['original_film_name']
        print(f"  {i+1:2d}. {name} ({area:.1f} km²) - {region} [from: {original_name}]")
    
    return output_file

if __name__ == "__main__":
    create_clean_film_islands()
