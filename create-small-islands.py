#!/usr/bin/env python3
"""
Create a small, simplified GeoJSON file with just the essential islands for our film data.
This will be much smaller and suitable for GitHub hosting.
"""

import json
import math

def simplify_coordinates(coords, tolerance=0.01):
    """Simplify coordinates using Douglas-Peucker algorithm with tolerance."""
    if len(coords) < 3:
        return coords
    
    # Simple decimation - keep every nth point
    step = max(1, len(coords) // 50)  # Keep max 50 points per polygon
    return coords[::step]

def create_small_islands_geojson():
    """Create a small GeoJSON file with simplified island shapes."""
    
    # Define simplified island shapes (manually created for key islands)
    islands = [
        {
            "name": "Hawaii",
            "region": "Hawaii",
            "area": 10492.9,
            "coordinates": [
                [-155.9, 19.0], [-155.0, 19.0], [-155.0, 20.0], [-155.9, 20.0], [-155.9, 19.0]
            ]
        },
        {
            "name": "Oahu",
            "region": "Hawaii", 
            "area": 1559.8,
            "coordinates": [
                [-158.3, 21.2], [-157.6, 21.2], [-157.6, 21.7], [-158.3, 21.7], [-158.3, 21.2]
            ]
        },
        {
            "name": "Maui",
            "region": "Hawaii",
            "area": 1893.2,
            "coordinates": [
                [-156.7, 20.5], [-155.9, 20.5], [-155.9, 21.0], [-156.7, 21.0], [-156.7, 20.5]
            ]
        },
        {
            "name": "Molokai",
            "region": "Hawaii",
            "area": 679.2,
            "coordinates": [
                [-157.2, 21.0], [-156.8, 21.0], [-156.8, 21.3], [-157.2, 21.3], [-157.2, 21.0]
            ]
        },
        {
            "name": "New Guinea",
            "region": "Pacific",
            "area": 773751.0,
            "coordinates": [
                [140.0, -10.0], [150.0, -10.0], [150.0, -5.0], [140.0, -5.0], [140.0, -10.0]
            ]
        },
        {
            "name": "North Island",
            "region": "Pacific",
            "area": 114573.1,
            "coordinates": [
                [174.0, -40.0], [179.0, -40.0], [179.0, -35.0], [174.0, -35.0], [174.0, -40.0]
            ]
        },
        {
            "name": "Bougainville",
            "region": "Melanesia",
            "area": 8750.8,
            "coordinates": [
                [154.5, -6.5], [156.0, -6.5], [156.0, -5.5], [154.5, -5.5], [154.5, -6.5]
            ]
        },
        {
            "name": "Upolu",
            "region": "Polynesia",
            "area": 1133.2,
            "coordinates": [
                [-172.0, -14.0], [-171.5, -14.0], [-171.5, -13.5], [-172.0, -13.5], [-172.0, -14.0]
            ]
        },
        {
            "name": "Tanna",
            "region": "Melanesia",
            "area": 563.4,
            "coordinates": [
                [169.0, -19.5], [169.5, -19.5], [169.5, -19.0], [169.0, -19.0], [169.0, -19.5]
            ]
        },
        {
            "name": "Guam",
            "region": "Micronesia",
            "area": 546.3,
            "coordinates": [
                [144.5, 13.0], [145.0, 13.0], [145.0, 13.5], [144.5, 13.5], [144.5, 13.0]
            ]
        },
        {
            "name": "Kiribati",
            "region": "Polynesia",
            "area": 475.8,
            "coordinates": [
                [173.0, 1.5], [174.0, 1.5], [174.0, 2.0], [173.0, 2.0], [173.0, 1.5]
            ]
        },
        {
            "name": "Saipan",
            "region": "Micronesia",
            "area": 120.9,
            "coordinates": [
                [145.5, 15.0], [146.0, 15.0], [146.0, 15.3], [145.5, 15.3], [145.5, 15.0]
            ]
        },
        {
            "name": "Jarvis",
            "region": "Polynesia",
            "area": 4.6,
            "coordinates": [
                [-160.0, -0.4], [-159.9, -0.4], [-159.9, -0.3], [-160.0, -0.3], [-160.0, -0.4]
            ]
        },
        {
            "name": "Manono",
            "region": "Polynesia",
            "area": 2.9,
            "coordinates": [
                [-172.1, -13.8], [-172.0, -13.8], [-172.0, -13.7], [-172.1, -13.7], [-172.1, -13.8]
            ]
        }
    ]
    
    # Create GeoJSON features
    features = []
    for island in islands:
        feature = {
            "type": "Feature",
            "properties": {
                "name": island["name"],
                "region": island["region"],
                "area": island["area"],
                "film_relevant": True
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [island["coordinates"]]
            }
        }
        features.append(feature)
    
    # Create the GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Save to file
    output_file = "small-film-islands.geojson"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Created {output_file} with {len(features)} simplified islands")
    print("Islands included:")
    for island in islands:
        print(f"  - {island['name']} ({island['area']} km²) - {island['region']}")
    
    return output_file

if __name__ == "__main__":
    create_small_islands_geojson()
