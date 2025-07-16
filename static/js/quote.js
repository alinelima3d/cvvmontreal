// Text
const textInput = document.getElementById("text");
const quotaDiv = document.getElementById("quotaDiv");
textInput.onchange = function() {
    quotaDiv.innerHTML = textInput.value;
};


// Author
const authorInput = document.getElementById("author");
const quoteAuthor = document.getElementById("quoteAuthor");
authorInput.onchange = function() {
    quoteAuthor.innerHTML = authorInput.value;
};

// Organization
const organizationInput = document.getElementById("organization");
const quoteOrganization = document.getElementById("quoteOrganization");
organizationInput.onchange = function() {
    quoteOrganization.innerHTML = organizationInput.value;
};

// Font-size
const fontSizeInput = document.getElementById("fontSize");
fontSizeInput.onchange = function() {
  console.log('mudou font size: ' + fontSizeInput.value)
    quotaDiv.style.fontSize = fontSizeInput.value + "px";
};
