document.addEventListener("DOMContentLoaded", function() {
    var currentPath = window.location.pathname;
    var navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        if (currentPath.startsWith(link.getAttribute('href'))) {
            document.querySelector('.nav-link.active')?.classList.remove('active');
            link.classList.add('active');
        }
    });
});