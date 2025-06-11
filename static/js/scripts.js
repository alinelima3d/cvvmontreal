
function loginFn() {
  console.log("LOGIN");
  const email = document.getElementById("email").value;
  //const pass = document.getElementById("password").value;

  //checkLogin(email, pass)
  let url = '/get_executive_user/' + email;
  fetch(url)
  .then(res => res.json())
  .then(out =>
    window.location.href = "/executive_member_area/" + out.id)
  .catch(err => console.log(err));

  //checkLogin(email, pass)
  let url_member = '/get_user/' + email;
  fetch(url_member)
  .then(res => res.json())
  .then(out =>
      window.location.href = "/member_area/" + out.id)
  .catch(err => console.log(err));

  // se login for correto
  // window.location.href = "/member_area";


}

// Modal
var defaultModal = document.getElementById('defaultModal')
defaultModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var url = button.getAttribute('data-bs-url')
  var title = button.getAttribute('data-bs-title')

  var iframeModal = document.getElementById('iframeModal');
  iframeModal.src = url;
  // iframeModal.width  = iframeModal.contentWindow.document.body.scrollWidth;
  // iframeModal.height = iframeModal.contentWindow.document.body.scrollHeight;
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  var modalTitle = defaultModal.querySelector('.modal-title')
  var modalBodyInput = defaultModal.querySelector('.modal-body input')

  modalTitle.textContent = title
})
