function loginFn() {
  console.log("LOGIN");
  const email = document.getElementById("email").value;
  //const pass = document.getElementById("password").value;

  //checkLogin(email, pass)
  let url = '/get_executive_user/' + email;
  fetch(url)
  .then(res => res.json())
  .then(out => {
    document.cookie = "user=aline";
    window.location.href = "/executive_member_area/" + out.id;

  })

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
  var currentUserId = document.createElement("VAR");


}

// Modal
var defaultModal = document.getElementById('defaultModal');
console.log(defaultModal);
if (defaultModal) {
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
}

function addMembership(member_id) {
  var iframeModal = window.parent.document.getElementById('iframeModal');
  console.log('member_id')
  console.log(member_id)
  var url = "/add_membership/" + member_id
  iframeModal.src = url;

  // change title do modal para add new

  // console.log("add membership")
  // var newBtn = document.getElementById('newBtn');
  // newBtn.style = "display:none"
  // var saveBtn = document.getElementById('saveBtn');
  // saveBtn.style = "display:block"
  // var cancelBtn = document.getElementById('cancelBtn');
  // cancelBtn.style = "display:block"
  // var table = document.getElementById('membershipTable');
  // var row = table.insertRow(-1);
  // var cell1 = row.insertCell(0);
  // var cell2 = row.insertCell(1);
  // var cell3 = row.insertCell(2);
  // var cell4 = row.insertCell(3);
  // cell1.style = "background-color: #ffffa6"
  // cell2.style = "background-color: #ffffa6; margin-bottom:8px"
  // cell3.style = "background-color: #ffffa6; margin-bottom:8px"
  // // cell4.style = "background-color: #ffffa6; margin-bottom:8px"
  // cell1.innerHTML = '<button class="btn blueButton">Upload bill</button>';
  // const today = new Date();
  // const year = today.getFullYear();
  // const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed, so add 1
  // const day = String(today.getDate()).padStart(2, '0');
  //
  // const formattedDate = `${year}-${month}-${day}`;
  // const formattedDateEnd = `${year+1}-${month}-${day}`;
  // cell2.innerHTML = '<input type="text" id="start" placeholder="YYYY-mm-dd" value="' + formattedDate + '" name="start" style="margin-bottom:8px">';
  // cell3.innerHTML = '<input type="text" id="end" placeholder="YYYY-mm-dd" value="' + formattedDateEnd + '" name="end" style="margin-bottom:8px">';
  // // cell4.innerHTML = '<input type="text" id="warned" placeholder="YYYY-mm-dd" name="fname" style="margin-bottom:8px">';

}

function cancelMembership() {
  var table = document.getElementById('membershipTable');
  table.deleteRow(-1);
  var newBtn = document.getElementById('newBtn');
  newBtn.style = "display:block"
  var saveBtn = document.getElementById('saveBtn');
  saveBtn.style = "display:none"
  var cancelBtn = document.getElementById('cancelBtn');
  cancelBtn.style = "display:none"
}
function saveMembership() {
  var table = document.getElementById('membershipTable');
  var start = document.getElementById('start').value;
  var end = document.getElementById('end').value;
  // save via API
  fetch('/add_membership/1', {
      method: 'POST',
      headers: {
                    "Content-Type": "application/json"
                },
      body: JSON.stringify({ // Convert the JavaScript object to a JSON string for the body
        start: start,
        end: end
      })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json(); // Or response.text() if not JSON
  })
  .then(data => {
      console.log('Success:', data);
      // Handle successful submission (e.g., display success message)
  })
  .catch(error => {
      console.error('Error:', error);
      // Handle errors (e.g., display error message)
  });


  var newBtn = document.getElementById('newBtn');
  newBtn.style = "display:block"
  var saveBtn = document.getElementById('saveBtn');
  saveBtn.style = "display:none"
  var cancelBtn = document.getElementById('cancelBtn');
  cancelBtn.style = "display:none"
}

function checkCookie() {
  let username = getCookie("username");
  if (username != "") {
   alert("Welcome again " + username);
  } else {
    username = prompt("Please enter your name:", "");
    if (username != "" && username != null) {
      setCookie("username", username, 365);
    }
  }
}
