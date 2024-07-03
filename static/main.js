

function validateForm() {
    let x = document.forms["login"]["username"].value;
    if (x == "") {
      alert("username must be filled out");
      return false;
    }
}

function validateFormReg() {
    let username = document.forms["register"]["username"].value;
    let password = document.forms["register"]["password"].value
    if (username == "" || password == "" ) {
        alert("Username and Password must be filled out");
        return false;
    }
}

