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
2. [Usecase](#usecase)
3. [Design](#design)
4. [Development](#development)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Credits](#credits)
8. [License](#license)


# Requirements

## 1. Functional Requirements

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


## 1.1. Non-Functional Requirements

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

## 1.2. Requirements Engineering
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
   - Below the welcome message, there should be a dashboard summary showing:
   - **Total Recipes**: Displays the total number of recipes in the database.
   - **Recipes Added by User**: Displays the count of recipes added by the logged-in user.
   - **Favorited Recipes**: Displays the count of recipes favorited by the user.
   - Additional cards allow users to:
   - **Manage My Recipes**: Link to the recipe management page.
   - **View All Recipes**: Link to view all available recipes.
   - **Update Account**: Link to the account update page.
   ### For Guests:
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