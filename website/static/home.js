document.addEventListener('DOMContentLoaded', function() {
  var closeButtons = document.querySelectorAll('.btn-close');
  closeButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var alert = this.closest('.alert');
      alert.style.display = 'none';
    });
  });
});


const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");
const navItems = document.querySelectorAll(".nav-links a");

/* Toggle menu */
hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
});

/* Close menu when a link is clicked (mobile UX) */
navItems.forEach(item => {
  item.addEventListener("click", () => {
    navLinks.classList.remove("active");
  });
});

/* Fix layout when resizing from mobile → desktop */
window.addEventListener("resize", () => {
  if(window.innerWidth > 768){
    navLinks.classList.remove("active");
  }
});

