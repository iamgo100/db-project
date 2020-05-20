(async () => {
    cont = document.getElementById('cont');
    res = await fetch('/index.html');
    if (res.body === 'OK') {
        cont.innerHTML = `<div>Добро пожаловать!</div>
            <div><button id="auth">Авторизация</button></div>
            <div><button id="reg">Регистрация</button></div>`
    }
})();