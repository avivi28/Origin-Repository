function checkDigit(event) {
	let code = event.which ? event.which : event.keyCode;
	if ((code < 48 || code > 57) && code > 31) {
		return false; //cannot enter a-z
	}
	return true;
}

//---------Verify the user status------
let bookingCookie = document.cookie;

function verifyUser() {
	if (bookingCookie == '') {
		location.href = '/';
	}
}

verifyUser();

//---------Get Planned Info from API-------
const bookingAPIUrl = '/api/booking';
let bookingBody = document.getElementById('entire_information');
let footer = document.querySelector('footer');
let orderedData;

function getBookingAPI() {
	showLoading();
	fetch(bookingAPIUrl, {
		method: 'GET',
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			orderedData = Res['data'];
			if (orderedData == null) {
				bookingBody.textContent = '目前沒有任何待預訂的行程';
				bookingBody.style = 'margin: 35px 0px 40px';
				footer.style = 'padding-bottom: 806px';
			} else {
				showData(Res);
				showUserData();
			}
		})
		.catch((error) => console.log(error));
}

getBookingAPI();

//------------show the data after connected get API------------
let convertedDate;
function showData(Res) {
	const returnData = Res['data'];
	let attractionData = returnData['attraction'];

	let attractionImage = document.getElementById('attraction_image');
	attractionImage.src = attractionData['image'];
	attractionImage.className = 'informationContainer_selectedAttractionImg';

	let attractionName = document.getElementById('attraction_name');
	attractionName.textContent = '台北一日遊：' + attractionData['name'];

	let selectedDate = document.getElementById('selected_date');
	inputDate = returnData['date'];
	let newDate = new Date(inputDate);
	convertedDate = newDate.toISOString().split('T')[0];
	selectedDate.textContent = convertedDate;

	let selectedTime = document.getElementById('selected_time');
	selectedTime.textContent = returnData['time'];

	let selectedFee = document.getElementById('selected_fee');
	priceData = returnData['price'];
	selectedFee.textContent = priceData;

	let selectedPlace = document.getElementById('selected_place');
	selectedPlace.textContent = attractionData['address'];

	let totalPrice = document.getElementById('total_price');
	totalPrice.textContent = '總價：新台幣 ' + priceData + ' 元';
}

//----------get User info from JWT------------
let base64Url = bookingCookie.split('.')[1];
let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
let jsonPayload = decodeURIComponent(
	atob(base64)
		.split('')
		.map(function (c) {
			return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
		})
		.join('')
);
let userData = JSON.parse(jsonPayload);

let titleName = document.getElementById('title_username');
userName = userData['name'];
userEmail = userData['email'];
titleName.textContent = '您好，' + userName + '，待預訂的行程如下：';

//----------show User info by using data in JWT-------
function showUserData() {
	document.getElementById('contact_name').setAttribute('value', userName);
	document.getElementById('contact_email').setAttribute('value', userEmail);
}

//-----------delete the selected booking--------------
function deleteBooking() {
	fetch(bookingAPIUrl, {
		method: 'DELETE',
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			deleteData = Res['ok'];
			if (deleteData == true) {
				location.reload();
			}
		})
		.catch((error) => console.log(error));
}

//--------loading effect-----------

function showLoading() {
	document.getElementById('loader').style.display = 'none';
	document.getElementById('attraction_image').style.display = 'block';
}

function showConnecting() {
	document.getElementById('connecting_loader').style.display = 'block';
}

//---------Connect TapPay Frontend--------
TPDirect.setupSDK(
	// 設置好等等 GetPrime 所需要的金鑰
	124004,
	'app_RRWnuNSgOB8XTulbmwnfWKznImPCXant2F5L3R8jSe8OX6tiTDoMVOk2p65T',
	'sandbox'
);

let cardViewContainer = document.getElementById('cardview-container');

const fields = {
	number: {
		element: document.getElementById('card-number'),
		placeholder: '**** **** **** ****',
	},
	expirationDate: {
		element: document.getElementById('card-expiration-date'),
		placeholder: 'MM / YY',
	},
	ccv: {
		element: document.getElementById('card-ccv'),
		placeholder: 'ccv',
	},
};

// 把 TapPay 內建style給植入到 div 中
TPDirect.card.setup({
	fields: fields,
	styles: {
		input: {
			color: 'gray',
		},
		'input.ccv': {
			'font-size': '16px',
		},
		'input.expiration-date': {
			'font-size': '16px',
		},
		'input.card-number': {
			'font-size': '16px',
		},
		'.valid': {
			color: 'green',
		},
		'.invalid': {
			color: 'red',
		},
		'@media screen and (max-width: 400px)': {
			input: {
				color: 'orange',
			},
		},
	},
});

let numberTick = document.getElementById('number_tick');
let numberCross = document.getElementById('number_cross');

let expiryTick = document.getElementById('expiry_tick');
let expiryCross = document.getElementById('expiry_cross');

let ccvTick = document.getElementById('ccv_tick');
let ccvCross = document.getElementById('ccv_cross');

TPDirect.card.onUpdate(function (update) {
	// number 欄位是錯誤的
	if (update.status.number === 2) {
		numberCross.style.display = 'block';
		numberTick.style.display = 'none';
	} else if (update.status.number === 0) {
		numberCross.style.display = 'none';
		numberTick.style.display = 'block';
	} else {
		numberCross.style.display = 'none';
		numberTick.style.display = 'none';
	}

	if (update.status.expiry === 2) {
		expiryCross.style.display = 'block';
		expiryTick.style.display = 'none';
	} else if (update.status.expiry === 0) {
		expiryCross.style.display = 'none';
		expiryTick.style.display = 'block';
	} else {
		expiryCross.style.display = 'none';
		expiryTick.style.display = 'none';
	}

	if (update.status.ccv === 2) {
		ccvCross.style.display = 'block';
		ccvTick.style.display = 'none';
	} else if (update.status.ccv === 0) {
		ccvCross.style.display = 'none';
		ccvTick.style.display = 'block';
	} else {
		ccvCross.style.display = 'none';
		ccvTick.style.display = 'none';
	}
});

// 讓 button click 之後觸發 getPrime 方法
let returnMessage = document.getElementById('return_message');

function onClick() {
	// 取得 TapPay Fields 的 status
	const tappayStatus = TPDirect.card.getTappayFieldsStatus();
	let phoneNumberInput = document.getElementById('phone_number').value;

	// fail to getPrime
	if (tappayStatus.canGetPrime === false) {
		returnMessage.textContent = '請確認付款資訊是否輸入正確!';
		returnMessage.style.display = 'block';
		returnMessage.style.color = 'red';
		return;
	}

	// Get prime
	TPDirect.card.getPrime((result) => {
		if (phoneNumberInput == null) {
			returnMessage.textContent = '請確認手機號碼是否輸入正確!';
			returnMessage.style.display = 'block';
			returnMessage.style.color = 'red';
			return;
		}
		if (result.status !== 0) {
			returnMessage.textContent = '錯誤訊息:' + result.msg;
			returnMessage.style.display = 'block';
			returnMessage.style.color = 'red';
			return;
		}

		let prime = result.card.prime;
		submitPrime(prime);
	});

	//---------send prime to backend-----------
	function submitPrime(prime) {
		let primeData = {
			prime: prime,
			order: {
				price: orderedData['price'],
				trip: {
					attraction: orderedData['attraction'],
					date: convertedDate,
					time: orderedData['time'],
				},
				contact: {
					name: userName,
					email: userEmail,
					phone: phoneNumberInput,
				},
			},
		};

		fetch('/api/orders', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(primeData),
			credentials: 'same-origin',
		})
			.then((Res) => Res.json())
			.then((Res) => {
				showConnecting();
				resData = Res['data'];
				orderNumber = Res['data']['number'];
				if (resData != null) {
					successBooking();
				} else {
					returnMessage.textContent = '付款錯誤，請重新嘗試!';
					returnMessage.style.display = 'block';
					returnMessage.style.color = 'red';
				}
			})
			.catch((error) => console.log(error));
	}
}

function successBooking() {
	fetch(bookingAPIUrl, {
		method: 'DELETE',
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			deleteData = Res['ok'];
			if (deleteData == true) {
				location.href = '/thankyou?number=' + orderNumber;
			}
		})
		.catch((error) => console.log(error));
}
