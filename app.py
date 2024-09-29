import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 
from datetime import timedelta
from bson.errors import InvalidId 

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

mongo = PyMongo(app)


@app.route('/')
def get_index():
    # Reference the collection from the database
    recipesCollection = mongo.db.recipesCollection
    usersCollection = mongo.db.usersCollection
    
    # Query to get the last 9 inserted recipes, sorted by _id in descending order
    recipes = recipesCollection.find().sort('_id', -1).limit(9)
    
    # Initialize statistics variables
    total_recipes = recipesCollection.count_documents({})
    user_recipes_count = 0
    favorited_recipes_count = 0
    
    if 'user' in session:
        user = usersCollection.find_one({"username": session['user']})
        
        # Get the count of recipes added by the logged-in user
        user_recipes_count = recipesCollection.count_documents({"added_by": session['user']})
        
        favorited_recipes_count = len(user.get('favorited_recipes', []))
    
    return render_template(
        'index.html',
        recipes=recipes,
        total_recipes=total_recipes,
        user_recipes_count=user_recipes_count,
        favorited_recipes_count=favorited_recipes_count
    )



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
    
    is_favorite = False
    if 'user' in session:
        user = mongo.db.usersCollection.find_one({"username": session['user']})
        # Check if the recipe is in the user's favorited recipes list
        if recipe_id in user.get("favorited_recipes", []):
            is_favorite = True

    # Pass the recipe, is_favorite, and from_page parameters to the template
    return render_template('recipe_detail.html', recipe=recipe, is_favorite=is_favorite, from_page=from_page)


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
                session.permanent = True
                return redirect(url_for('get_index'))
            else:
                flash('Incorrect password, please try again.', 'error')
        else:
            flash('Email not found, please register first.', 'error')

    return render_template('login.html')


@app.route('/keep_alive')
def keep_alive():
    session.modified = True
    return '', 204

@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/toggle_favorite/<recipe_id>', methods=['POST'])
def toggle_favorite(recipe_id):

    usersCollection = mongo.db.usersCollection
    user = usersCollection.find_one({"username": session['user']})
    
    # Check if the recipe is already in the user's favorites
    favorited_recipes = user.get("favorited_recipes", [])
    
    if ObjectId(recipe_id) in favorited_recipes:
        # If it is already a favorite, remove it
        usersCollection.update_one(
            {"username": session['user']},
            {"$pull": {"favorited_recipes": ObjectId(recipe_id)}}
        )
        flash('Recipe removed from your favorites.', 'success')
    else:
        # If it is not a favorite, add it
        usersCollection.update_one(
            {"username": session['user']},
            {"$push": {"favorited_recipes": ObjectId(recipe_id)}}
        )
        flash('Recipe added to your favorites!', 'success')
    
    return redirect(url_for('get_recipe', recipe_id=recipe_id, from_page=request.args.get('from_page')))

@app.route('/favorites')
def get_favorites():
    # Check if the user is logged in
    if not session.get('user'):
        flash('You need to log in to view your favorite recipes.', 'error')
        return redirect(url_for('login'))

    # Get the logged-in user's information
    user = mongo.db.usersCollection.find_one({"username": session['user']})
    
    # Get the list of favorite recipe IDs from the user document
    favorite_recipe_ids = user.get('favorited_recipes', [])

    # If the user has favorited recipes, query the recipes collection to get them
    favorite_recipes = []
    if favorite_recipe_ids:
        # Convert the list of ObjectIds to a list of recipe documents
        favorite_recipes = list(mongo.db.recipesCollection.find({"_id": {"$in": favorite_recipe_ids}}))

    # Render the 'favorites.html' template, passing the favorite recipes
    return render_template('favorites.html', favorite_recipes=favorite_recipes)




@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    # Check if the user is logged in
    if 'user' not in session:
        flash('You need to log in to update your profile.', 'error')
        return redirect(url_for('login'))

    usersCollection = mongo.db.usersCollection
    user = usersCollection.find_one({"username": session['user']})

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the username or email already exists
        if usersCollection.find_one({"username": username, "_id": {"$ne": user["_id"]}}):
            flash('Username already exists.', 'error')
            return redirect(url_for('update_profile'))

        if usersCollection.find_one({"email": email, "_id": {"$ne": user["_id"]}}):
            flash('Email already in use.', 'error')
            return redirect(url_for('update_profile'))

        # Update the user details
        update_data = {
            'username': username,
            'email': email
        }

        # Update the password if a new one is provided
        if password:
            update_data['password_hash'] = generate_password_hash(password)

        usersCollection.update_one({"_id": user["_id"]}, {"$set": update_data})
        flash('Profile updated successfully!', 'success')

        # Update the session username if it has changed
        if username != session['user']:
            session['user'] = username

        return redirect(url_for('get_index'))

    return render_template('update_profile.html', user=user)


@app.route('/manage_recipes')
def manage_recipes():
    if 'user' not in session:
        flash('You need to log in to manage your recipes.', 'error')
        return redirect(url_for('login'))
    
    user_recipes = mongo.db.recipesCollection.find({"added_by": session['user']})
    return render_template('manage_recipes.html', recipes=user_recipes)


@app.route('/recipe/create', methods=['GET', 'POST'])
@app.route('/create_recipe', methods=['POST'])
def create_recipe():
   
    usersCollection = mongo.db.usersCollection
    user = usersCollection.find_one({"username": session['user']})
    username = session['user']
   
    if request.method == 'POST':
    # Extract form data
        title = request.form.get('title')
        ingredients = request.form.getlist('ingredients[]')
        preparation_steps = request.form.getlist('preparation_steps[]')
        cuisine = request.form.get('cuisine')
        prep_time = int(request.form.get('prep_time'))
        cook_time = int(request.form.get('cook_time'))
        servings = int(request.form.get('servings'))
        image_url = request.form.get('image_url')
        tags = request.form.get('tags')

    # Create a recipe dictionary
        recipe = {
            'title': title,
            'ingredients': ingredients,
            'preparation_steps': preparation_steps,
            'cuisine': cuisine,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'servings': servings,
            'image_url': image_url,
            'required_tools': request.form.getlist('required_tools[]') or [],  
            'tags': tags.split(',') if tags else [],  
            'added_by': username,
            'date_time_added': datetime.now()
        }

        # Insert the recipe into the MongoDB collection
        try:
            mongo.db.recipesCollection.insert_one(recipe)
            flash('Recipe created successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

        return redirect(url_for('manage_recipes')) 

    return render_template('create_recipe.html') 


@app.route('/recipe/edit/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if 'user' not in session:
        flash('You need to log in to edit a recipe.', 'error')
        return redirect(url_for('login'))

    recipe = mongo.db.recipesCollection.find_one({"_id": ObjectId(recipe_id)})
   
    if not recipe or recipe['added_by'] != session['user']:
        flash('You do not have permission to edit this recipe.', 'error')
        return redirect(url_for('manage_recipes'))

    if request.method == 'POST':
        # Update the recipe data
        update_data = {
            'title': request.form.get('title'),
            'ingredients': request.form.getlist('ingredients[]'),
            'preparation_steps': request.form.getlist('preparation_steps[]'),
            'required_tools': request.form.get('required_tools []'),
            'cuisine': request.form.get('cuisine'),
            'prep_time': request.form.get('prep_time'),
            'cook_time': request.form.get('cook_time'),
            'servings': request.form.get('servings'),
            'required_tools': request.form.getlist('required_tools[]') or [],
            'image_url': request.form.get('image_url'),
            'tags': request.form.get('tags').split(","),
            'date_time_edited': datetime.now()
            
        }
        mongo.db.recipesCollection.update_one({"_id": ObjectId(recipe_id)}, {"$set": update_data})
        flash('Recipe updated successfully!.', 'success')
        
        return redirect(url_for('manage_recipes'))
  
    return render_template('edit_recipe.html', recipe=recipe, enumerate=enumerate)

@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    try:
        mongo.db.recipesCollection.delete_one({'_id': ObjectId(recipe_id)})
        flash('Recipe deleted successfully', 'success')
    except Exception as e:
        flash('An error occurred while trying to delete the recipe', 'error')
    return redirect(url_for('manage_recipes'))


@app.route('/equipment_categories')
def show_equipment_categories():
    equipment_collection = mongo.db['equipmentCollection']
    # Retrieve all categories with their menu_image
    categories = equipment_collection.find({}, {"category": 1, "menu_image": 1, "_id": 1})

    # Pass the categories to the template
    return render_template('equipment_categories.html', categories=categories)


@app.route('/category/<category_id>')
def show_category_items(category_id):
    try:
        # Convert the category_id to ObjectId if it is a valid ObjectId
        try:
            category_id = ObjectId(category_id)
        except InvalidId:
            # If it's not a valid ObjectId, continue using it as a string
            pass

        # Query using either ObjectId or string, based on the type of category_id
        query = {"_id": category_id} if isinstance(category_id, ObjectId) else {"_id": str(category_id)}
        category = mongo.db.equipmentCollection.find_one(query)

    except Exception as e:
        # Return a 500 error page if something goes wrong with the database query
        return "An error occurred while querying the database.", 500

    if category:
        # Convert the ObjectId in the category to a string before passing to the template
        category["_id"] = str(category["_id"])
        items = category.get('items', [])
        return render_template('category_items.html', category=category, items=items)
    else:
        # Return a 404 error if the category is not found
        return "Category not found", 404


@app.context_processor
def cart_count_processor():
    cart_item_count = 0  # Default cart count

    if 'user' in session:
        # Get the logged-in username
        username = session['user']
        
        # Find the user in the usersCollection
        user = mongo.db.usersCollection.find_one({"username": username})
        if user:
            # Extract user ID
            user_id = user['_id']
            
            # Find all cart documents for the user
            carts = mongo.db.cartsCollection.find({"user": ObjectId(user_id)})
            
            # Sum up the quantity from all cart documents
            for cart in carts:
                # Check if 'quantity' field is present in the cart document
                if 'quantity' in cart:
                    # Add the quantity to the cart count
                    cart_item_count += int(cart['quantity'])
    # Make cart_item_count available globally in all templates
    return {'cart_item_count': cart_item_count}



@app.route('/cart_item_count', methods=['GET'])
def get_cart_item_count():
    cart_item_count = cart_count_processor()['cart_item_count']
    return jsonify({'cart_item_count': cart_item_count})

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    username = session['user']
    user = mongo.db.usersCollection.find_one({"username": username})
    user_id = user['_id']
    try:
        data = request.get_json()

        # Assuming you have a cartCollection to store cart items
        result= mongo.db.cartsCollection.insert_one({
            "item_category_id": ObjectId(data['category_id']),
            "item_name": data['item_name'],
            "item_price": data['item_price'],
            "quantity": data['quantity'],
            "total_price": data['total_price'],
            "user": user['_id']
        })
        # Check if the insertion was successful
        if result.inserted_id:  # This means the item was added to the cart
            flash('Item added to cart successfully!', 'success')
            return jsonify(success=True)
        else:
            flash('Failed to add item to cart. Please try again.', 'error')
            return jsonify(success=False)
        
       
    except Exception as e:
        print(f"Error adding to cart: {e}")
        flash('An error occurred while adding the item to the cart. Please try again.', 'error')
        return jsonify({"success": False}), 500



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
             debug=True)
    