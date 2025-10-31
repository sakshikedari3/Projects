import pandas as pd
from parse_user_query import parse_user_query  # Make sure this file exists

# Load merged dataset
df = pd.read_csv("merge_Rainfall_Crop.csv")

print("✅ Available States:", df["State_Name"].unique())
print("✅ Available Crops:", df["Crop"].unique())
print("✅ Available Years:", df["YEAR"].unique())

# Sample question
query = "Compare the average annual rainfall in Andhra Pradesh and Tamil Nadu for the last 5 years. Also list the top 3 rice-producing districts in each state."
# Step 1: Parse the question
parsed = {
    "task": "compare_rainfall_and_crop_production",
    "states": ["kerala", "tamil nadu"],
    "years": [2011, 2012, 2013, 2014],
    "crop_type": "rice",
    "metrics": ["rainfall", "production"]
}

parsed = {
    "task": "compare_rainfall_and_crop_production",
    "states": ["kerala", "tamil nadu"],
    "years": [2011, 2012, 2013, 2014],
    "crop_type": "rice",
    "metrics": ["rainfall", "production"]
}

print("Parsed Query:", parsed)

# Step 2: Filter the dataset
filtered = df[
    (df["State_Name"].astype(str).str.lower().str.strip().isin([s.lower().strip() for s in parsed["states"]])) &  
    (df["YEAR"].isin(parsed["years"])) &
    (df["Crop"].astype(str).str.lower().str.contains(parsed["crop_type"].lower(), na=False))
]

print("Filtered Rows:", len(filtered))
print(filtered.head())

# Step 3: Aggregate results
# Average rainfall per state

monthly_cols = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
filtered["Annual_Rainfall"] = filtered[monthly_cols].sum(axis=1)

avg_rainfall = filtered.groupby("State_Name")["Annual_Rainfall"].mean()

# Top 3 crops by production per state
top_crops = (
    filtered.groupby(["State_Name", "Crop"])["Production"]
    .sum()
    .reset_index()
    .sort_values(["State_Name", "Production"], ascending=[True, False])
    .groupby("State_Name")
    .head(3)
)

if filtered.empty:
    print("⚠️ No matching data found for the given query. Please check crop type, state names, or year range.")
else:
    # Proceed with rainfall and crop analysis

# Step 4: Print the answer
    print("📊 Average Rainfall (mm):")
    for state, value in avg_rainfall.items():
        print(f" - {state.title()}: {round(value, 2)} mm")

    print("\n🌾 Top 3 Crops by Production:")
    for state in parsed["states"]:
        state_lower = state.lower()
        crops = top_crops[top_crops["State_Name"] == state_lower]
        print(f"\n{state.title()}:")
        for _, row in crops.iterrows():
            print(f" - {row['Crop'].title()}: {int(row['Production'])} tonnes")

    print("\n📁 Source: merge_Rainfall_Crop.csv (from data.gov.in)")