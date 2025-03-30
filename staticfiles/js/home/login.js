let password = document.getElementById("password");
let password_view = document.getElementById("password_view");
// console.log(password_view);

password_view.addEventListener('click', function () {
    if (password.type == "password") {
        password.type = "text";
        password_view.innerHTML = '<i class="fas fa-eye"></i>';
        password_view.title = "Hide Password";
    } else {
        password.type = "password";
        password_view.innerHTML = '<i class="fas fa-eye-slash"></i>';
        password_view.title = "View Password";
    }
})