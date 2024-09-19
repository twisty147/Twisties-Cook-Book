import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
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
    # Get the "from_page" query parameter
    from_page = request.args.get('from_page', 'home')  # Default is 'home' if not specified

    # Check if the user is logged in
    if not session.get('user'):
        flash('You need to log in to view recipe details.', 'error')
        return redirect(url_for('login'))

    try:
        # Convert recipe_id to ObjectId
        recipe_id = ObjectId(recipe_id)
    except Exception as e:
        # Handle invalid ObjectId format
        return f"Invalid recipe ID format: {e}", 400

    # Query to find the recipe by its ID
    recipe = recipesCollection.find_one_or_404({'_id': recipe_id})
    
    # Pass the recipe and from_page parameter to the template
    return render_template('recipe_detail.html', recipe=recipe, from_page=from_page)


@app.route('/recipes/tag/<tag>')
def get_recipes_by_tag(tag):
    # Reference the collection from the database
    recipesCollection = mongo.db.recipesCollection
    # Query to find recipes with the selected tag
    recipes = recipesCollection.find({'tags': tag})
    return render_template('recipes_by_tag.html', recipes=recipes, tag=tag)


@app.route('/recipes', methods=['GET'])
def get_recipes():
    # Check if the user is logged in
    if not session.get('user'):
        flash('You need to log in to explore recipes.', 'error')
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)  # Get the current page number
    per_page = 6  # Show 6 recipes per page (2 rows of 3 cards each)

    # Get search term from the request
    search_term = request.args.get('search', '')

    # Create a query that matches the search term in various fields
    query = {
        '$or': [
            {'title': {'$regex': search_term, '$options': 'i'}},
            {'ingredients': {'$regex': search_term, '$options': 'i'}},
            {'cuisine': {'$regex': search_term, '$options': 'i'}},
            {'tags': {'$regex': search_term, '$options': 'i'}},
            {'required_tools': {'$regex': search_term, '$options': 'i'}}
        ]
    }

    # Get the total number of matching recipes for pagination
    total_recipes = mongo.db.recipesCollection.count_documents(query)
    total_pages = (total_recipes + per_page - 1) // per_page  # Calculate total number of pages

    # Get the filtered and paginated recipes
    recipes_cursor = mongo.db.recipesCollection.find(query).skip((page - 1) * per_page).limit(per_page)
    recipes = list(recipes_cursor)  # Convert cursor to list for rendering

    return render_template('recipes.html', recipes=recipes, page=page, total_pages=total_pages, search_term=search_term)



@app.route('/contact', methods=['GET', 'POST'])
def get_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Validation check for empty fields
        if not name or not email or not message:
            flash('All fields are required!', 'error')  # Error message for empty fields
            return redirect(url_for('get_contact'))
        
        # Insert the form data into MongoDB
        contact_message = {
            'name': name,
            'email': email,
            'message': message
        }
        mongo.db.contactMessages.insert_one(contact_message)  # Insert into 'contactMessages' collection
        
        # Success feedback message
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('get_contact'))

    # Render the contact page on GET request
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        password_hash = generate_password_hash(password)
        
        # Create a dictionary for the new user
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': 'User'  # Hard-coded role
        }
        
        # Insert the new user into the usersCollection
        mongo.db.usersCollection.insert_one(user_data)

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = mongo.db.usersCollection.find_one({"email": email})
        if user:
            if check_password_hash(user['password_hash'], password):  
                session['user'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('get_index'))
            else:
                flash('Incorrect password, please try again.', 'error')
        else:
            flash('Email not found, please register first.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
             debug=True)
    