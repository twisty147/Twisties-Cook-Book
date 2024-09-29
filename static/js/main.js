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
        addToCartButton.onclick = function() {
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
