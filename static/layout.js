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

//-------register function------------
const registerForm = document.getElementById('register_form');
const nameInputForRegister = document.getElementById('register_name');
const emailInputForRegister = document.getElementById('register_email');
const pwInputForRegister = document.getElementById('register_password');

registerForm.addEventListener('submit', function register(ev) {
	ev.preventDefault();

	let registerAPIUrl = '/api/user';

	let formData = new FormData(registerForm);
	const registerInput = new URLSearchParams(formData);
	const jsonData = Object.fromEntries(registerInput.entries());

	fetch(registerAPIUrl, {
		method: 'POST',
		headers: new Headers({
			'Content-Type': 'application/json;charset=utf-8',
		}),
		body: JSON.stringify(jsonData),
	})
		.then((Res) => Res.json())
		.then((Res) => {
			error = Res['error'];
			if (!error) {
				successRegister();
				returnMessage.textContent = '註冊成功^^!!';
				nameInputForRegister.value = '';
				emailInputForRegister.value = '';
				pwInputForRegister.value = '';
			} else {
				repeatEmailHandler();
				returnMessage.textContent = '註冊失敗，Email重複QQ';
			}
		})
		.catch((error) => console.log(error));
});

//-----------Message handling after register------

let returnMessage = document.getElementById('message_after_submit');

function repeatEmailHandler() {
	returnMessage.className = 'new_message';
	const registerContent = document.getElementById('register-content');
	registerContent.style.height = '355px';
}

function successRegister() {
	returnMessage.className = 'success_message';
	const registerContent = document.getElementById('register-content');
	registerContent.style.height = '355px';
}
