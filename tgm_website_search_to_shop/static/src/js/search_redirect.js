/** @odoo-module **/

/**
 * Intercepts the website search bar form submission and redirects
 * to /shop?search= so that product results appear as cards/grid
 * instead of the default plain-text search results list.
 */
document.addEventListener('DOMContentLoaded', function () {
    const searchForms = document.querySelectorAll(
        'form.o_searchbar_form, form[action="/website/search"]'
    );
    searchForms.forEach(function (form) {
        form.setAttribute('action', '/shop');

        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            const input = form.querySelector('input[name="search"]');
            const searchTerm = input ? input.value.trim() : '';
            window.location.href = '/shop?search=' + encodeURIComponent(searchTerm);
        });
    });
});
