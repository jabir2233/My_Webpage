document.addEventListener('DOMContentLoaded', function() {
  var closeButtons = document.querySelectorAll('.btn-close');
  closeButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var alert = this.closest('.alert');
      alert.style.display = 'none';
    });
  });
});
