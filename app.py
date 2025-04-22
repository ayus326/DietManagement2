from flask import Flask, render_template, request, redirect, url_for, flash
from Main import generate_recipe_logic
from Main2 import analyze_recipe_logic
from Main3 import modify_recipe_logic

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Recipe Generator
@app.route('/generate_recipe', methods=['GET', 'POST'])
def generate_recipe():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        calories = request.form.get('calories', '')
        protein = request.form.get('protein', '')
        carbs = request.form.get('carbs', '')
        fat = request.form.get('fat', '')

        # Call the generate_recipe_logic from Main.py
        recipe_data, instructions = generate_recipe_logic(ingredients, calories, protein, carbs, fat)
        
        # Check if recipe_data or instructions are empty, if so, pass a fallback message
        if not recipe_data:
            recipe_data = [{"Ingredient": "No matching ingredients found", "Calories (kcal)": 0, "Protein (g)": 0, "Carbs (g)": 0, "Fat (g)": 0, "Sugar (g)": 0, "Sodium (mg)": 0, "Cholesterol (mg)": 0, "Vitamins": "N/A"}]
        
        if not instructions:
            instructions = ["No recipe instructions available. Please try different ingredients."]
        
        # Render the generate.html template and pass the recipe and instructions
        return render_template('generate.html', recipe=recipe_data, instructions=instructions)
    
    # If GET request, just render the page without recipe data
    return render_template('generate.html')

# Recipe Analyzer
@app.route('/analyze_recipe', methods=['GET', 'POST'])
def analyze_recipe_route():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        
        # Call the analyze_recipe function from Main2.py
        analysis = analyze_recipe_logic(ingredients)
        
        # Render the analyze.html template and pass the analysis data
        return render_template('analyze.html', analysis=analysis)
    
    # If GET request, just render the page without analysis data
    return render_template('analyze.html')

# Recipe Modifier
@app.route('/modify_recipe', methods=['GET', 'POST'])
def modify_recipe_route():
    if request.method == 'POST':
        data = request.form
        ingredients_text = data.get('ingredients')
        ingredients = [ing.strip() for ing in ingredients_text.split(',') if ing.strip()]
        
        calories = data.get('calories', '')
        protein = data.get('protein', '')
        carbs = data.get('carbs', '')
        fat = data.get('fat', '')
        sugar = data.get('sugar', '')
        sodium = data.get('sodium', '')
        cholesterol = data.get('cholesterol', '')
        vitamins = data.get('vitamins', '')
        
        desired_nutrition = {
            "Calories": float(calories) if calories else 0,
            "Protein (g)": float(protein) if protein else 0,
            "Carbs (g)": float(carbs) if carbs else 0,
            "Fat (g)": float(fat) if fat else 0,
            "Sugar (g)": float(sugar) if sugar else 0,
            "Sodium (mg)": float(sodium) if sodium else 0,
            "Cholesterol (mg)": float(cholesterol) if cholesterol else 0,
            "Vitamins": vitamins if vitamins else "N/A"
        }

        modified_recipe = modify_recipe_logic(ingredients, desired_nutrition)
        return render_template('modify.html', modified_recipe=modified_recipe)
    
    return render_template('modify.html')

@app.route('/top10')
def top10():
    return render_template('top10.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        # Abhi ke liye bas print ya flash kar rahe hain, database ke liye later karenge
        print(f"Name: {name}, Email: {email}, Message: {message}")
        flash("Thanks for contacting us! We'll get back to you soon.", "success")
        return redirect(url_for('contact'))
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login logic here
        return redirect(url_for("index"))  # or whatever route
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle signup logic here
        return redirect(url_for("login"))
    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)
