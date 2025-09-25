#!/usr/bin/env python3
"""
Extract real Pacific island shapes from the GlobalIsl_Merg_FeaturesToJSO.geojson file
and create a proper GeoJSON file with actual island boundaries for our visualization.
"""

import json
import sys
from pathlib import Path

def load_geojson(file_path):
    """Load a GeoJSON file and return the data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def is_pacific_island(feature):
    """Check if a feature is a Pacific island based on coordinates and properties."""
    if not feature.get('geometry') or not feature.get('properties'):
        return False
    
    # Get coordinates to check if it's in the Pacific region
    geometry = feature['geometry']
    if geometry['type'] == 'Polygon':
        coords = geometry['coordinates'][0]  # First ring of polygon
    elif geometry['type'] == 'MultiPolygon':
        coords = geometry['coordinates'][0][0]  # First ring of first polygon
    else:
        return False
    
    # Check if coordinates are in Pacific region (rough bounds)
    # Pacific: roughly 100°E to 80°W longitude, 60°N to 60°S latitude
    for coord in coords[:10]:  # Check first 10 coordinates for efficiency
        lon, lat = coord
        if -180 <= lon <= -100 or 100 <= lon <= 180:  # Pacific longitude range
            if -60 <= lat <= 60:  # Pacific latitude range
                return True
    
    return False

def get_island_name(feature):
    """Extract island name from feature properties."""
    props = feature.get('properties', {})
    
    # Try different possible name fields
    name_fields = ['Name_USGSO', 'NAME_wcmcI', 'NAME_LOCAL', 'GEONAME']
    for field in name_fields:
        if props.get(field) and props[field].strip():
            return props[field].strip()
    
    return "Unnamed Island"

def get_island_region(feature):
    """Determine the Pacific region based on coordinates."""
    geometry = feature['geometry']
    if geometry['type'] == 'Polygon':
        coords = geometry['coordinates'][0]
    elif geometry['type'] == 'MultiPolygon':
        coords = geometry['coordinates'][0][0]
    else:
        return "Unknown"
    
    # Get center coordinates
    lons = [coord[0] for coord in coords]
    lats = [coord[1] for coord in coords]
    center_lon = sum(lons) / len(lons)
    center_lat = sum(lats) / len(lats)
    
    # Determine region based on coordinates
    if 140 <= center_lon <= 180 and -30 <= center_lat <= 10:
        return "Melanesia"
    elif -180 <= center_lon <= -140 and 10 <= center_lat <= 30:
        return "Hawaii"
    elif -180 <= center_lon <= -140 and -30 <= center_lat <= 10:
        return "Polynesia"
    elif 140 <= center_lon <= 180 and 10 <= center_lat <= 30:
        return "Micronesia"
    else:
        return "Pacific"

def extract_pacific_islands():
    """Extract Pacific islands from the global dataset."""
    print("Loading global island dataset...")
    global_data = load_geojson('pasifikageo/GlobalIsl_Merg_FeaturesToJSO.geojson')
    
    if not global_data:
        print("Failed to load global island data")
        return
    
    print(f"Loaded {len(global_data['features'])} total features")
    
    # Filter for Pacific islands
    pacific_islands = []
    processed = 0
    
    for feature in global_data['features']:
        processed += 1
        if processed % 10000 == 0:
            print(f"Processed {processed} features...")
        
        if is_pacific_island(feature):
            # Create a simplified feature with just the essential data
            simplified_feature = {
                "type": "Feature",
                "properties": {
                    "name": get_island_name(feature),
                    "region": get_island_region(feature),
                    "area": feature['properties'].get('IslandArea', 0)
                },
                "geometry": feature['geometry']
            }
            pacific_islands.append(simplified_feature)
    
    print(f"Found {len(pacific_islands)} Pacific islands")
    
    # Create the output GeoJSON
    output_data = {
        "type": "FeatureCollection",
        "features": pacific_islands
    }
    
    # Save to file
    output_file = "real-pacific-islands.geojson"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Saved {len(pacific_islands)} Pacific islands to {output_file}")
    
    # Print some statistics
    regions = {}
    for feature in pacific_islands:
        region = feature['properties']['region']
        regions[region] = regions.get(region, 0) + 1
    
    print("\nIslands by region:")
    for region, count in sorted(regions.items()):
        print(f"  {region}: {count} islands")
    
    return output_file

if __name__ == "__main__":
    extract_pacific_islands()
