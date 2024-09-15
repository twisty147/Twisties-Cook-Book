document.addEventListener('DOMContentLoaded', function() {
    var resetFilter = document.getElementById('reset-filter');
    var urls = document.getElementById('urls');
    var recipesUrl = urls.getAttribute('data-recipes-url');

 
    resetFilter.addEventListener('click', function() {
        // Clear the search field
        document.getElementById('search').value = '';
        
        // Redirect to the recipes URL
        window.location.href = recipesUrl;
    });
    

});


document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
});