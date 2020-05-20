cont = document.getElementById('cont');

fetch('/index.html').then(res => cont.textContent = res)