import pandas as pd
usda_df = pd.read_csv("USDA(2).csv")

# Calculate mean of each column
mean_values = usda_df[['Protein', 'Carbohydrate', 'TotalFat']].mean()

# Replace missing values with the calculated mean
usda_df[['Protein', 'Carbohydrate', 'TotalFat']] = usda_df[['Protein', 'Carbohydrate', 'TotalFat']].fillna(mean_values)

# Verify the changes
print(usda_df[['Protein', 'Carbohydrate', 'TotalFat']].head())
usda_df.to_csv("cleaned_usda.csv", index=False)

