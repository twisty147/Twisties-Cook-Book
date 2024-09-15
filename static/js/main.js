document.addEventListener('DOMContentLoaded', function () {
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
});
