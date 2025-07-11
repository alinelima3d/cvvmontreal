console.log('forms')


var password_hash = document.getElementById("password_hash");
var password_hash_label = document.getElementById("password_hash_label");
var password_hash2 = document.getElementById("password_hash2");
var password_hash2_label = document.getElementById("password_hash2_label");

const update_pw = document.getElementById('update_pw');
update_pw.addEventListener('change', function() {
    // Your code to execute when the checkbox state changes
    if (this.checked) {
            console.log('Checkbox is now checked!');
            password_hash.style.display = "block";
            password_hash_label.style.display = "block";
            password_hash2.style.display = "block";
            password_hash2_label.style.display = "block";
            // Perform actions when checked
        } else {
            console.log('Checkbox is now unchecked!');
            password_hash.style.display = "none";
            password_hash_label.style.display = "none";
            password_hash2.style.display = "none";
            password_hash2_label.style.display = "none";
            // Perform actions when unchecked
        }
});


password_hash.style.display = "none";
password_hash_label.style.display = "none";
password_hash2.style.display = "none";
password_hash2_label.style.display = "none";
