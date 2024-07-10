function loadComponent(url, elementId) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        });
}

loadComponent('header.html', 'header-placeholder');
loadComponent('footer.html', 'footer-placeholder');