#!/usr/bin/env python3
"""
Filter the real Pacific islands to include only major islands relevant to our film data.
This will create a more manageable dataset with actual island shapes.
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

def get_island_area(feature):
    """Get the area of an island from its properties."""
    props = feature.get('properties', {})
    return props.get('area', 0)

def is_major_island(feature):
    """Determine if an island is major enough to include."""
    area = get_island_area(feature)
    name = feature.get('properties', {}).get('name', '').lower()
    
    # Include islands with significant area (larger than 1 km²)
    if area > 1.0:
        return True
    
    # Include specific known islands even if small
    major_island_names = [
        'hawaii', 'oahu', 'maui', 'kauai', 'molokai', 'lanai', 'niihau', 'kahoolawe',
        'fiji', 'viti levu', 'vanua levu', 'taveuni', 'kadavu',
        'samoa', 'upolu', 'savaii', 'tutuila', 'manono',
        'tonga', 'tongatapu', 'vavau', 'haapai', 'eua',
        'tahiti', 'moorea', 'bora bora', 'huahine', 'raiatea',
        'new caledonia', 'grande terre', 'lifou', 'mare',
        'vanuatu', 'efate', 'espiritu santo', 'malekula', 'ambrym',
        'solomon islands', 'guadalcanal', 'malaita', 'new georgia',
        'papua new guinea', 'new britain', 'new ireland', 'bougainville',
        'palau', 'babeldaob', 'koror', 'peleliu',
        'marshall islands', 'majuro', 'kwajalein', 'ebeye',
        'kiribati', 'tarawa', 'christmas island', 'kiritimati',
        'tuvalu', 'funafuti', 'nanumea', 'nanumanga',
        'nauru', 'cook islands', 'rarotonga', 'aitutaki',
        'french polynesia', 'marquesas', 'gambier', 'austral',
        'easter island', 'rapa nui', 'pitcairn', 'norfolk',
        'guam', 'saipan', 'tinian', 'rota',
        'federated states of micronesia', 'ponape', 'kosrae', 'yap', 'chuuk',
        'niue', 'tokelau', 'wallis and futuna', 'american samoa',
        'northern mariana islands', 'wake island', 'johnston atoll',
        'midway', 'palmyra', 'jarvis', 'baker', 'howland'
    ]
    
    for major_name in major_island_names:
        if major_name in name:
            return True
    
    return False

def filter_major_islands():
    """Filter the Pacific islands to include only major ones."""
    print("Loading real Pacific islands dataset...")
    islands_data = load_geojson('real-pacific-islands.geojson')
    
    if not islands_data:
        print("Failed to load real Pacific islands data")
        return
    
    print(f"Loaded {len(islands_data['features'])} total Pacific islands")
    
    # Filter for major islands
    major_islands = []
    for feature in islands_data['features']:
        if is_major_island(feature):
            major_islands.append(feature)
    
    print(f"Filtered to {len(major_islands)} major islands")
    
    # Sort by area (largest first)
    major_islands.sort(key=get_island_area, reverse=True)
    
    # Create the output GeoJSON
    output_data = {
        "type": "FeatureCollection",
        "features": major_islands
    }
    
    # Save to file
    output_file = "major-pacific-islands.geojson"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Saved {len(major_islands)} major Pacific islands to {output_file}")
    
    # Print some statistics
    regions = {}
    for feature in major_islands:
        region = feature['properties']['region']
        regions[region] = regions.get(region, 0) + 1
    
    print("\nMajor islands by region:")
    for region, count in sorted(regions.items()):
        print(f"  {region}: {count} islands")
    
    # Print top 20 largest islands
    print("\nTop 20 largest islands:")
    for i, feature in enumerate(major_islands[:20]):
        name = feature['properties']['name']
        area = feature['properties']['area']
        region = feature['properties']['region']
        print(f"  {i+1:2d}. {name} ({area:.1f} km²) - {region}")
    
    return output_file

if __name__ == "__main__":
    filter_major_islands()

