import json

def merge_geojson_shapes(input_file, output_file):
    """Merge all shapes from features into a single MultiPolygon feature."""

    # Load the GeoJSON file
    with open(input_file, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Initialize the merged MultiPolygon structure
    merged_feature = {
        "type": "Feature",
        "properties": {"CONTINENT": "Europe"},
        "geometry": {"type": "MultiPolygon", "coordinates": []}
    }

    # Process each feature in the GeoJSON file
    for feature in geojson_data["features"]:
        geometry = feature["geometry"]

        if geometry["type"] == "Polygon":
            # Convert Polygon to MultiPolygon format by wrapping it in an extra list
            merged_feature["geometry"]["coordinates"].append(geometry["coordinates"])

        elif geometry["type"] == "MultiPolygon":
            # Extend existing MultiPolygon coordinates
            merged_feature["geometry"]["coordinates"].extend(geometry["coordinates"])

    # Save the merged feature to a new GeoJSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_feature, f, indent=4)

merge_geojson_shapes("custom.geo.json",
                     "other-shapes.geojson")
