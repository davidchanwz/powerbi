import pandas as pd

# 1. Load the Dataset
file_path = 'datasets/kaggle-energy/Country_Consumption_TWH.csv'  # Update with your file path
data = pd.read_csv(file_path)

# 2. Inspect the Dataset
print(data.head())  # View the first few rows
print(data.info())  # Check column data types and missing values
print(data.describe())  # Get summary statistics

# 3. Clean the Data
# a. Remove empty rows and columns
data = data.dropna(how='all')  # Drop rows where all values are NaN
data = data.dropna(axis=1, how='all')  # Drop columns where all values are NaN

# b. Convert 'Year' column to integer
data['Year'] = data['Year'].astype(int)

# c. Remove invalid rows
# Remove rows where 'Year' is missing or zero
data = data[data['Year'] > 0]

# 4. Add Year-on-Year Growth Rate
for country in data.columns[1:]:  # Exclude the 'Year' column
    data[f'{country}_Growth_Rate'] = data[country].pct_change() * 100

# 5. Reshape the Data for Power BI
# Melt the data from wide to long format
long_data = data.melt(id_vars=['Year'], var_name='Country', value_name='Energy_Consumption')

# Optional: Add Year-on-Year Growth Rate to Long Data
long_data['Growth_Rate'] = data.melt(id_vars=['Year'], value_vars=data.columns[1:], var_name='Country', value_name='Growth_Rate')['Growth_Rate']

# 6. Validate the Data
# Check for missing or invalid values
print(long_data.isnull().sum())  # Check for null values
print(long_data.head())  # Preview the processed data

# 7. Save the Processed Data
output_path = 'processed/processed_energy_data.csv'
long_data.to_csv(output_path, index=False)
print(f"Processed data saved to {output_path}")