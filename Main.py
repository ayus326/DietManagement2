import pandas as pd
from rapidfuzz import process
import re
from flask import Flask, request, jsonify

# Load datasets
food_ingredients_df = pd.read_csv("Food Ingredients and Recipe Dataset (1).csv")
usda_df = pd.read_csv("cleaned_usda.csv")

app = Flask(__name__)

# Function to find closest match for ingredient
def get_usda_match(ingredient, usda_df, threshold=95):
    # Check for partial match first
    matched_rows = usda_df[usda_df['Ingredient'].str.lower().str.contains(r'\b' + re.escape(ingredient.lower()) + r'\b')]
    if not matched_rows.empty:
        print(f"Partial match found for '{ingredient}':", matched_rows.iloc[0]['Ingredient'])
        return matched_rows.iloc[0]

    # Fuzzy match if no partial match found
    usda_ingredients = usda_df['Ingredient'].str.lower().tolist()
    match = process.extractOne(ingredient, usda_ingredients)
    if match and match[1] >= threshold:
        print(f"Fuzzy match for '{ingredient}':", match[0])
        return usda_df[usda_df['Ingredient'].str.lower() == match[0]].iloc[0]

    print(f"No match found for '{ingredient}'")
    return None

# Function to create recipe instructions based on ingredients
def create_recipe_instructions(ingredient_list):
    if not ingredient_list:
        return ["No instructions available. Please enter valid ingredients."]

    steps = [
        f"1. Wash and prepare the ingredients: {', '.join(ingredient_list)}.",
        f"2. Chop all ingredients and heat some oil in a pan.",
        f"3. Cook {ingredient_list[0]} until soft and well-mixed.",
        "4. Add remaining ingredients, season with salt and spices.",
        "5. Simmer for 10-15 minutes and serve hot. Enjoy your healthy meal!"
    ]
    return steps

# 🔥 MAIN LOGIC FUNCTION: Can be used anywhere (Flask route or manual import)
def generate_recipe_logic(ingredients, calories='', protein='', carbs='', fat=''):
    input_ingredients = [i.strip().lower() for i in ingredients.split(",")]
    default_value = 1
    matched_data = []

    # Process each ingredient using USDA matching
    for ingredient in input_ingredients:
        matched = get_usda_match(ingredient, usda_df)

        if matched is not None:
            data = {
                "Ingredient": matched["Ingredient"],
                "Calories (kcal)": matched.get("Calories", default_value),
                "Protein (g)": matched.get("Protein", default_value),
                "Carbs (g)": float(carbs) if carbs else matched.get("Carbs", default_value),
                "Fat (g)": float(fat) if fat else matched.get("Fat", default_value),
                "Sugar (g)": matched.get("Sugar", default_value),
                "Sodium (mg)": matched.get("Sodium", default_value),
                "Cholesterol (mg)": matched.get("Cholesterol", default_value),
                "Vitamins": matched.get("Vitamins", "N/A")
            }
            matched_data.append(data)
        else:
            print(f"No USDA match found for ingredient '{ingredient}'")

    # User input ingredients ko dikhana hai final output mein
    user_ingredients_display = ", ".join([ing.strip() for ing in ingredients.lower().split(',')])

    # Final output row - even if match not found
    if not matched_data:
        filtered_data = [{
            "Ingredient": user_ingredients_display,
            "Calories (kcal)": default_value,
            "Protein (g)": default_value,
            "Carbs (g)": float(carbs) if carbs else default_value,
            "Fat (g)": float(fat) if fat else default_value,
            "Sugar (g)": default_value,
            "Sodium (mg)": default_value,
            "Cholesterol (mg)": default_value,
            "Vitamins": "N/A"
        }]
    else:
        # Ek hi row mein combine karna
        combined_data = {
            "Ingredient": user_ingredients_display,
            "Calories (kcal)": sum(d["Calories (kcal)"] for d in matched_data),
            "Protein (g)": sum(d["Protein (g)"] for d in matched_data),
            "Carbs (g)": float(carbs) if carbs else sum(d["Carbs (g)"] for d in matched_data),
            "Fat (g)": float(fat) if fat else sum(d["Fat (g)"] for d in matched_data),
            "Sugar (g)": sum(d["Sugar (g)"] for d in matched_data),
            "Sodium (mg)": sum(d["Sodium (mg)"] for d in matched_data),
            "Cholesterol (mg)": sum(d["Cholesterol (mg)"] for d in matched_data),
            "Vitamins": "N/A"
        }
        filtered_data = [combined_data]

    # Instructions
    instructions = create_recipe_instructions([user_ingredients_display])

    return filtered_data, instructions

# Flask Route for recipe generation
@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients', '')
    target_nutrition = data.get('nutrition', {})  # Get the nutritional targets from the request
    
    # Extract nutrition values if provided
    calories = target_nutrition.get('calories', '')
    protein = target_nutrition.get('protein', '')
    carbs = target_nutrition.get('carbs', '')
    fat = target_nutrition.get('fat', '')
    
    # Call the recipe generation function with nutrition parameters
    recipe, instructions = generate_recipe_logic(ingredients, calories, protein, carbs, fat)
    
    # Prepare the response as JSON
    return jsonify({
        'recipe': recipe,
        'instructions': instructions
    })

if __name__ == '__main__':
    app.run(debug=True)
