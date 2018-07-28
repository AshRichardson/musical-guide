function revealArrow() {
	var consentCheckBox = document.getElementById("consentCheckbox");
	var ageCheckBox = document.getElementById("ageCheckbox");
	var arrow = document.getElementById("submit-button");
	if (consentCheckBox.checked == true && ageCheckbox.checked == true) {
		arrow.style.display = "block";
	} else {
		arrow.style.display = "none";
	}
}