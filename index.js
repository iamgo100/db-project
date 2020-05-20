cont = document.getElementById('cont');
req = new XMLHttpRequest();

req.open('GET', '/index.html');
req.onload = () => {
    cont.textContent = req.response
};
req.send()