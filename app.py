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
       return render_template('index.html')

@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
   return render_template('recipe_detail.html')



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
    