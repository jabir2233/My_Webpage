//Flash Message
document.addEventListener('DOMContentLoaded', function() {
  var closeButtons = document.querySelectorAll('.btn-close');
  closeButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var alert = this.closest('.alert');
      alert.style.display = 'none';
    });
  });
});

//Resend Timer
let timeLeft = 30;
let timer = null;

const resendBox = document.getElementById("resendBox");

// Disable resend (not clickable)
function disableResend() {
    resendBox.style.pointerEvents = "none";
    resendBox.style.opacity = "0.6";
}

// Enable resend (clickable)
function enableResend() {
    resendBox.style.pointerEvents = "auto";
    resendBox.style.opacity = "1";
}

function startCountdown() {
    disableResend();
    resendBox.innerHTML = `Resend in <span id="countdown">${timeLeft}</span>sec`;

    timer = setInterval(() => {
        timeLeft--;
        document.getElementById("countdown").textContent = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timer);

            resendBox.innerHTML =
                `<span id="resendBtn" style="color:#3b82f6;cursor:pointer;">Resend OTP</span>`;

            enableResend();

            document.getElementById("resendBtn").onclick = () => {
                timeLeft = 30;
                startCountdown();
            };
        }
    }, 1000);
}

// Start on page load
startCountdown();

// OTP Input Handling
const inputs = document.querySelectorAll(".otp-inputs input");
const otpFinal = document.getElementById("otpFinal");

inputs.forEach((input, index) => {
  input.addEventListener("input", () => {
    if (input.value.length === 1 && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }
    updateOTP();
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && index > 0 && input.value === "") {
      inputs[index - 1].focus();
    }
  });

  input.addEventListener('paste', (e) => {
    e.preventDefault();
    const data = e.clipboardData.getData("text").replace(/\D/g, "");

    if (data.length === inputs.length) {
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = data[i];
        }
        inputs[inputs.length - 1].focus();
        updateOTP();
    }
  });
});

// Combine all digits into hidden field
function updateOTP() {
  let otp = "";
  inputs.forEach((input) => otp += input.value);
  otpFinal.value = otp;
}