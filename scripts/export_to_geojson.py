import pandas as pd
import geopandas as gpd

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGqeKmxJoSXQVoM1owMlPzlh58BUWGFuaJpArRgfPN6GdulhDQhet7unrYw6Lb7Pszh8etsDhC-v23/pub?output=csv"
GEOM_PATH = "data/geometry_template.geojson"
OUTPUT_PATH = "data/inland_stream_data.geojson"

def main():
    df = pd.read_csv(SHEET_URL)

    df = df.rename(columns={
        "Temperature (C)": "Temperature"
        "Dissolved Oxygen (mg/L)": "DO",
        "Salinity (ppt)": "Salinity",
        "Turbidity (NTU)": "Turbidity",
        "Conductivity (uS/cm)": "Conductivity",
        "Nitrate (mg/L)": "Nitrate",
        "Phosphate (mg/L)": "Phosphate"
    })

    geom = gpd.read_file(GEOM_PATH)
    merged = geom.merge(df, on="FID", how="left")

    if merged.crs is None:
        merged.set_crs(epsg=4326, inplace=True)

    merged.to_file(OUTPUT_PATH, driver="GeoJSON")
    print(f"Updated {len(merged)} features → {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
