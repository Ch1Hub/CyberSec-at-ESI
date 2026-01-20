const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const nextBtn = document.getElementById("nextBtn");


function isValidEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}

nextBtn.addEventListener("click", () => {
  const email = document.getElementById("email").value.trim();
  const pass = document.getElementById("password").value;
  const confirmPass = document.getElementById("confirmPassword").value;

  if (!email || !pass || !confirmPass) {
    alert("Please fill in all fields!");
    return;
  }

  if (!isValidEmail(email)) {
    alert("Please enter a valid email address!");
    return;
  }

  if (pass !== confirmPass) {
    alert("Passwords do not match!");
    return;
  }


  step1.classList.remove("active");
  step2.classList.add("active");
});


step2.addEventListener("submit", (e) => {
  e.preventDefault();
  const data = {
    email: document.getElementById("email").value,
    firstName: document.getElementById("firstName").value,
    lastName: document.getElementById("lastName").value,
    tel: document.getElementById("tel").value,
    address: document.getElementById("address").value,
  };

  console.log("Form submitted:", data);
  alert("Form submitted successfully!");
  
});

