document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".custom-form");
  const resultContainer = document.getElementById("resultContainer");

  // Form Data Object
  const formData = {};

  // Event Listener for Form Submission
  form.addEventListener("submit", function (event) {
    event.preventDefault();

    if (validateForm()) {
      collectFormData();
      calculatePrice();
    }
  });

  // Validate Form Inputs
  function validateForm() {
    const errorMessages = document.querySelectorAll(".text-danger");
    errorMessages.forEach((error) => (error.textContent = "")); // Clear previous errors

    let isValid = true;

    // List of fields to validate
    const fieldsToValidate = [
      { name: "bedrooms", type: "number" },
      { name: "bathrooms", type: "number", validate: validateBathrooms },
      { name: "garageSpaces", type: "number" },
      { name: "yearBuilt", type: "number" },
      { name: "patiosPorches", type: "number" },
      { name: "lotSize", type: "number" },
      { name: "houseSize", type: "number" },
      { name: "numStories", type: "number" },
      { name: "hasHoa", type: "select" },
      { name: "appliances", type: "number" },
      { name: "purchaseYear", type: "year", validate: validatePurchaseYear },
    ];

    // Validate each field
    fieldsToValidate.forEach(({ name, type, validate }) => {
      const field = form.querySelector(`[name="${name}"]`);
      const value = field ? field.value.trim() : null;

      if (!value || (type === "number" && isNaN(value))) {
        showError(name, `Please enter a valid ${name}.`);
        isValid = false;
      } else if (validate && !validate(value)) {
        isValid = false; // Error messages are handled in the validate function
      }
    });

    return isValid;
  }

  // Custom Validators
  function validateBathrooms(value) {
    if (value % 1 !== 0 && value % 1 !== 0.5) {
      showError("bathrooms", "Bathrooms must be an integer or end in .5.");
      return false;
    }
    return true;
  }

  function validatePurchaseYear(value) {
    const currentYear = new Date().getFullYear();
    if (parseInt(value, 10) < currentYear) {
      showError("purchaseYear", "Please enter a future or current year.");
      return false;
    }
    return true;
  }

  // Display Error Message
  function showError(fieldName, message) {
    const errorElement = document.getElementById(`${fieldName}Error`);
    if (errorElement) errorElement.textContent = message;
  }

  // Collect Form Data
  function collectFormData() {
    const fields = [
      "address",
      "latitude",
      "longitude",
      "zipCode",
      "bedrooms",
      "bathrooms",
      "garageSpaces",
      "yearBuilt",
      "patiosPorches",
      "lotSize",
      "houseSize",
      "numStories",
      "hasHoa",
      "appliances",
      "purchaseYear",
    ];

    fields.forEach((field) => {
      const input = form.querySelector(`[name="${field}"]`);
      if (input) {
        formData[field] = input.value.trim();
      }
    });
  }

  // Calculate Price Logic
  function calculatePrice() {
    let totalPrice = 300000;

    totalPrice += (parseInt(formData.bedrooms) || 0) * 50000;
    totalPrice += (parseInt(formData.bathrooms) || 0) * 30000;
    totalPrice += (parseInt(formData.garageSpaces) || 0) * 20000;
    totalPrice += Math.max(0, 2000 - parseInt(formData.yearBuilt) || 0) * 2000;
    totalPrice += (parseInt(formData.patiosPorches) || 0) * 10000;
    totalPrice += ((parseInt(formData.lotSize) || 0) / 100) * 5000;
    totalPrice += ((parseInt(formData.houseSize) || 0) / 100) * 10000;
    totalPrice += Math.max(0, (parseInt(formData.numStories) || 1) - 1) * 30000;

    // Final adjustment
    totalPrice += totalPrice * 0.012;

    displayResult(`Estimated Price: $${totalPrice.toFixed(2)}`);
  }

  // Display Result
  function displayResult(resultText) {
    resultContainer.textContent = resultText;
  }
});
