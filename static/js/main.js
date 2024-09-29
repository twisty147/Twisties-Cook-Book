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
};

fetch('/cart_item_count')
    .then(response => response.json())
    .then(data => {
        document.querySelector('.badge').innerText = data.cart_item_count;
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

document.addEventListener('DOMContentLoaded', function () {
    // Initialize Materialize
    M.AutoInit();

    // Reset filter functionality
    var resetFilter = document.getElementById('reset-filter');
    var urls = document.getElementById('urls');
    var recipesUrl = urls ? urls.getAttribute('data-recipes-url') : null;

    if (resetFilter && recipesUrl) {
        resetFilter.addEventListener('click', function () {
            // Clear the search field
            document.getElementById('search').value = '';

            // Redirect to the recipes URL
            window.location.href = recipesUrl;
        });
    }

    // Initialize Materialize sidenav
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);



    // Auto-hide flash messages after 5 seconds
    setTimeout(function () {
        let message = document.getElementById('flashMessage');
        if (message) {
            message.style.display = 'none';
        }
    }, 5000); // 5000 milliseconds = 5 seconds



    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);

    // When a delete link is clicked
    document.querySelectorAll('.modal-trigger').forEach(function (element) {
        element.addEventListener('click', function () {
            var recipeId = this.getAttribute('data-recipe-id');
            var recipeTitle = this.getAttribute('data-recipe-title');
            // Set the recipe title in the modal
            document.getElementById('recipeTitle').textContent = recipeTitle;
            // Set the delete form action dynamically
            var deleteForm = document.getElementById('deleteForm');
            deleteForm.setAttribute('action', '/delete_recipe/' + recipeId);
        });
    });

});

