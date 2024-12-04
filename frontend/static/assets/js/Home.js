document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".custom-form");
  const resultContainer = document.getElementById("resultContainer");
  const loadingIndicator = document.createElement("div");
  loadingIndicator.textContent = "Calculating...";
  loadingIndicator.style.display = "none";
  loadingIndicator.classList.add("loading-indicator");
  resultContainer.parentNode.insertBefore(loadingIndicator, resultContainer);

  const formData = {}; // Object to store form data

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    if (validateForm()) {
      collectFormData();
      calculatePrice();
    }
  });

  function validateForm() {
    const errorMessages = document.querySelectorAll(".text-danger");
    errorMessages.forEach((error) => (error.textContent = "")); // Clear previous errors

    let isValid = true;
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

    fieldsToValidate.forEach(({ name, type, validate }) => {
      const field = form.querySelector(`[name="${name}"]`);
      const value = field ? field.value.trim() : null;

      if (!value || (type === "number" && isNaN(value))) {
        showError(name, `Please enter a valid ${name}.`);
        isValid = false;
      } else if (validate && !validate(value)) {
        isValid = false;
      }
    });

    return isValid;
  }

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

  function showError(fieldName, message) {
    const errorElement = document.getElementById(`${fieldName}Error`);
    if (errorElement) errorElement.textContent = message;
  }

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

  function calculatePrice() {
    const apiUrl = "/api/predict";
    const requestData = {
      address: formData.address,
      latitude: parseFloat(formData.latitude),
      longitude: parseFloat(formData.longitude),
      zipCode: formData.zipCode,
      bedrooms: parseInt(formData.bedrooms, 10) || 0,
      bathrooms: parseFloat(formData.bathrooms) || 0,
      garageSpaces: parseInt(formData.garageSpaces, 10) || 0,
      yearBuilt: parseInt(formData.yearBuilt, 10) || 0,
      patiosPorches: parseInt(formData.patiosPorches, 10) || 0,
      lotSize: parseInt(formData.lotSize, 10) || 0,
      houseSize: parseInt(formData.houseSize, 10) || 0,
      numStories: parseInt(formData.numStories, 10) || 0,
      hasHoa: formData.hasHoa === "yesHoa" ? 1 : 0,
      appliances: parseInt(formData.appliances, 10) || 0,
      purchaseYear: parseInt(formData.purchaseYear, 10) || new Date().getFullYear(),
    };

    // Display loading indicator
    loadingIndicator.style.display = "block";
    resultContainer.textContent = "";

    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data && data.prediction) {
          displayResult(`Estimated Price: $${parseFloat(data.prediction).toFixed(2)}`);
        } else {
          displayResult("Prediction not available. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error fetching prediction:", error);
        displayResult("An error occurred while fetching the prediction.");
      })
      .finally(() => {
        // Hide loading indicator
        loadingIndicator.style.display = "none";
      });
  }

  function displayResult(resultText) {
    resultContainer.textContent = resultText;
  }
});
