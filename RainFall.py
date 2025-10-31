import pandas as pd

# File paths
dataset1 = "crop_yield.csv"
dataset2 = "rainfall_validation.csv"

def read_csv(path):
    return pd.read_csv(path)

def clean_crop_data(df):
    df['State_Name'] = df['State_Name'].str.lower().str.strip()
    df['District_Name'] = df['District_Name'].str.lower().str.strip()
    df['Season'] = df['Season'].str.lower().str.strip()
    df['Crop'] = df['Crop'].str.lower().str.strip()
    return df

def clean_rainfall_data(df):
    df['State_Name'] = df['State_Name'].str.lower().str.strip()
    return df

def merge_datasets(df_crop, df_rain):
    return pd.merge(df_crop, df_rain, on=["State_Name", "YEAR"], how="inner")

def main():
    df_crop = read_csv(dataset1)
    df_crop = clean_crop_data(df_crop)
    df_crop.to_csv("crop_clean.csv", index=False)

    df_rain = read_csv(dataset2)
    df_rain = clean_rainfall_data(df_rain)
    df_rain.to_csv("rainfall_clean.csv", index=False)

    df_merged = merge_datasets(df_crop, df_rain)
    df_merged.to_csv("merge_Rainfall_Crop.csv", index=False)

if __name__ == "__main__":
    main()