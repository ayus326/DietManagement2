import pandas as pd
from rapidfuzz import process
import re
from difflib import get_close_matches

# Load datasets
food_ingredients_df = pd.read_csv("Food Ingredients and Recipe Dataset (1).csv")
usda_df = pd.read_csv("cleaned_usda.csv")



def get_best_match(ingredient, usda_list):
    # Step 1: Try exact match
    for item in usda_list:
        if ingredient.lower() == item.lower():
            return item

    # Step 2: Filter USDA names with length close to ingredient name
    filtered_usda = [item for item in usda_list if len(item) <= len(ingredient) + 10]

    # Step 3: Get best fuzzy match from filtered list
    matches = get_close_matches(ingredient, filtered_usda, n=1, cutoff=0.6)
    if matches:
        return matches[0]

    return None


# Clean ingredient names from food ingredients dataset
allowed_ingredients = set()
for row in food_ingredients_df["Ingredient"].dropna():
    ingredients = re.findall(r"[a-zA-Z]+(?: [a-zA-Z]+)*", row)
    for ing in ingredients:
        ing_clean = ing.strip().lower()
        if len(ing_clean) > 2:
            allowed_ingredients.add(ing_clean)

# User input for recipe ingredients
user_input = "onion, tomato, cheese"  # Example input
input_ingredients = [i.strip().lower() for i in user_input.split(",")]

# Default value for missing nutrition data
default_nutrition_value = 1

# Fetch and display nutrition values for each ingredient
matched_nutrition_data = []
for ingredient in input_ingredients:
    if ingredient in allowed_ingredients:
        matched_row = get_usda_match(ingredient, usda_df)
        if matched_row is not None:
            nutrition_info = {
                "Ingredient": ingredient
            }
            
            # Add all nutritional values from USDA
            for nutrient in ["Calories", "Protein", "Carbs", "Fat", "Sugar", "Sodium", "Cholesterol", "Vitamins", "Fiber", "Potassium"]:
                nutrition_info[f"{nutrient}"] = matched_row.get(nutrient, default_nutrition_value)
                
                # Log warning if value is missing or 0
                if nutrition_info[f"{nutrient}"] == 0 or nutrition_info[f"{nutrient}"] is None:
                    print(f"Warning: Missing or 0 value for {nutrient} in '{ingredient}'")
            
            matched_nutrition_data.append(nutrition_info)
        else:
            print(f"No match found for '{ingredient}' in USDA dataset.")
    else:
        print(f"'{ingredient}' is not a valid ingredient from allowed list.")

# Display matched nutrition data
print("\nMatched Nutrition Data:")
for item in matched_nutrition_data:
    print(item)
