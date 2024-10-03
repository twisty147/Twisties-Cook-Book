# Introduction to the Twisties Cookbook

Welcome to the **Twisties Cookbook**, a one-stop platform where culinary creativity meets convenience. Designed with food enthusiasts in mind, our web application allows you to easily find, share, and store your favorite recipes—all while discovering new ways to enhance your cooking experience.

## Purpose and Value for Users

The **Twisties Cookbook** is built for home cooks, foodies, and anyone passionate about preparing delicious meals. Our platform gives you the freedom to organize and access recipes like never before. Whether you’re searching for the perfect dish to cook tonight or want to add your own culinary creations to share with the world, the *Twisties Cookbook*  makes the process seamless.

With features like ingredient lists, step-by-step preparation instructions, personal favorite cuisine, and required tools, the application offers a comprehensive cooking experience that goes beyond simple recipes. Users can:

- **Find Recipes Easily**: Our intuitive search and directory allow you to locate recipes by ingredient, cuisine, or required cooking tools.
- **Add & Customize**: Upload your own recipes, edit them as needed, and share your unique culinary twists with the community.
- **Personal Cooking Library**: Store and manage your favorite recipes in one place, accessible from any device, any time.

## Purpose and Value for the Site Owner

In addition to being a valuable resource for users, the **Twisties Cookbook** serves as a platform to promote high-quality kitchen tools that can elevate any cooking experience. Each recipe highlights the necessary cooking tools, helping users discover the best products to enhance their culinary skills. By offering direct links and suggestions for kitchen tools, the app bridges the gap between cooking content and product discovery, ensuring a seamless integration of tools into the cooking process.

## Advanced Features

For those looking to enhance their cooking toolkit, the **Required Tools** feature highlights the best kitchen gadgets that make the recipes easier and more enjoyable to prepare. Not only do we recommend the right tools for each recipe, but we also feature our own brand of kitchen essentials, ensuring you have the best equipment at your fingertips.

With **Twisties Cookbook**, cooking becomes more than just a task—it’s an interactive, engaging, and highly personalized experience. Start exploring, sharing, and cooking with a twist today!

# Table of Contents

1. [Requirements](#requirements)
2. [Database](#database)
3. [Usecase](#usecase)
4. [Design](#design)
5. [Development](#development)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Credits](#credits)
9. [License](#license)


# REQUIREMENTS

## Functional Requirements

**User Login Verification**
   - The system must check if a user is logged in using session data.
   - If the user is not logged in, a welcome message for guests should be displayed.

**Personalized Welcome Message**
   - Display a welcome message that includes the username of the logged-in user.
   - Display a general welcome message for users who are not logged in.

**Dashboard Statistics (Nice to Have)**
   - Show statistics:
     - Total number of recipes available in the application.
     - Number of recipes added by the logged-in user.
     - Number of favorited recipes by the logged-in user.

**Quick Links Section**
   - Provide links for:
     - Home.
     - Viewing all recipes.
     - Contact.
     - Managing user recipes with CRUD Functionalities.
     - Updating user account information.

**Call to Action Button**
   - Include a prominent button that allows guests to log in to explore recipes.

**Featured Recipes Display**
   - Display a section for "Featured Recipes."

**Responsive Design**
   - Ensure that the design is adaptable across diffrent types of devices.

**Feedback Notifications**
   - Implement messages to provide feedback for various user actions.

## Non-Functional Requirements

**User Interface Design**
   - The interface should be intuitive and easy to navigate.
   - Use consistent design elements (colors, fonts) throughout the page.

**Accessibility**
   - The page must comply with WCAG 2.1 Level AA accessibility standards.

**Session Management**
   - Ensure that session data is securely managed and sensitive information is protected.

**Input Validation**
   - Validate all user inputs.

**Cross-Browser Support**
   - The website should be compatible with the latest versions of major browsers.


## Requirements Engineering
**Base Template**
   - Include CSS Frameworks
   - Include javaScript Libraries/files
   - Include header setion Brand logo linking to the home page.
   - Include a links that changes based on the user's login status.
   - Include a mobile-friendly sidebar menu.
   - Include a Main content section
   - Include a Footer Section.
   - **All pages should extend from the base template.**

**Index Page**
   - If a user is logged in, the page displays a personalized welcome message: "Welcome, {username}!".
   - **Nice to Have**Below the welcome message, there should be a dashboard summary showing:
   - **Total Recipes**: Displays the total number of recipes in the database.
   - **Recipes Added by User**: Displays the count of recipes added by the logged-in user.
   - **Favorited Recipes**: Displays the count of recipes favorited by the user.
   - Additional cards allow users to:
   - **Manage My Recipes**: Link to the recipe management page.
   - **View All Recipes**: Link to view all available recipes.
   - **Update Account**: Link to the account update page.
   - **Index Page for Guests**
      - If a user is not logged in, the page displays a welcoming message: "Welcome to Twisties Cookbook".
      - There should be a call-to-action button prompting guests to log in: "Log In to Explore Recipes".
   - **Section Header**: A heading titled "Featured Recipes" should be displayed in the center.
   - **Recipe Cards**: Each featured recipe should be shown in a card format, which includes:
   - An image of the recipe.
   - The title of the recipe.
   - The cooking time and serving information.
   - A link to view the full recipe.

**Contact Page**
   - There should be a button with a back arrow icon allowing users to navigate back to the previous page.
   - There should be a centered header with the text "Contact Us" to indicate the purpose of the page.
   - There should be a form that captures user input with the following fields:
   - **Name**: A required text input for the user's name.
   - **Email**: A required email input for the user's email address.
   - **Message**: A required textarea for the user's message.
   - A submit button with that triggers the form submission.
   - A section displaying contact information.
   - A section with a centered header "Find Us" indicating the location of Twisties Cookbook Physical office.
   - An embedded Google Map that displays the location of the business.

**Log in Page**
   - Include a message prompting users who do not have an account to register, linking to the registration page
   - Include the following fields in the login form:
      - **Email Field:**
      - **Password Field:**
      - **Submit Button**

**Registration Page**
   - Include a message prompting users who already have an account to log in, linking to the login page:
   - Include a Registration Form with the following fields: 
      - **Name Field:**
      - **Email Field:**
      - **Password Field:**
      - **Register Button**

**Recipes Page**
   - Include a button to allow users to go back to the previous page
   - Display the title of the page
   - Implement a search form for users to search recipes
   - Create a section to display the recipes
   - Implement pagination controls to navigate through multiple pages of recipes
   - Users should be able to add recipes to favorites
   - users should be able to share recipes to their page on social media
   - **NICE TO HAVE** Build upon the required tools field to promote Twisties brand of kitchen tools 
   

**Manage Recipe**
   - Users Should be able to perform CRUD functionalities on recipes. Update/Delete only for the recipes they added.

**Cart**
- The users cart page should extend the base template
- Display the title of the page
- Check if the cart is empty and display a message accordingly
- Create a list to display items in the cart
- Display a summary of the cart contents and total cost
- Confirm before deleting an item in cart
- Users should be able to edit items in their cart


# DATABASE

-**userCollection** 
   - Used for storing user information in the MongoDB collection.
      - Fields Explanation:
               - _id
               - Type: ObjectId
               - Description: This is a unique identifier for the user document in the MongoDB collection. MongoDB automatically generates this value when a new document is inserted which ensures that a specific user document can be uniquely identified within the collection.
         
               - username
               - Type: String
               - Description: This field stores the unique username chosen by the user when they registered.  The application will use this field for displaying the user's name in various parts of the application, such as on the profile page.
           
               - email
               - Type: String
               - Description: This field contains the user's email address, which they use to register, log in to the application and for communication purposes.

               - password_hash
               - Type: String
               - Description: This field stores the hashed version of the user's password. Hashing will ensure that the password is stored securely and is not readable in plain text. This hash will be used for verifying the password during the login process.

               - role
               - Type: String
               - Description: This field specifies the role of the user in the application. The role can be User, Admin, or other predefined roles based on the application's access control requirements.

               - favorited_recipes
               - Type: Array of ObjectIds
               - Description: This field is an array that stores the unique IDs of recipes that the user has marked as favorites. The IDs correspond to recipes stored in the recipesCollection. The application will use this field to check if a particular recipe is in the user’s favorites list and to display all favorited recipes on the user's profile or favorites page.

**recipesCollection**
   - Used for storing recipe information in the MongoDB collection.
         - Fields Explanation:
            -  _id
               -  Type: ObjectId
               -  Description: This is a unique identifier automatically generated by MongoDB when a new user document is inserted. It ensures that each user can be uniquely identified within the collection.

            -  title
               -  Type: String
               -  Description: The name or title of the recipe. This field is used to display the name of the dish in listings, search results, and on the recipe detail page.

            -  ingredients
               -  Type: Array of String elements
               -  Description: A list of ingredients required for the recipe. Each element in the array represents a separate ingredient, making it easier to parse and display the list in a structured manner.

            -  preparation_steps
               -  Type: Array of String elements
               -  Description: Step-by-step instructions on how to prepare the dish. Each element in the array corresponds to a separate step, making it easy to present the preparation process in a logical order.

            -  required_tools
               -  Type: Array of String elements
               -  Description: A list of kitchen tools needed to prepare the recipe. This will help the user ensure they have all the necessary equipment before starting to cook.

            -  cuisine
               -  Type: String
               -  Description: The type of cuisine the recipe belongs to, providing additional context about the dish's origin.
            
            -  prep_time
               -  Type: Integer
               -  Description: The amount of time (in minutes) required to prepare the ingredients before cooking.

            -  cook_time
               -  Type: Integer
               -  Description: The amount of time (in minutes) required to cook the dish.
            
            - servings
               -  Type: String
               -  Description: The number of servings the recipe yields, allowing users to adjust portions as needed.

            -  image_url
               -  Type: String (URL)
               -  Description: A URL pointing to an image of the prepared dish. This image will be used to visual representation on recipe listings and detail pages.
            
            -  tags
               -  Type: Array of String elements
               -  Description: A list of tags associated with the recipe, used for categorization, filtering, and searching. 
            
            -  added_by
               -  Type: String
               -  Description: The username of the person who added the recipe to the collection. This will help track the contributor and potentially offer editing privileges to the original creator.

            -  date_time_added
               -  Type: ISODate
               -  Description: The date and time when the recipe was added to the collection, stored in ISO format. This field will be used to sort or filter recipes by recency.
            
            -  date_time_edited
               -  Type: ISODate
               -  Description: The date and time when the recipe was last edited, if applicable. This field will be set to null if no edits have been made since the recipe was first added.

**equipmentCollection**
- Used for storing cooking tools/equiptments information in the MongoDB collection.
         - Fields Explanation:
            -  _id
               -  Type: ObjectId
               -  Description: A unique identifier for the equipment category, automatically generated by MongoDB. It allows for distinct identification of each document within the collection.

            -  category
               -  Type: String
               -  Description: The name of the equipment category, which helps classify and organize the kitchen tools within the collection. This will be used for filtering and searching equipment by their usage or type.

            -  items
               -  Type: Array of Object elements
               -  Description: A list of individual equipment items within the category. Each item object contains detailed information such as name, image URL, stock, price, and description.
                  -  Nested Object Fields:
                     -  name
                        -  Type: String
                        -  Description: The name of the equipment item.
                     
                     -  image_url
                        -  Type: String (URL)
                        -  Description: A URL pointing to an image of the equipment item, which can be displayed on the equipment detail page or listings.
                     
                     -  No_in_Stock
                        -  Type: Integer
                        -  Description: The number of units available in stock for the item, useful for managing inventory.
                   
                     -  price_in_pounds
                        -  Type: Integer
                        -  Description: The price of the item in pounds (£).
                     
                     -  description
                        -  Type: String
                        -  Description: A brief description of the item, explaining its purpose and usage.
                     
            -  menu_image
               -  Type: String (URL)
               -  Description: A URL pointing to an icon image representing the category. This image will be used in the menu or category listings for visual identification.

**cartsCollection**
- Used for storing items that has been added to the users cart in the MongoDB collection.
         - Fields Explanation:
            - _id
               -  Type: ObjectId
               -  Description: A unique identifier for this cartItem, automatically generated by MongoDB. It allows for distinct identification of each cart item within the collection.
            
            -  item_category_id
               -  Type: ObjectId
               -  Description: The ID of the category to which the item belongs. This references a document in the equipmentCollection to link the item to its category.

            -  item_name
               -  Type: String
               -  Description: The name of the cart item, which is part of the equipment catalog.

            -  item_price
               -  Type: String
               -  Description: The price of a single unit of the cart item in pounds (£).

            -  quantity
               -  Type: Integer
               -  Description: The number of units of the item in cart.

            -  total_price
               -  Type: Integer
               -  Description: The total price for the cart item, will be calculated by multiplying item_price by quantity.

            -  user
               -  Type: ObjectId
               -  Description: The ID of the user who made the purchase, linking this document to the user profile stored in the usersCollection.

**contactMessages**
- Used for storing messages from the contact page for the administrators view in the MongoDB collection.
         - Fields Explanation:
           -    _id
               -  Type: ObjectId
               -  Description: A unique identifier for this contact form submission, automatically generated by MongoDB. It allows for distinct identification of each message within the collection.

            -  name
               -  Type: String
               -  Description: The name of the user who submitted the contact form.

            -  email
               -  Type: String
               -  Description: The email address provided by the user for correspondence or follow-up communication.

            -  message
               -  Type: String
               -  Description: The message or inquiry sent by the user through the contact form. It could be a general inquiry, feedback, or a request for support.


# USECASE

### Actors
- **Primary Actor:** User
- **Secondary Actors:** System
### Main Flow (Basic Scenario)

**Access Home Page**
   - **Step 1:** The user navigates to the home page http://twisties-cook-book-e57860eccdee.herokuapp.com/.
      - The system queries the `recipesCollection` to retrieve the last 9 inserted recipes, sorted by `_id` in descending order.
      - The system calculates the total number of recipes in the database.
      - if the user is logged in (determined by checking the session):
         - The system queries the `usersCollection` to find the user by their username.
         - The system counts the number of recipes added by the logged-in user.
         - The system retrieves the count of recipes that the user has favorited.
         - The system renders the `index.html` template, passing the following data:
            - The latest 9 recipes.
            - The total number of recipes in the database.
            - The count of recipes added by the logged-in user.
            - The count of favorited recipes by the logged-in user.
      - if the user isnt logged in
         - The system will render the guest home page and prompt them to login.

**Access Recipe**
   - **Step 2:** The user navigates to the recipes page or the user clicks on the total recipe card or view all recipe Card.
      - The system checks if the user is logged in.
         - The system counts the total number of recipes for pagination purposes.
         - The system retrieves a subset of recipes based on the current page and the number of recipes per page (6 recipes per page).
         - The system renders the `recipes.html` template, passing the list of recipes, current page.
      -  if the user searches with the provided search field
         -  The system queries the `recipesCollection` using the search term, if provided. If no search term is entered, the query matches all recipes.
         -  The system calculates the total number of matching recipes to support pagination and determines the total number of pages based on the `per_page` value (6 recipes per page).
         -  The system retrieves the recipes for the current page and renders the `recipes.html` template, passing the recipes, current page number, total pages, and search term to the template for display.
      - if the user isnt loggedin
         - The system redirects the user to the `login.html` template page.

**Access Recipe Details**
   - **Step 3:** The user clicks on a particular recipe.
      - The system checks if the user is logged in by verifying the session.
         - The system attempts to convert the `recipe_id` to an `ObjectId`.
         - The system queries the `recipesCollection` to find the recipe by its ID.
         - The system checks if the recipe is in the user's list of favorited recipes.
         - The system sets `is_favorite` to `True` if the recipe is favorited; otherwise, it remains `False`.
         - The system renders the `recipe_detail.html` template, passing the recipe details, `is_favorite` status, and `from_page` parameters.
            - if the user clicks any of the tags
               -  The system receives the `<tag>` parameter from the URL.
               -  The system queries the `recipesCollection` in the database, searching for recipes that contain the specified `<tag>` in their `tags` field.
               -  The system renders the `recipes_by_tag.html` template, passing the list of matching recipes and the tag to the template.
            -if the user clicks on the Discover more tools here link in the required tools section.
               -  The system receives the request to view equipment categories.
               -  The system queries the `equipmentCollection` in the MongoDB database, retrieving all documents with the fields `category` (name of the category) and `menu_image` (image associated with the category).
               - The system renders the `equipment_categories.html` template, passing the list of categories to be displayed to the user.
               - if the user clicks any of the categories
                  -  The system queries the MongoDB collection `equipmentCollection` to retrieve the category based on the provided `category_id`.
                  -  The system attempts to convert the `category_id` to an `ObjectId`. If it fails (invalid `ObjectId`), the system treats `category_id` as a string.
                  -  The system retrieves the category matching the `category_id`.
                  -  The system retrieves the list of items in the category from the `items` field.
                  -  The system renders the `category_items.html` template, passing the category and its items to the template.

**Access Manage Recipes**
   - **Step 4:** The user clicks on the manage recipe card.
   - The system checks if the user is logged in.
      - The system queries the `recipesCollection` in MongoDB to retrieve recipes that were added by the logged-in user.
      - The system renders the `manage_recipes.html` template and passes the user's recipes for display, allowing the user to manage their recipe collection.
   - If the user tries to access manage recipe without being logged in, they are redirected to the login page.
   -**Step 5:** The user clicks on the manage view recipe.
      - The system checks if the user is logged in by verifying the session.
         - The system attempts to convert the `recipe_id` to an `ObjectId`.
         - The system queries the `recipesCollection` to find the recipe by its ID.
         - The system checks if the recipe is in the user's list of favorited recipes.
         - The system sets `is_favorite` to `True` if the recipe is favorited; otherwise, it remains `False`.
         - The system renders the `recipe_detail.html` template, passing the recipe details, `is_favorite` status, and `from_page` parameters.
      - If the user tries to access view recipe without being logged in, they are redirected to the login page.
   -**Step 6:** The user clicks on the edit recipe.
      -The system checks if the user is logged in.
         - The system fetches the recipe with the given `recipe_id` from the MongoDB collection.
      - If the user tries to access edit recipe without being logged in, they are redirected to the login page.
   -**Step 7** The user edits the recipe details on the form and submits the updated information via a `POST` request.
      - The system collects the updated data from the form.
      - The system updates the recipe document in the `recipesCollection` in MongoDB with the new data.
      - The user is redirected to the "Manage Recipes" page.
   -**Step 8** The user clicks on delete recipe
      - The system converts the `recipe_id` to an `ObjectId` and attempts to delete the recipe from the `recipesCollection` in the MongoDB database.
      - The user is redirected back to the "Manage Recipes" page to view the updated list of their recipes.

**Access Recipes Added By Me**
   - **Step 9** The user clicks on recipe added by me card
      - The system checks if the user is logged in.
      - The system queries the `recipesCollection` in MongoDB to retrieve recipes that were added by the logged-in user.
      - The system renders the `manage_recipes.html` template and passes the user's recipes for display, allowing the user to manage their recipe collection.
   
**Access Favorites**
   -  **Step 10** The user clicks on the my favorites card.
      -  The system checks if the user is logged in by verifying the session.
      -  If the user is logged in, the system queries the `usersCollection` to retrieve the logged-in user's document.
      -  The system extracts the list of favorited recipe IDs from the user’s document.
      -  If the user has favorited recipes, the system queries the `recipesCollection` using the list of favorite recipe IDs to retrieve the corresponding recipe documents.
      -  The system renders the `favorites.html` template, passing the list of favorite recipes to be displayed on the page.

**Update User Profile**
   - **Step 11** The user clicks on the update account card.
      -  The system checks if the user is logged in by verifying the session.
      -  The system queries the `usersCollection` to get the current user’s document using their session username.
      -  The system displays the current user profile data in the `update_profile.html` form.
      -  The user updates their username, email, or password in the form and submits it.
      -  The system checks if the provided username or email already exists in the database for another user.
      -  If there are no conflicts, the system updates the user's document in `usersCollection` with the new username, email, and (if provided) the hashed password.
      -  If the username has been changed, the system updates the session with the new username.
      -  The user is redirected to the index page where they can continue using the application with their updated profile.
