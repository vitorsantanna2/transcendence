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

    const uploadButton = document.getElementById("uploadButton");
    const imageUpload = document.getElementById("imageUpload");
    const profileImage = document.getElementById("profileImage");

    // Trigger the file input when the upload button is clicked
    uploadButton.addEventListener("click", function () {
        imageUpload.click();
    });

    // Handle the file input change
    imageUpload.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imageDataUrl = e.target.result;
                // Update the profile image preview
                profileImage.src = imageDataUrl;
                // Store the image in localStorage
                localStorage.setItem("profileImage", imageDataUrl);
            };
            reader.readAsDataURL(file);
        }
    });

    // Load the stored image on page load, if available
    const storedImage = localStorage.getItem("profileImage");
    if (storedImage) {
        profileImage.src = storedImage;
    }
});