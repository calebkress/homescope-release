document.addEventListener('DOMContentLoaded', function() {
  var formData = {
    zipCode: '',
    bedrooms: '',
    bathrooms: '',
    garageSpaces: '',
    yearBuilt: '',
    patiosPorches: '',
    lotSize: '',
    houseSize: '',
    numStories: '',
  };

  var form = document.querySelector('.custom-form');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); 
    // only calculate price if form is valid
    if (validateForm()) {
      calculatePrice();
    }
  });

  function validateForm() {
    // Reset error messages
    var errorMessages = document.querySelectorAll('.text-danger');
    errorMessages.forEach(function(error) {
      error.textContent = '';
    });

    var isValid = true;

    // Validate each input
    // Home Type
    var homeType = form.querySelector('[name="homeType"]').value;
    if (!homeType) {
      document.getElementById('homeTypeError').textContent = 'Please select a home type.';
      isValid = false;
    }
    // Zipcode
    var zipcode = form.querySelector('[name="zipCode"]').value;
    if (!zipcode || isNaN(zipcode)) {
      document.getElementById('zipCodeError').textContent = 'Please enter a valid zipcode.';
      isValid = false;
    }

    // Bedrooms
    var bedrooms = form.querySelector('[name="bedrooms"]').value;
    if (!bedrooms || isNaN(bedrooms)) {
      document.getElementById('bedroomsError').textContent = 'Please enter a valid number of bedrooms.';
      isValid = false;
    }

    // Bathrooms
    var bathrooms = form.querySelector('[name="bathrooms"]').value;
    if (!bathrooms || isNaN(bathrooms)) {
      document.getElementById('bathroomsError').textContent = 'Please enter a valid number of bathrooms.';
      isValid = false;
    } else if (bathrooms % 1 !== 0 && bathrooms % 1 !== 0.5) {
      document.getElementById('bathroomsError').textContent = 'Please enter a valid number of bathrooms (integer or .5).';
      isValid = false;
    }
    // Garage Spaces
    var garageSpaces = form.querySelector('[name="garageSpaces"]').value;
    if (!garageSpaces || isNaN(garageSpaces)) {
      document.getElementById('garageSpacesError').textContent = 'Please enter a valid number of garage spaces.';
      isValid = false;
    }
    // Year Built
    var yearBuilt = form.querySelector('[name="yearBuilt"]').value;
    if (!yearBuilt || isNaN(yearBuilt)) {
      document.getElementById('yearBuiltError').textContent = 'Please enter a valid year built.';
      isValid = false;
    }
    // Patios/Porches
    var patiosPorches = form.querySelector('[name="patiosPorches"]').value;
    if (!patiosPorches || isNaN(patiosPorches)) {
      document.getElementById('patiosPorchesError').textContent = 'Please enter a valid number of patios/porches.';
      isValid = false;
    }
    // Lot Size
    var lotSize = form.querySelector('[name="lotSize"]').value;
    if (!lotSize || isNaN(lotSize)) {
      document.getElementById('lotSizeError').textContent = 'Please enter a valid lot size.';
      isValid = false;
    }
    // House Size
    var houseSize = form.querySelector('[name="houseSize"]').value;
    if (!houseSize || isNaN(houseSize)) {
      document.getElementById('houseSizeError').textContent = 'Please enter a valid house size.';
      isValid = false;
    }
    // Number of Stories
    var numStories = form.querySelector('[name="numStories"]').value;
    if (!numStories || isNaN(numStories)) {
      document.getElementById('numStoriesError').textContent = 'Please enter a valid number of stories.';
      isValid = false;
    }
    // Prospective Purchase Year 
    var purchaseYear = form.querySelector('[name="purchaseYear"]').value;
    var currentYear = new Date().getFullYear();
    if (purchaseYear < currentYear) {
      document.getElementById('purchaseYearError').textContent = 'Please enter a valid year.';
      isValid = false;
    }

    return isValid;
  }

  function calculatePrice() {
    // Collect values from the form
    formData.zipCode = form.querySelector('[name="zipCode"]').value;
    formData.bedrooms = form.querySelector('[name="bedrooms"]').value;
    formData.bathrooms = form.querySelector('[name="bathrooms"]').value;
    formData.garageSpaces = form.querySelector('[name="garageSpaces"]').value;
    formData.yearBuilt = form.querySelector('[name="yearBuilt"]').value;
    formData.patiosPorches = form.querySelector('[name="patiosPorches"]').value;
    formData.lotSize = form.querySelector('[name="lotSize"]').value;
    formData.houseSize = form.querySelector('[name="houseSize"]').value;
    formData.numStories = form.querySelector('[name="numStories"]').value;

    let totalPrice = 300000; 

    totalPrice += parseInt(formData.bedrooms || 0) * 50000;
    totalPrice += parseInt(formData.bathrooms || 0) * 30000;
    totalPrice += parseInt(formData.garageSpaces || 0) * 20000;
    totalPrice += Math.max(0, 2000 - parseInt(formData.yearBuilt || 0)) * 2000;
    totalPrice += parseInt(formData.patiosPorches || 0) * 10000;
    totalPrice += (parseInt(formData.lotSize || 0) / 100) * 5000;
    totalPrice += (parseInt(formData.houseSize || 0) / 100) * 10000;
    totalPrice += Math.max(0, parseInt(formData.numStories || 0) - 1) * 30000;
    // totalPrice = Math.min(totalPrice, 1200000);
    totalPrice = totalPrice + (totalPrice * 0.012);

    displayResult(`Estimated Price: $${totalPrice.toFixed(2)}`);
  }

  function displayResult(resultText) {
    // Ensure there's an element with the ID 'resultContainer' in your HTML to display the result
    var resultContainer = document.getElementById('resultContainer');
    resultContainer.textContent = resultText;
  }
});
