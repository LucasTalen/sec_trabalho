function triggerFileInput() {
    document.getElementById('profile-pic').click();
}

function loadProfilePic(event) {
    const profilePicPreview = document.getElementById('profile-pic-preview');
    profilePicPreview.src = URL.createObjectURL(event.target.files[0]);
}