function revealArrow() {
	var checkBox = document.getElementById("consentCheckbox");
	console.log('1');
	if (checkBox.checked == true) {
		console.log('2');
		var arrow = document.getElementById("submit-button");
		arrow.style.display = "block";
	}
}