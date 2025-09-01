import os
import pandas as pd

# Folder containing CSV files
folder = "temperatures"

# Load all CSV files
dataframes = []
for file in os.listdir(folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder, file))
        dataframes.append(df)

# Combine into one DataFrame
data = pd.concat(dataframes, ignore_index=True)

# Convert Date column
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Drop rows without Temperature values
data = data.dropna(subset=['Temperature'])

# --- Helper function for seasons ---
def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"

# Add Season column
data['Season'] = data['Date'].dt.month.apply(get_season)

# -------------------------------------------------
# 1. Seasonal Average
# -------------------------------------------------
seasonal_avg = data.groupby('Season')['Temperature'].mean()

with open("average_temp.txt", "w") as f:
    for season, avg in seasonal_avg.items():
        f.write(f"{season}: {avg:.1f}°C\n")

# -------------------------------------------------
# 2. Largest Temperature Range
# -------------------------------------------------
station_groups = data.groupby('Station')['Temperature']
ranges = station_groups.max() - station_groups.min()
max_range = ranges.max()
stations_with_max = ranges[ranges == max_range].index

with open("largest_temp_range_station.txt", "w") as f:
    for station in stations_with_max:
        max_temp = station_groups.max()[station]
        min_temp = station_groups.min()[station]
        f.write(f"{station}: Range {max_range:.1f}°C (Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n")

# -------------------------------------------------
# 3. Temperature Stability
# -------------------------------------------------
stddevs = station_groups.std()

min_std = stddevs.min()
max_std = stddevs.max()

most_stable = stddevs[stddevs == min_std].index
most_variable = stddevs[stddevs == max_std].index

with open("temperature_stability_stations.txt", "w") as f:
    for station in most_stable:
        f.write(f"Most Stable: {station}: StdDev {min_std:.1f}°C\n")
    for station in most_variable:
        f.write(f"Most Variable: {station}: StdDev {max_std:.1f}°C\n")

print("✅ Analysis complete. Results saved in text files.")
