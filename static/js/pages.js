activateButton();
var userId = sessionStorage.getItem('userId');
if (userId) {
  showUserPhoto();
}
else {
  showLoginBnt();
}
