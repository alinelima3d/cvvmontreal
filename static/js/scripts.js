function loginFn() {
  const email = document.getElementById("email").value;
  const pass = document.getElementById("password").value;
  const alertLogin = document.getElementById("alertLogin");

  //checkLogin(email, pass)
  // let url = '/get_executive_member/' + email;

  var url = "/check_login/"
  let data = {
    email: email,
    pass: pass
  }
  let fetchData = {
    method: 'POST',
    body: JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json; charset=UTF-8'
    })
  }

  fetch(url, fetchData)
  .then(res => res.json())
  .then(out => {
    if (out.error) {
      alertLogin.innerHTML = out.error;
      alertLogin.classList.add("show")
      alertLogin.classList.remove("hide")
      alertLogin.alert()
    }
    else {
      sessionStorage.setItem('userId', out.id);
      if (out.is_executive_member) {
        sessionStorage.setItem('isExecutiveMember', 'true');
        window.location.href = "/executive_member_area/";
      }
      else {
        sessionStorage.setItem('isExecutiveMember', 'false');
        window.location.href = "/member_area/";
      }

    }

  })
  .catch(err => console.log(err));

};

function logout() {
  sessionStorage.setItem('userId', '');
  sessionStorage.setItem('isExecutiveMember', '');
  window.location.href = "/";
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

function addMembership(member_id, member_name) {
  var iframeModal = window.parent.document.getElementById('iframeModal');
  var url = "/add_membership/" + member_id
  iframeModal.src = url;
  var defaultModalLabel = window.parent.document.getElementById("defaultModalLabel");
  defaultModalLabel.innerHTML = "Add Membership " + member_name;
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

function showUserPhoto() {
  // HIDE BOTAO Login

  document.getElementById("signIn").style.display = "none";
  // UNHIDE BOTAO USER
  document.getElementById("photo").style.display = "block";




  let id = sessionStorage.getItem('userId');
  let isExecutiveMember = sessionStorage.getItem('isExecutiveMember');
  if (isExecutiveMember == 'true') {
    console.log('is em')
    var url_member = '/get_executive_member_id/' + id;
    var photo_url = "https://cvvmontreal.s3.us-east-2.amazonaws.com/images/executive_member_pics/"
  }
  else {
    console.log('is not em')
    var url_member = '/get_member_id/' + id;
    var photo_url = "/static/upload/member_pics/"
  }

  document.getElementById("executive_member_area_menu").href = "/executive_member_area/" + id;
  console.log(document.getElementById("executive_member_area_menu").href);

  console.log(url_member)
  fetch(url_member)
  .then(res => res.json())
  .then(out =>
    {
      // window.location.href = "/member_area/" + out.id
      if (isExecutiveMember == 'true') {
        document.getElementById("photo").src = photo_url + out.executive_member_pic
      }
      else {
        document.getElementById("photo").src = photo_url + out.member_pic
      }
    })
  .catch(err => console.log(err));

  // HIDE EXECUTIVE MEMBER AREA
  if (isExecutiveMember == 'true') {
    document.getElementById("member_area_menu").style.display = "none";
    document.getElementById("executive_member_area_menu").style.display = "block";
    document.getElementById("content_management_menu").style.display = "block";
  }
  else {
    document.getElementById("member_area_menu").style.display = "block";
    document.getElementById("executive_member_area_menu").style.display = "none";
    document.getElementById("content_management_menu").style.display = "none";
  }

}
function showLoginBnt() {
  document.getElementById("signIn").style.display = "block";
}
function activateButton() {
  var buttons = document.getElementsByClassName("subMenuButton");
  for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].href == window.location.href) {
      buttons[i].classList.add("subMenuButtonActive")
    }
    else {
      buttons[i].classList.remove("subMenuButtonActive")
    }
  }
}

function likeNews(id) {
  console.log('like news: ' + id)
  var url = "/add_likes_news/"
  let data = {
    id: id,
  }
  let fetchData = {
    method: 'POST',
    body: JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json; charset=UTF-8'
    })
  }

  fetch(url, fetchData)
  .then(res => res.json())
  .then(out => {
    document.getElementById("likes").innerHTML = out.likes;


  })
}


function changeStatuses() {
  var checkboxes = document.getElementsByClassName("checkboxAttendance")
  for (let i = 0; i < checkboxes.length; i++) {
    console.log("id " + checkboxes[i].id)
    var splits = checkboxes[i].id.split("_")
    var member = splits[0];
    var meeting = splits[1];
    var checked = checkboxes[i].checked;
    console.log("member" + member)
    console.log("meeting" + meeting)
    console.log("checked" + checkboxes[i].checked)

    if (member) {
      var url = "/change_attendance/"
      let data = {
        member: member,
        meeting: meeting,
        checked: checked
      }
      let fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
          'Content-Type': 'application/json; charset=UTF-8'
        })
      }

      fetch(url, fetchData)
      .then(res => res.json())
      .then(out => {
        if (out.error) {
          // const alertAttendance = document.getElementById("alertAttendance");
          // alertAttendance.innerHTML = out.error;
          // alertAttendance.classList.add("show")
          // alertAttendance.classList.remove("hide")
          // alertAttendance.alert()
        }
        else {
          // const wwarningAttendance = document.getElementById("warningAttendance");
          // wwarningAttendance.innerHTML = out.result;
          // wwarningAttendance.classList.add("show")
          // wwarningAttendance.classList.remove("hide")
          // wwarningAttendance.alert()
        }
      })
      .catch(err => console.log(err));
    }
  }

}

function checkAll() {
  var checkboxes = document.getElementsByClassName("checkboxAttendance")
  for (let i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = true;
  }
}
function uncheckAll() {
  var checkboxes = document.getElementsByClassName("checkboxAttendance")
  for (let i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = false;
  }
}
function editMembership(membership_id) {
  var iframeModal = window.parent.document.getElementById('iframeModal');
  var url = "/update_membership/" + membership_id
  iframeModal.src = url;

}
