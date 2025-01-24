document.addEventListener('DOMContentLoaded', function() {
    function getQueryParam(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    const accessToken = getQueryParam('access_token');

    if (accessToken) {
        localStorage.setItem('access_token', accessToken);
        console.log('Access token saved to local storage.');
    } else {
        console.log('No access token found in URL.');
    }

    function isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    window.history.replaceState({}, document.title, window.location.pathname);

    if (isAuthenticated()) {
        console.log('User is authenticated.');
    } else {
        console.log('User is not authenticated.');
    }
});