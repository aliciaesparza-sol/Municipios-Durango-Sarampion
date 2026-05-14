import shapefile
import json

def convert_shp_to_geojson(shp_path, geojson_path):
    # Read the shapefile
    reader = shapefile.Reader(shp_path, encoding='cp1252')
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
        
    # Write GeoJSON
    geojson = {"type": "FeatureCollection", "features": buffer}
    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)

if __name__ == "__main__":
    convert_shp_to_geojson("Municipios.shp", "municipios.json")
    print("Conversion complete: municipios.json created.")
