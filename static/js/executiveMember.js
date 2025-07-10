
console.log("FILL EXECUTIVE MEMBER")




  // HIDE BOTAO Login

  document.getElementById("signIn").style.display = "none";
  // UNHIDE BOTAO USER
  document.getElementById("photo").style.display = "block";
  let id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1)
  let url_member = '/get_executive_member_id/' + id;
  fetch(url_member)
  .then(res => res.json())
  .then(out =>
      // window.location.href = "/member_area/" + out.id
      document.getElementById("photo").src = "/static/images/upload/executive_member_pics/" + out.executive_member_pic
    )
  .catch(err => console.log(err));
  document.cookie = "usernameId=" + id;
  // document.getElementById("photo").src = "/static/images/executive_members/"+ id + ".png";
  // SE FOR MEMBER
    // HIDE EXECUTIVE MEMBER AREA
    document.getElementById("member_area_menu").style.display = "none";
    document.getElementById("executive_member_area_menu").style.display = "block";
  // SE FOR EXECUTIVE MEMBER
    // HIDE EXECUTIVE MEMBER
    // UNHIDE MEMBER AREA
