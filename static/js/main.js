function goBack() {
    window.history.back();
}

// Function to reset session timeout on user activity
function resetSession() {
    fetch('/keep_alive');  // Send a request to the server to reset session
}

// Add event listeners for any user activity
window.onload = function () {
    document.addEventListener('mousemove', resetSession);
    document.addEventListener('keypress', resetSession);
    document.addEventListener('click', resetSession);
   
    fetch('/cart_item_count')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.badge');
            if (badge) {
                badge.innerText = data.cart_item_count;
            }
            calculateTotalCost();
        });

    // Auto-logout after 10 minutes of inactivity
    let idleTime = 0;
    function timerIncrement() {
        idleTime++;
        if (idleTime >= 10) {  // After 10 minutes
            window.location.href = "/logout";  // Redirect to logout page
        }
    }

    // Increment the idle time every minute
    setInterval(timerIncrement, 60000);  // 1 minute intervals
    document.onmousemove = document.onkeypress = function () {
        idleTime = 0;  // Reset idle time on any activity
    };

    // Initialize Materialize
    M.AutoInit();

    // Reset filter functionality
    const resetFilter = document.getElementById('reset-filter');
    const urls = document.getElementById('urls');
    const recipesUrl = urls ? urls.getAttribute('data-recipes-url') : null;

    if (resetFilter && recipesUrl) {
        resetFilter.addEventListener('click', function () {
            // Clear the search field
            document.getElementById('search').value = '';
            // Redirect to the recipes URL
            window.location.href = recipesUrl;
        });
    }

    // Initialize Materialize sidenav
    const sidenavElems = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenavElems);

    // Auto-hide flash messages after 5 seconds
    setTimeout(function () {
        const message = document.getElementById('flashMessage');
        if (message) {
            message.style.display = 'none';
        }
    }, 5000); // 5000 milliseconds = 5 seconds

    // Initialize modal functionality
    const modalElems = document.querySelectorAll('.modal');
    M.Modal.init(modalElems);

    // When a delete link is clicked
    document.querySelectorAll('.modal-trigger').forEach(function (element) {
        element.addEventListener('click', function () {
            const recipeId = this.getAttribute('data-recipe-id');
            const recipeTitle = this.getAttribute('data-recipe-title');
            // Set the recipe title in the modal
            const recipeTitleElement = document.getElementById('recipeTitle');
            if (recipeTitleElement) {
                recipeTitleElement.textContent = recipeTitle;
            }
            // Set the delete form action dynamically
            const deleteForm = document.getElementById('deleteForm');
            if (deleteForm) {
                deleteForm.setAttribute('action', '/delete_recipe/' + recipeId);
            }
        });
    });
};
//JavaScript for adding and removing ingredients and preparation steps
let ingredientCount = 1;
let stepCount = 1;
let toolCount = 1;
// Add Ingredient
document.getElementById('add-ingredient-btn').addEventListener('click', function () {
    ingredientCount++;
    const newIngredient = `
                <div class="input-field" id="ingredient-${ingredientCount}" style="display: flex;">
                    <input type="text" id="ingredient_input_${ingredientCount}" name="ingredients[]" required>
                    <label for="ingredient_input_${ingredientCount}">Ingredient ${ingredientCount}</label>
                    <i class="material-icons red-text delete-ingredient" style="cursor: pointer;">delete</i>
                </div>`;
    document.getElementById('ingredients-section').insertAdjacentHTML('beforeend', newIngredient);
});

// Add Preparation Step
document.getElementById('add-step-btn').addEventListener('click', function () {
    stepCount++;
    const newStep = `
                <div class="input-field" id="step-${stepCount}" style="display: flex;">
                    <textarea id="preparation_step_${stepCount}" name="preparation_steps[]" class="materialize-textarea" required></textarea>
                    <label for="preparation_step_${stepCount}">Step ${stepCount}</label>
                    <i class="material-icons red-text delete-step" style="cursor: pointer;">delete</i>
                </div>`;
    document.getElementById('preparation-steps-section').insertAdjacentHTML('beforeend', newStep);
});

// Delete Ingredient
document.getElementById('ingredients-section').addEventListener('click', function (e) {
    if (e.target.classList.contains('delete-ingredient')) {
        e.target.parentElement.remove();
    }
});

// Delete Preparation Step
document.getElementById('preparation-steps-section').addEventListener('click', function (e) {
    if (e.target.classList.contains('delete-step')) {
        e.target.parentElement.remove();
    }
});


// Add Required Tool
document.getElementById('add-tool-btn').addEventListener('click', function () {
    toolCount++;
    const newTool = `
        <div class="input-field" id="tool-${toolCount}" style="display: flex;">
            <input type="text" id="tool_input_${toolCount}" name="required_tools[]" required>
            <label for="tool_input_${toolCount}">Tool ${toolCount}</label>
            <i class="material-icons red-text delete-tool" style="cursor: pointer;">delete</i>
        </div>`;
    document.getElementById('tools-section').insertAdjacentHTML('beforeend', newTool);
});

// Delete Required Tool
document.getElementById('tools-section').addEventListener('click', function (e) {
    if (e.target.classList.contains('delete-tool')) {
        e.target.parentElement.remove();
    }
});
function addToCart(categoryId, itemName, itemPrice, itemIndex) {
    const quantityInput = document.getElementById(`quantity-${itemIndex}`);
    const quantity = parseInt(quantityInput.value);

    if (!quantity || quantity < 1) {
        quantityInput.style.borderColor = 'red';
        return;
    }

    const totalPrice = itemPrice * quantity;

    const data = {
        category_id: categoryId,
        item_name: itemName,
        item_price: itemPrice,
        quantity: quantity,
        total_price: totalPrice
    };

    fetch('/add_to_cart', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            window.location.reload(); // Reload page regardless of success
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function showItemModal(name, imageUrl, description, price, categoryId, index, noInStock) {
    // Set the modal content
    document.getElementById('modalItemName').innerText = name;
    document.getElementById('modalItemImage').src = imageUrl;
    document.getElementById('modalItemDescription').innerText = description;
    document.getElementById('modalItemPrice').innerText = price;
    document.getElementById('modalQuantity').value = 1;
    document.getElementById('modalQuantity').max = noInStock;

    // Update Add to Cart button functionality
    const addToCartButton = document.getElementById('modalAddToCartButton');
    if (addToCartButton) {
        addToCartButton.onclick = function () {
            const quantity = document.getElementById('modalQuantity').value;
            addToCart(categoryId, name, price, index);
        };
    }

    // Open the modal
    const modalInstance = M.Modal.getInstance(document.getElementById('itemModal'));
    if (modalInstance) {
        modalInstance.open();
    }
}
function showRemoveConfirmation(itemId, itemName) {
    // Set the item title in the confirmation modal
    document.getElementById('itemTitle').innerText = itemName;

    // Update the delete form's action dynamically
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.onsubmit = function (e) {
        e.preventDefault(); // Prevent the default form submission
        removeFromCart(itemId);  // Call the remove function
    };

    // Open the modal
    const modalInstance = M.Modal.getInstance(document.getElementById('deleteModal'));
    modalInstance.open();
}

function removeFromCart(itemId) {
    fetch(`/remove_from_cart/${itemId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();  // Reload the page to update cart
            } else {
                console.error('Failed to remove item:', data.message);
                alert('Failed to remove item from cart');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function toggleEdit(itemId) {
    const displaySpan = document.getElementById(`quantity-display-${itemId}`);
    const inputField = document.getElementById(`quantity-input-${itemId}`);
    const updateButton = document.getElementById(`update-button-${itemId}`);

    if (inputField.style.display === "none") {
        // Show input field and hide display span
        inputField.style.display = "inline-block";
        displaySpan.style.display = "none";
        updateButton.style.display = "inline-block";
    } else {
        // Hide input field and show display span
        inputField.style.display = "none";
        displaySpan.style.display = "inline-block";
        updateButton.style.display = "none";
    }
}

function updateCart(itemId) {
    const quantityInput = document.getElementById(`quantity-input-${itemId}`);
    const newQuantity = parseInt(quantityInput.value);

    if (newQuantity < 1) {
        alert('Quantity must be at least 1.');
        return;
    }

    // Call your function to update the cart on the server
    fetch(`/update_cart/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: newQuantity })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update displayed quantity
                window.location.reload();

            } else {
                alert('Failed to update the cart. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
// Function to calculate the total cost of all cart items
function calculateTotalCost() {
    let totalCost = 0;

    // Select all cart items using the class `cart-item`
    const cartItems = document.querySelectorAll('.collection-item');

    // Iterate through each item and sum up the total cost
    cartItems.forEach(item => {
        // Retrieve the item price and quantity from data attributes
        const itemPrice = parseFloat(item.getAttribute('data-item-price'));
        const itemQuantity = parseInt(item.getAttribute('data-item-quantity'));

        // Calculate the total price for this item and add it to the total cost
        totalCost += itemPrice * itemQuantity;
    });

    // Display the total cost in the cart summary
    document.getElementById('total-cost').innerText = totalCost.toFixed(2);
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', calculateTotalCost);

function previewImage(event) {
    const image = document.getElementById('image_preview');
    const file = event.target.files[0]; // Get the selected file
    const reader = new FileReader();

    // When the file is loaded, show the image preview
    reader.onload = function () {
        image.src = reader.result; // Set the image src to the loaded file
        image.style.display = 'block'; // Show the image
    }

    // Read the image file as a data URL
    if (file) {
        reader.readAsDataURL(file);
    }
}
// Add more ingredients, steps, and tools dynamically on page load
document.addEventListener('DOMContentLoaded', function () {
    let ingredientCount = parseInt("{{ recipe.ingredients|length or 0 }}", 10);
    let stepCount = parseInt("{{ recipe.preparation_steps|length or 0 }}", 10);
    let toolCount = parseInt("{{ recipe.required_tools|length or 0 }}", 10);

    // Add Ingredient
    document.getElementById('add-ingredient-btn').addEventListener('click', function () {
        ingredientCount++;
        const newIngredient = `
            <div class="input-field" style="display: flex;" id="ingredient-${ingredientCount}">
                <input type="text" id="ingredient_input_${ingredientCount}" name="ingredients[]" required>
                <label for="ingredient_input_${ingredientCount}">Ingredient ${ingredientCount}</label>
                <i class="material-icons red-text delete-ingredient" style="cursor: pointer;">delete</i>
            </div>`;
        document.getElementById('ingredients-section').insertAdjacentHTML('beforeend', newIngredient);
    });

    // Add Preparation Step
    document.getElementById('add-step-btn').addEventListener('click', function () {
        stepCount++;
        const newStep = `
            <div class="input-field" style="display: flex;" id="step-${stepCount}">
                <textarea id="preparation_step_${stepCount}" name="preparation_steps[]" class="materialize-textarea" required></textarea>
                <label for="preparation_step_${stepCount}">Step ${stepCount}</label>
                <i class="material-icons red-text delete-step" style="cursor: pointer;">delete</i>
            </div>`;
        document.getElementById('preparation-steps-section').insertAdjacentHTML('beforeend', newStep);
    });
    // Add Required Tool
    document.getElementById('add-tool-btn').addEventListener('click', function () {
        toolCount++;
        const newTool = `
        <div class="input-field" style="display: flex;" id="tool-${toolCount}">
            <input type="text" id="required_tool_${toolCount}" name="required_tools[]" required>
            <label for="required_tool_${toolCount}">Tool ${toolCount}</label>
            <i class="material-icons red-text delete-tool" style="cursor: pointer;">delete</i>
        </div>`;
        document.getElementById('required-tools-section').insertAdjacentHTML('beforeend', newTool);
    });
    // Delete Ingredient
    document.getElementById('ingredients-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-ingredient')) {
            e.target.parentElement.remove();
        }
    });

    // Delete Preparation Step
    document.getElementById('preparation-steps-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-step')) {
            e.target.parentElement.remove();
        }
    });
    // Delete Required Tool
    document.getElementById('required-tools-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-tool')) {
            e.target.parentElement.remove();
        }
    });
});