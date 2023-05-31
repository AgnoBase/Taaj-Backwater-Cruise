
 function tpPage(){
    window.open("tpPage.html")
 }

 function redirect(){
    window.location.href = "service.html"
 }

//name validation
 const nameInput = document.querySelector('#name');
const nameError = document.querySelector('#name-error');

nameInput.addEventListener('input', () => {
  // Reset error message
  nameError.textContent = '';

  // Validate name field
   if (nameInput.value.trim().length < 2) {
    nameError.textContent = 'Name must be at least 2 characters long.';
  } else if (!isValidName(nameInput.value.trim())) {
    nameError.textContent = 'Please enter a valid name (letters only).';
  }
});

// Helper function for validating name field
function isValidName(name) {
  const nameRegex = /^[a-zA-Z]+$/;
  return nameRegex.test(name);
}


// Date Validation function

const dateInput = document.querySelector('#date');
const dateError = document.querySelector('#date-error');

// Set minimum date to today's date
const today = new Date();
const todayString = today.toISOString().split('T')[0];
dateInput.setAttribute('min', todayString);

dateInput.addEventListener('input', () => {
  // Reset error message
  dateError.textContent = '';

  // Validate date field
  if (dateInput.value < todayString) {
    dateError.textContent = 'Please select a date that is not in the past.';
  }
});


const adultsInput = document.querySelector('#adults');
const adultsError = document.querySelector('#adults-error');

adultsInput.addEventListener('input', () => {
  // Validate number of adults
  const adultsValue = adultsInput.value;
  if (adultsValue < 1) {
    adultsInput.classList.add('invalid');
    adultsError.textContent = 'Number of adults must be more than 0';
  } else {
    adultsInput.classList.remove('invalid');
    adultsError.textContent = '';
  }
});