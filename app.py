"""
ALL codes in this project are original codes however a lot of research went into bug fixes and Ideas fron several websites.
However special recognition goes to the following:
 **Code Institute**: Acknowledgement for the training and utilization of `Code-Institute-Org/ci-full-template`.
Stack Overflow**: Recognized for providing invaluable assistance during troubleshooting sessions, offering insights on bug fixes.
Materialize CSS**: For providing a user-friendly front-end framework that greatly simplified the design and styling of the Twisties Cookbook application.
 Its responsive grid system, components, and rich documentation enabled the creation of a visually appealing and consistent user interface.
**Flask setup and MongoDB integration**: Thanks to testdriven.io for aditional Flask tutorials. 
**JavaScript Ideas**: Special thanks to Dev.to 


   Copyright (c) 2024 Oliver Amah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this website without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, copies of the website, 
and to permit persons to whom the website is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the website.

IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE Website.


"""
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
import cloudinary.uploader
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size limit (16MB)

mongo = PyMongo(app)


@app.route('/')
def get_index():
    """
    Route handler for the index page of the application.
    This function retrieves the most recent recipes from the database,
    calculates statistics, and passes the data to 
    the index.html template for rendering.
    """
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
    """
    Route handler for viewing a specific recipe's details.
    This function retrieves the recipe by its ID, checks user login status,
    determines if the recipe is favorited by the user, and passes relevant
    information to the 'recipe_detail.html' template.
    """
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
    """
    Route handler for displaying recipes associated with a specific tag.
    This function queries the database for recipes that contain the given tag
    and renders them on a 'recipes_by_tag.html' template.
    
    :param tag: The tag used to filter recipes.
    :return: Rendered HTML page showing recipes with the specified tag.
    """
    # Reference the collection from the database
    recipesCollection = mongo.db.recipesCollection
    # Query to find recipes with the selected tag
    recipes = recipesCollection.find({'tags': tag})
    return render_template('recipes_by_tag.html', recipes=recipes, tag=tag)


@app.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Route handler for displaying a paginated list of recipes.
    Allows users to search for recipes based on a search term and provides pagination functionality.
    
    If the user is not logged in, they are redirected to the login page.
    
    :return: Rendered HTML page showing a list of recipes that match the search term.
    """
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
    """
    Handles the contact page functionality:
    - GET: Renders the contact form for the user to fill out.
    - POST: Processes the form data, validates the inputs, and stores the message in MongoDB.
    
    :return: Renders the contact page template on GET, or redirects on form submission (POST).
    """
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
    """
    Handles the user registration process:
    - GET: Renders the registration form.
    - POST: Processes the registration form data, hashes the password, and stores the user in MongoDB.
    
    :return: Renders the registration page or redirects to login upon successful registration.
    """
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
    """
    Handles user login functionality:
    - GET: Renders the login form.
    - POST: Validates user credentials and logs in the user.

    :return: Renders the login page or redirects to the index upon successful login.
    """
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
    """
    Endpoint to refresh the user session and prevent it from expiring.
    This is typically used to keep the session active while the user is still interacting with the application.

    :return: An empty response with HTTP status code 204 (No Content).
    """
    session.modified = True
    return '', 204

@app.route('/logout')
def logout():
    """
    Endpoint to log out the user by clearing the session data.
    After logging out, the user is redirected to the login page with a success message.

    :return: Redirect to the login page.
    """
    session.clear()  # Clears all session data
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/toggle_favorite/<recipe_id>', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    Toggle the favorite status of a recipe for the logged-in user.
    If the recipe is already in the user's favorites, it is removed; 
    if not, it is added to their favorites.

    :param recipe_id: The ID of the recipe to toggle as favorite.
    :return: Redirects to the recipe detail page.
    """

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
    """
    Retrieve and display the user's favorite recipes.

    :return: Renders the favorites page with the user's favorite recipes.
    """
    
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
    """
    Endpoint to allow users to update their profile details (username, email, password).
    The user must be logged in to access this route. The form allows users to change
    their username, email, and optionally update their password.
    
    :return: Renders the profile update page (GET) or redirects after successful update (POST).
    """

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
    """
    Route to manage the user's own recipes. 
    Only accessible by logged-in users. Displays all recipes created by the current user.
    
    :return: Renders the manage_recipes.html template with the user's recipes.
    """

    if 'user' not in session:
        flash('You need to log in to manage your recipes.', 'error')
        return redirect(url_for('login'))
    
    user_recipes = mongo.db.recipesCollection.find({"added_by": session['user']})
    return render_template('manage_recipes.html', recipes=user_recipes)

# Configure Cloudinary 
cloudinary.config(
    cloud_name='dq27h3qqy',
    api_key='657419882937697',
    api_secret='zCM1OE5iDvdDUOy3-twKpygTerU',
    secure=True
)
# My last commit was done using a diffrent user name i forgot to change my user name before submitting my changes hence the vanderTech username
@app.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    """
    Route to handle the creation of a new recipe. The form data is extracted from the POST request
    and the recipe is saved in the MongoDB database. Optionally, an image can be uploaded using Cloudinary.
    
    :return: Redirects to the 'manage_recipes' page upon successful creation, or renders the create form.
    """
    username = session.get('user')

    if request.method == 'POST':
        # Handle form submission
        title = request.form.get('title')
        ingredients = request.form.getlist('ingredients[]')
        preparation_steps = request.form.getlist('preparation_steps[]')
        cuisine = request.form.get('cuisine')
        prep_time = int(request.form.get('prep_time'))
        cook_time = int(request.form.get('cook_time'))
        servings = int(request.form.get('servings'))
        tags = request.form.get('tags')
        required_tools = request.form.getlist('required_tools[]') or []

        # Handle image upload
        image_url = None
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file and image_file.filename != '':
                upload_result = cloudinary.uploader.upload(image_file)
                image_url = upload_result.get('url')

        # Create recipe dictionary
        recipe = {
            'title': title,
            'ingredients': ingredients,
            'preparation_steps': preparation_steps,
            'cuisine': cuisine,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'servings': servings,
            'image_url': image_url,
            'required_tools': required_tools,
            'tags': tags.split(',') if tags else [],
            'added_by': username,
            'date_time_added': datetime.now()
        }

        try:
            mongo.db.recipesCollection.insert_one(recipe)
            flash('Recipe created successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

        return redirect(url_for('manage_recipes'))

    # Render the form when accessed via GET
    return render_template('create_recipe.html')



@app.route('/recipe/edit/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    Route to handle the editing of a recipe. Users can modify their own recipes,
    and optionally update the recipe image by uploading a new one.

    :param recipe_id: The ID of the recipe to be edited.
    :return: Renders the edit form on GET or updates the recipe and redirects on POST.
    """
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
            'cuisine': request.form.get('cuisine'),
            'prep_time': int(request.form.get('prep_time')),
            'cook_time': int(request.form.get('cook_time')),
            'servings': int(request.form.get('servings')),
            'required_tools': request.form.getlist('required_tools[]') or [],
            'tags': request.form.get('tags').split(","),
            'date_time_edited': datetime.now()
        }

        # Handle image upload
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            # Check if the user selected a file
            if image_file and image_file.filename != '':
                # Upload the file to Cloudinary
                upload_result = cloudinary.uploader.upload(image_file)
                # Get the URL of the uploaded image
                update_data['image_url'] = upload_result.get('url')
        
        # Update the recipe document in the MongoDB collection
        mongo.db.recipesCollection.update_one({"_id": ObjectId(recipe_id)}, {"$set": update_data})
        flash('Recipe updated successfully!', 'success')

        return redirect(url_for('manage_recipes'))
  
    return render_template('edit_recipe.html', recipe=recipe, enumerate=enumerate)


@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    """
    Endpoint to handle the deletion of a recipe from the database.
    
    :param recipe_id: The ID of the recipe to be deleted.
    :return: Redirects to the 'manage_recipes' page after successful or failed deletion.
    """
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
    """
    Endpoint to display all equipment categories available in the equipmentCollection.
    
    :return: Renders the 'equipment_categories.html' template and passes the categories to the template.
    """
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
    """
    This function calculates the total number of items in the user's cart and makes 
    the count available globally in all templates. It's a context processor function, 
    meaning the result is injected into all templates automatically.
    
    :return: A dictionary containing the cart_item_count, which will be available globally.
    """
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
    """
    This endpoint returns the current number of items in the user's cart.
    It relies on the cart_count_processor function to calculate the total item count.
    
    :return: A JSON response containing the cart item count.
    """
    cart_item_count = cart_count_processor()['cart_item_count']
    return jsonify({'cart_item_count': cart_item_count})

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """
    Route to handle adding items to a user's cart.
    
    Retrieves the current user from the session, finds the user record in the database,
    and then inserts the item details into the 'cartsCollection' with reference to 
    the user who added it. On success, a success message is flashed, and JSON response 
    is sent back. If there is any error (like missing data or database issues), an error message
    is flashed and a failure response is sent.
    
    :return: JSON response with success status (True/False) based on the insertion outcome.
    """
    username = session['user']
    user = mongo.db.usersCollection.find_one({"username": username})
    user_id = user['_id']
    try:
        data = request.get_json()

        
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



@app.route('/view_cart', methods=['GET'])
def view_cart():
    """
    Route to handle the display of the current user's cart.
    
    The function retrieves the logged-in user's details from the session,
    fetches the corresponding cart items from the database, and enriches
    the data with related images and stock info from the 'equipmentCollection'.
    If the user is not logged in or not found, appropriate error messages are flashed.
    
    :return: Renders the 'view_cart.html' template with the user's cart items, or
             redirects to login if the user is not authenticated.
    """
    # Get the logged-in user from the session
    username = session.get('user')

    if not username:
        flash('Please log in to view your cart', 'error')
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    # Find the user's ID
    user = mongo.db.usersCollection.find_one({"username": username})
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('get_index'))  # Handle if the user is not found

    try:
        # Fetch all cart items for the logged-in user
        cart_items = list(mongo.db.cartsCollection.find({"user": user['_id']}))

        # Prepare a list to store cart items with image URLs
        cart_with_images = []

        # Loop through each cart item to fetch image_url from equipmentCollection
        for item in cart_items:
            # Find the corresponding equipment by item_category_id in equipmentCollection
            equipment = mongo.db.equipmentCollection.find_one({"_id": ObjectId(item['item_category_id'])})

            # Find the matching item in the equipment 'items' array and extract the image URL
            image_url = None
            if equipment and 'items' in equipment:
                for equipment_item in equipment['items']:
                    if equipment_item['name'] == item['item_name']:  # Match the item name
                        image_url = equipment_item.get('image_url', '/static/images/default.png')
                        break

            # Add the image URL and other details to the cart item data
            cart_with_images.append({
                "item_name": item['item_name'],
                "item_price": item['item_price'],
                "quantity": item['quantity'],
                "total_price": item['total_price'],
                "item_category_id": str(item['item_category_id']),
                "image_url": image_url if image_url else "/static/images/default.png",  # Fallback image
                "stock": equipment_item.get('stock', 0) if equipment_item else 0,  # Assuming there's a stock field
                "id": str(item['_id'])  # Cart item ID for updating/removing
            })

        # Render to a template (for web page)
        return render_template('view_cart.html', cart_items=cart_with_images)

    except Exception as e:
        print(f"Error fetching cart: {e}")
        flash('An error occurred while retrieving your cart. Please try again.', 'error')
        return redirect(url_for('get_index'))


@app.route('/remove_from_cart/<item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """
    Route to handle removing an item from the user's cart.

    The function retrieves the logged-in user's details from the session,
    checks if the user is authenticated, and attempts to remove the specified
    cart item from the 'cartsCollection'. If the user or item is not found, or 
    if the user is unauthorized to remove the item, appropriate messages are flashed.
    
    :param item_id: The ID of the cart item to be removed.
    :return: JSON response indicating success or failure with appropriate HTTP status codes.
    """
    # Get the logged-in user from the session
    username = session.get('user')

    if not username:
        flash('Please log in to modify your cart', 'error')
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    try:
        # Find the user's ID
        user = mongo.db.usersCollection.find_one({"username": username})

        if not user:
            flash('User not found', 'error')
            return jsonify(success=False, message="User not found"), 404

        # Remove the item from the cart for the user
        result = mongo.db.cartsCollection.delete_one({
            "_id": ObjectId(item_id),
            "user": user['_id']
        })

        if result.deleted_count > 0:
            flash('Item removed from cart', 'success')
            return jsonify(success=True, message="Item removed successfully"), 200
        else:
            flash('Failed to remove item from cart', 'error')
            return jsonify(success=False, message="Item not found or unauthorized access"), 404

    except Exception as e:
        print(f"Error removing item from cart: {e}")
        flash('An error occurred while removing the item from the cart.', 'error')
        return jsonify(success=False, message="Internal server error"), 500


@app.route('/update_cart/<item_id>', methods=['POST'])
def update_cart(item_id):
    """
    Route to handle updating the quantity of an item in the user's cart.

    The function retrieves the current user from the session, checks the validity of 
    the new quantity provided by the client, fetches the cart item from the database, 
    and updates the item's quantity and total price. If the cart item is not found 
    or if any issues arise (e.g., invalid data), appropriate error responses are returned.

    :param item_id: The ID of the cart item to be updated.
    :return: JSON response indicating success or failure.
    """
    username = session['user']
    user = mongo.db.usersCollection.find_one({"username": username})
    user_id = user['_id']

    # Get the new quantity from the request
    data = request.get_json()
    new_quantity = data.get('quantity')
    
    # Ensure the quantity is an integer (if not, this could cause calculation issues)
    try:
        new_quantity = int(new_quantity)
    except ValueError:
        return jsonify(success=False, error="Invalid quantity value"), 400

    try:
        # Fetch the cart item to get the current price
        cart_item = mongo.db.cartsCollection.find_one({"_id": ObjectId(item_id), "user": user_id})
        
        if not cart_item:
            return jsonify(success=False, error="Cart item not found"), 404

        # Get the price from the cart item and ensure it's a float for calculation
        item_price = cart_item.get('item_price', 0.0)
        try:
            item_price = float(item_price)
        except ValueError:
            return jsonify(success=False, error="Invalid item price value"), 400

        print(f"Updating cart item. Item Price: {item_price}, New Quantity: {new_quantity}")

        # Update the cart item in the database
        mongo.db.cartsCollection.update_one(
            {"_id": ObjectId(item_id), "user": user_id},
            {"$set": {
                "quantity": new_quantity,
                "total_price": new_quantity * item_price  # Update total price
            }}
        )
        flash("Cart item updated successfully.", "success")
        return jsonify(success=True)
        

    except Exception as e:
        print(f"Error updating cart item: {e}")
        return jsonify(success=False, error=str(e)), 500



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
             debug=False)
    