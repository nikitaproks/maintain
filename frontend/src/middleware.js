export async function getSession(fetch, request) {
    const cookies = request.headers.get("cookie");

    const result = await fetch('http://nginx/api/v1/users/me', {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'content-type': 'application/json',
            Cookie: cookies
        }
    })

    return await result.json();
}


export async function requireAuth(fetch, request) {
    const data = getSession(fetch, request);

    return data;
}