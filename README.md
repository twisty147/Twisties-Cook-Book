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


## 2. Non-Functional Requirements

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

## 2. Requirements Engineering
**Home Page**
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
