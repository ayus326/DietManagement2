import pandas as pd
from difflib import get_close_matches
import re

# Load USDA data
usda_df = pd.read_csv("cleaned_usda.csv")

# Manually corrected ingredients
ingredient_corrections = {
    "spinach": "Spinach, raw",
    "garlic": "Garlic, raw",
    "chicken": "Chicken breast, roasted",
    "banana": "Banana, raw",
    "tomato": "Tomato, raw",
    "onion": "Onion, raw",
    "potato": "Potato, raw"
}

# Function to clean ingredient name (strip spaces and convert to lowercase)
def clean_ingredient(ingredient):
    return ingredient.strip().lower()

# Function to get the best match for an ingredient
def get_best_match(ingredient, usda_df):
    # Apply manual corrections if needed
    if ingredient in ingredient_corrections:
        ingredient = ingredient_corrections[ingredient]

    # Clean the ingredient name before matching
    ingredient = clean_ingredient(ingredient)

    # Exact match
    for index, item in usda_df.iterrows():
        if clean_ingredient(item['Ingredient']) == ingredient:
            return item
    
    # Fuzzy match if exact doesn't work
    matches = get_close_matches(ingredient, usda_df['Ingredient'].apply(clean_ingredient).tolist(), n=1, cutoff=0.6)
    if matches:
        return usda_df[usda_df['Ingredient'].apply(clean_ingredient) == matches[0]].iloc[0]
    
    return None


# Common ingredients list - tu chahe toh isme aur bhi add kar sakta hai
common_ingredients = [
    "apple", "banana", "carrot", "spinach", "chicken", "beef", "tomato",
    "onion", "garlic", "potato", "rice", "broccoli", "cheese", "egg", "milk",
    "bread", "butter", "yogurt", "mushroom", "pepper", "cabbage", "beans",
    "cucumber", "lentils", "corn", "peas", "fish", "paneer", "tofu", "ginger"
]

def extract_ingredients(text):
    """
    Extracts known ingredients from a given text using word boundaries.
    """
    pattern = r'\b(?:' + '|'.join(common_ingredients) + r')\b'
    found = re.findall(pattern, text.lower())
    return list(set(found))  # remove duplicates


# Function to handle user input and show nutrition data
def analyze_recipe_logic(paragraph):
    input_ingredients = extract_ingredients(paragraph)
    default_nutrition_value = 1
    total_nutrition = {
        "Ingredients": ", ".join(input_ingredients),
        "Calories": 0,
        "Protein": 0,
        "Carbs": 0,
        "Fat": 0,
        "Sugar": 0,
        "Sodium": 0,
        "Cholesterol": 0,
        "Vitamins": "",
        "Fiber": 0,
        "Potassium": 0
    }

    for ingredient in input_ingredients:
        matched_row = get_best_match(ingredient, usda_df)
        if matched_row is not None:
            for nutrient in ["Calories", "Protein", "Carbs", "Fat", "Sugar", "Sodium", "Cholesterol", "Fiber", "Potassium"]:
                value = matched_row.get(nutrient, default_nutrition_value)
                if pd.isna(value):
                    value = default_nutrition_value
                total_nutrition[nutrient] += value
            # Concatenate all vitamin info
            vitamin_info = matched_row.get("Vitamins", "")
            if vitamin_info and vitamin_info != "0":
                total_nutrition["Vitamins"] += f"{ingredient}: {vitamin_info}, "
        else:
            print(f"No match found for '{ingredient}' in USDA dataset.")

    # Remove trailing comma in Vitamins
    total_nutrition["Vitamins"] = total_nutrition["Vitamins"].rstrip(', ')

    return [total_nutrition]  # Return as a list with one combined dict


# Main function to run the app
def main():
    user_input = input("Enter ingredients (comma separated): ")
    nutrition_info = analyze_recipe_logic(user_input)
    
    # Display the results
    if nutrition_info:
        for item in nutrition_info:
            print(f"Ingredient: {item['Ingredient']}")
            for nutrient, value in item.items():
                if nutrient != 'Ingredient':
                    print(f"{nutrient}: {value}")
            print("\n")
    else:
        print("No valid ingredients found.")

if __name__ == "__main__":
    main()
