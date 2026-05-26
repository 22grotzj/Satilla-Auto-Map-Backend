import pandas as pd
import geopandas as gpd

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGqeKmxJoSXQVoM1owMlPzlh58BUWGFuaJpArRgfPN6GdulhDQhet7unrYw6Lb7Pszh8etsDhC-v23/pub?output=csv"
GEOM_PATH = "data/geometry_template.geojson"
OUTPUT_PATH = "Inland_Stream_Data.geojson"



def main():
    # Load sheet
    df = pd.read_csv(SHEET_URL)

    # Clean column names
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=True)

    # Rename BEFORE merging
    df = df.rename(columns={
        "Dissolved Oxygen (mg/L)": "DO",
        "Salinity (ppt)": "Salinity",
        "Turbidity (NTU)": "Turbidity",
        "Conductivity (uS/cm)": "Conductivity",
        "Nitrate (mg/L)": "Nitrate",
        "Phosphate (mg/L)": "Phosphate",
        "Temperature (C)": "Temperature"
    })

    # Load geometry
    geom = gpd.read_file(GEOM_PATH)
    geom.columns = geom.columns.str.strip().str.replace('\ufeff', '', regex=True)

    # Ensure FID types match
    df["FID"] = pd.to_numeric(df["FID"], errors="coerce")
    geom["FID"] = pd.to_numeric(geom["FID"], errors="coerce")

    # Merge
    merged = geom.merge(df, on="FID", how="left")

    # Remove duplicate merge columns
    merged = merged.drop(columns=[col for col in merged.columns if col.endswith("_x")])
    merged = merged.rename(columns=lambda c: c.replace("_y", ""))

    # Ensure CRS
    if merged.crs is None:
        merged.set_crs(epsg=4326, inplace=True)

    print("COLUMNS:", list(merged.columns))


    # Export
    merged.to_file(OUTPUT_PATH, driver="GeoJSON")
    print(f"Updated {len(merged)} features → {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
