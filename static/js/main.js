function goBack() {
    window.history.back();
}
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
