const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
  container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
  container.classList.remove("active");
});

document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('.btn-close').forEach(button => {
    button.addEventListener('click', () => {
      button.parentElement.style.display = 'none';
    });
  });
});

function redirectToForgotPassword() {
  window.location.href = '/reset_password';
}