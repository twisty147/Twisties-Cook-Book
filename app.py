import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
#app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")





mongo = PyMongo(app)

@app.route('/')
def get_index():
    # Reference the collection from the database
    recipesCollection = mongo.db.recipesCollection 
    # Query to get the last 9 inserted recipes, sorted by _id in descending order
    recipes = recipesCollection.find().sort('_id', -1).limit(9)
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    # Reference the collection from the database
    recipesCollection = mongo.db.recipesCollection
    try:
        # Convert recipe_id to ObjectId
        recipe_id = ObjectId(recipe_id)
    except Exception as e:
        # Handle invalid ObjectId format
        return f"Invalid recipe ID format: {e}", 400

    # Query to find the recipe by its ID
    recipe = recipesCollection.find_one_or_404({'_id': recipe_id})
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/recipes/tag/<tag>')
def get_recipes_by_tag(tag):
    # Reference the collection from the database
    recipesCollection = mongo.db.recipesCollection
    # Query to find recipes with the selected tag
    recipes = recipesCollection.find({'tags': tag})
    return render_template('recipes_by_tag.html', recipes=recipes, tag=tag)



@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = mongo.db.recipesCollection.find()
    return render_template("recipes.html", recipes=recipes)


@app.route('/contact')
def get_contact():
    return render_template('contact.html')


@app.route('/register')
def get_register():
    return render_template('register.html')


@app.route('/login')
def get_login():
    return render_template('login.html')




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
             debug=True)
    