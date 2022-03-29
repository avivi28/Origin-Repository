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
const registerAPIUrl = '/api/user';
const registerForm = document.getElementById('register_form');
const nameInputForRegister = document.getElementById('register_name');
const emailInputForRegister = document.getElementById('register_email');
const pwInputForRegister = document.getElementById('register_password');

registerForm.addEventListener('submit', function register(ev) {
	ev.preventDefault();

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
				registerMessage.textContent = '註冊成功^^!!';
				nameInputForRegister.value = '';
				emailInputForRegister.value = '';
				pwInputForRegister.value = '';
			} else {
				repeatEmailHandler();
				registerMessage.textContent = '註冊失敗，Email重複QQ';
			}
		})
		.catch((error) => console.log(error));
});

//-----------Message handling after register------
let registerMessage = document.getElementById('message_after_register');

function repeatEmailHandler() {
	registerMessage.className = 'new_message';
	const registerContent = document.getElementById('register-content');
	registerContent.style.height = '355px';
}

function successRegister() {
	registerMessage.className = 'success_message';
	const registerContent = document.getElementById('register-content');
	registerContent.style.height = '355px';
}

//----------Sign in function------------
const signInForm = document.getElementById('sign_in_form');
signInForm.addEventListener('submit', function signIn(ev) {
	ev.preventDefault();

	let formData = new FormData(signInForm);
	const signInInput = new URLSearchParams(formData);
	const jsonData = Object.fromEntries(signInInput.entries());

	fetch(registerAPIUrl, {
		method: 'PATCH',
		headers: new Headers({
			'Content-Type': 'application/json;charset=utf-8',
		}),
		body: JSON.stringify(jsonData),
	})
		.then((Res) => Res.json())
		.then((Res) => {
			error = Res['error'];
			if (!error) {
				location.reload();
			} else {
				signInErrorHandler();
				signInMessage.textContent = '登入失敗，帳號或密碼錯誤';
			}
		})
		.catch((error) => console.log(error));
});

const signInMessage = document.getElementById('message_after_signin');
function signInErrorHandler() {
	signInMessage.className = 'new_message';
	const signInContent = document.getElementById('signin-content');
	signInContent.style.height = '300px';
}

//--------verify the user status-------
const signInButton = document.getElementById('signin_button');
function verifyUser() {
	fetch(registerAPIUrl, {
		method: 'GET',
		credentials: 'same-origin', //for bring cookies
	})
		.then((Res) => Res.json())
		.then((Res) => {
			const getData = Res['data'];
			if (getData != null) {
				signInButton.textContent = '登出系統';
				signInButton.removeAttribute('onclick', 'showModal()');
				signInButton.setAttribute('onclick', 'logOut()');
			} else {
				signInButton.textContent = '登入/註冊';
			}
		})
		.catch((error) => console.log(error));
}

verifyUser();

//---------logOut function----------
function logOut() {
	fetch(registerAPIUrl, {
		method: 'DELETE',
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			logOutData = Res['ok'];
			if (logOutData == true) {
				location.reload();
			}
		})
		.catch((error) => console.log(error));
}

//---------Connect to Booking Page------
let bookingButton = document.getElementById('booking_button');
let cookie = document.cookie;

function connectBooking() {
	if (cookie == '') {
		showModal();
	} else {
		location.href = '/booking';
	}
}
