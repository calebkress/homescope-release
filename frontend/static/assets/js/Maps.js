let autocomplete;

function initAutocomplete() {
const addressField = document.getElementById("address");

autocomplete = new google.maps.places.Autocomplete(addressField, {
    types: ["address"],
    componentRestrictions: { country: "us" },
});

autocomplete.addListener("place_changed", fillInAddress);
}

function fillInAddress() {
const place = autocomplete.getPlace();

if (!place.geometry || !place.geometry.location) {
    alert("No details available for input: '" + place.name + "'");
    return;
}

const latitude = place.geometry.location.lat();
const longitude = place.geometry.location.lng();

// Find ZIP code from address components
const zipComponent = place.address_components.find(component =>
    component.types.includes("postal_code")
);
const zipCode = zipComponent ? zipComponent.long_name : "";

console.log("Latitude:", latitude);
console.log("Longitude:", longitude);
console.log("ZIP Code:", zipCode);

// Populate hidden form fields or display the data
document.getElementById("latitude").value = latitude;
document.getElementById("longitude").value = longitude;
document.getElementById("zipCode").value = zipCode;
}

document.addEventListener("DOMContentLoaded", initAutocomplete);
