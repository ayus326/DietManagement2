import pandas as pd


# Load CSV
df = pd.read_csv("ingredient_substitutes_sampled.csv")
df.fillna("None", inplace=True)

# Normalize case
df['Ingredient'] = df['Ingredient'].str.upper()
df['Substitute 1'] = df['Substitute 1'].str.upper()
df['Substitute 2'] = df['Substitute 2'].str.upper()

# User input
user_ingredients = ["Butter", "Sugar", "Eggs", "Flour"]
user_targets = {
    "Calories": 100,
    "Protein (g)": 5,
    "Fat (g)": 2,
    "Carbs (g)": 15,
    "Sugar (g)": 5,
    "Sodium (mg)": 50,
    "Cholesterol (mg)": 10
}

# Nutrition data for exact and partial matching
nutrition_data = {
    "BUTTER": {"Calories": 717.0, "Protein (g)": 0.85, "Fat (g)": 81.11, "Carbs (g)": 0.06, "Sugar (g)": 0.06, "Sodium (mg)": 714.0, "Cholesterol (mg)": 215.0},
    "SUGAR": {"Calories": 387.0, "Protein (g)": 0.0, "Fat (g)": 0.0, "Carbs (g)": 100.0, "Sugar (g)": 100.0, "Sodium (mg)": 0.0, "Cholesterol (mg)": 0.0},
    "EGGS": {"Calories": 143.0, "Protein (g)": 12.6, "Fat (g)": 9.5, "Carbs (g)": 1.1, "Sugar (g)": 0.4, "Sodium (mg)": 140.0, "Cholesterol (mg)": 372.0},
    "FLOUR": {"Calories": 364.0, "Protein (g)": 10.33, "Fat (g)": 1.0, "Carbs (g)": 76.3, "Sugar (g)": 0.3, "Sodium (mg)": 2.0, "Cholesterol (mg)": 0.0},
}


def get_nutrition_info(ingredient):
    # Standardize ingredient (upper case, strip spaces)
    ingredient = ingredient.strip().upper()
    
    # Check for exact match first
    if ingredient in nutrition_data:
        return nutrition_data[ingredient]
    
    # If no exact match, check for partial match with exact substring
    matches = [key for key in nutrition_data if ingredient in key and len(key.split(',')) == len(ingredient.split(','))]
    
    if matches:
        best_match = matches[0]  # Take the first valid match
        print(f"⚠️ Using partial match for '{ingredient}': {best_match}")
        return nutrition_data[best_match]

    # If no valid partial match found, check for substitutes
    substitutes = get_substitutes(ingredient)
    if substitutes:
        for substitute in substitutes:
            if substitute in nutrition_data:
                print(f"⚠️ Using substitute for '{ingredient}': {substitute}")
                return nutrition_data[substitute]
    
    # Return error if no match or substitute found
    return f"Error in data: No nutritional info found for {ingredient} or its substitutes."
nutrition_data = {
    "BUTTER": {"Calories": 717.0, "Protein (g)": 0.85, "Fat (g)": 81.11, "Carbs (g)": 0.06, "Sugar (g)": 0.06, "Sodium (mg)": 714.0, "Cholesterol (mg)": 215.0},
    "SUGAR": {"Calories": 387.0, "Protein (g)": 0.0, "Fat (g)": 0.0, "Carbs (g)": 100.0, "Sugar (g)": 100.0, "Sodium (mg)": 0.0, "Cholesterol (mg)": 0.0},
    "EGGS": {"Calories": 143.0, "Protein (g)": 12.6, "Fat (g)": 9.5, "Carbs (g)": 1.1, "Sugar (g)": 0.4, "Sodium (mg)": 140.0, "Cholesterol (mg)": 372.0},
    "FLOUR": {"Calories": 364.0, "Protein (g)": 10.33, "Fat (g)": 1.0, "Carbs (g)": 76.3, "Sugar (g)": 0.3, "Sodium (mg)": 2.0, "Cholesterol (mg)": 0.0}
}
def get_substitutes(ingredient):
    # Placeholder for actual substitute logic
    return []
user_ingredients = ["Butter", "Sugar", "Eggs", "Flour"]

# Main loop to check nutrition info
for ingredient in user_ingredients:
    result = get_nutrition_info(ingredient)
    print(f"Ingredient: {ingredient}")
    print(result)
    print("-" * 40)
