export function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(`${name}=`)) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

export function getToken(name) {
    let token = getCookie(name);
    if (!token) {
        //window.location.href = '/login'
    }
    return token
}

export function isLoggedIn() {
    let token = getCookie("Authorization");
    console.log(token)
    if (token != null) {
        return true
    } else {
        return false
    }
}