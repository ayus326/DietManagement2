import pandas as pd
from rapidfuzz import process
import re

# Load datasets
food_ingredients_df = pd.read_csv("Food Ingredients and Recipe Dataset (1).csv")
usda_df = pd.read_csv("cleaned_usda.csv")

def get_usda_match(ingredient, usda_df, threshold=95):
    # Step 1: Partial match search (improve with case insensitivity and spaces handling)
    matched_rows = usda_df[usda_df['Ingredient'].str.lower().str.contains(r'\b' + re.escape(ingredient.lower()) + r'\b')]
    if not matched_rows.empty:
        print(f"Partial match found for '{ingredient}':", matched_rows.iloc[0]['Ingredient'])
        return matched_rows.iloc[0]  # return full row

    # Step 2: Fuzzy match if partial match fails
    usda_ingredients = usda_df['Ingredient'].str.lower().tolist()
    match = process.extractOne(ingredient, usda_ingredients)
    if match and match[1] >= threshold:
        print(f"Fuzzy match for '{ingredient}':", match[0])
        return usda_df[usda_df['Ingredient'].str.lower() == match[0]].iloc[0]

    print(f"No match found for '{ingredient}'")
    return None

# Clean ingredient names from food ingredients dataset
allowed_ingredients = set()
for row in food_ingredients_df["Ingredient"].dropna():
    ingredients = re.findall(r"[a-zA-Z]+(?: [a-zA-Z]+)*", row)
    for ing in ingredients:
        ing_clean = ing.strip().lower()
        if len(ing_clean) > 2:
            allowed_ingredients.add(ing_clean)

print("Sample allowed ingredients:", list(allowed_ingredients)[:30])

# User input processing
user_input = "onion, tomato, cheese"  # Example input
input_ingredients = [i.strip().lower() for i in user_input.split(",")]

# Step 3: Match ingredients and fetch nutrition data
matched_nutrition_data = []

# Default value for missing nutrition data
default_nutrition_value = 1  # You can adjust this as per your needs

for ingredient in input_ingredients:
    if ingredient in allowed_ingredients:
        matched_row = get_usda_match(ingredient, usda_df)
        if matched_row is not None:
            # Fetch nutrition values with proper handling for missing or 0.0 values
            nutrition_info = {
                "Ingredient": ingredient,
                "Calories (kcal)": matched_row.get("Calories", default_nutrition_value),
                "Protein (g)": matched_row.get("Protein", default_nutrition_value),
                "Carbs (g)": matched_row.get("Carbs", default_nutrition_value),
                "Fat (g)": matched_row.get("Fat", default_nutrition_value),
                "Sugar (g)": matched_row.get("Sugar", default_nutrition_value),
                "Sodium (mg)": matched_row.get("Sodium", default_nutrition_value),
                "Cholesterol (mg)": matched_row.get("Cholesterol", default_nutrition_value),
                "Vitamins": matched_row.get("Vitamins", "N/A")
            }

            # If a nutrition value is found to be 0 or missing, log a warning
            for nutrient, value in nutrition_info.items():
                if value == 0 or value is None:
                    print(f"Warning: Missing or 0 value for {nutrient} in '{ingredient}'")

            matched_nutrition_data.append(nutrition_info)
        else:
            print(f"No match found for '{ingredient}' in USDA dataset.")
    else:
        print(f"'{ingredient}' is not a valid ingredient from allowed list.")

# Step 4: Display matched nutrition data
print("\nMatched Nutrition Data:")
for item in matched_nutrition_data:
    print(item)
