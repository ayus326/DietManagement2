import pandas as pd
# Load the substitutes dataset
df = pd.read_csv("ingredient_substitutes_sampled.csv")

# Clean up the ingredient and substitute columns
df['Ingredient'] = df['Ingredient'].str.upper().str.strip()  # Upper case and strip spaces
df['Substitute 1'] = df['Substitute 1'].str.upper().str.strip()
df['Substitute 2'] = df['Substitute 2'].str.upper().str.strip()

# Verify the loaded data (optional)
print(df.head())  # Check first few rows to ensure data looks correct
print(f"Ingredients in CSV: {df['Ingredient'].unique()}")  # To see the cleaned ingredients
