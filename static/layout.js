//-------modal event of signin button------------
let modal = document.getElementById('signin-modal');
function showModal() {
	modal.style.display = 'block';
}

//-------switch between signin model & register modal----------------
let returnButton = document.getElementById('return-register');
let registerModal = document.getElementById('register-modal');
function returnRegister() {
	modal.style.display = 'none';
	registerModal.style.display = 'block';
}

function returnSignIn() {
	modal.style.display = 'block';
	registerModal.style.display = 'none';
}

//--------close the modal-------------
let closeButton = document.getElementById('close');
function closeModal() {
	modal.style.display = 'none';
	registerModal.style.display = 'none';
}
