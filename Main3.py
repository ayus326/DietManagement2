# Main3.py
from flask import Flask, request, jsonify
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)

df = pd.read_csv('USDA_with_Substitutes.csv')

def modify_recipe_logic(ingredients, target_nutrition):
    modified_recipe = []
    
    for ingredient in ingredients:
        matches = process.extract(ingredient, df['Ingredient'], limit=1)
        best_match = matches[0][0] if matches else None
        substitute = df[df['Ingredient'] == best_match]

        if not substitute.empty:
            sub_row = substitute.iloc[0]

            # Check if essential nutrition fields are not missing
            if pd.notnull(sub_row['Calories']) and pd.notnull(sub_row['Protein']) and pd.notnull(sub_row['Carbohydrate']) and pd.notnull(sub_row['TotalFat']):
                nutrition_info = {
                    'Calories': sub_row['Calories'],
                    'Protein (g)': sub_row['Protein'],
                    'Carbs (g)': sub_row['Carbohydrate'],
                    'Fat (g)': sub_row['TotalFat'],
                    'Sugar (g)': sub_row['Sugar'],
                    'Sodium (mg)': sub_row['Sodium'],
                    'Cholesterol (mg)': sub_row['Cholesterol']
                }
            else:
                nutrition_info = "No nutrition data available."

            modified_recipe.append({
                'Ingredient': sub_row['Ingredient'],
                'Original Ingredient': ingredient,
                'Nutrition Info': nutrition_info
            })
        else:
            modified_recipe.append({
                'Ingredient': f"No substitute found for {ingredient}",
                'Original Ingredient': ingredient,
                'Nutrition Info': "No nutrition data available."
            })

    return modified_recipe

# Flask route (still optional if you want it)
@app.route('/modify_recipe', methods=['POST'])
def modify_recipe_api():
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    target_nutrition = data.get('target_nutrition', {})
    result = modify_recipe_logic(ingredients, target_nutrition)
    return jsonify(result)
